import os
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from config.settings import settings
from models.job import Job, AuditLog
from models.entity import File, Entity, PseudonymMapping
from core.file_router import FileRouter
from core.detection.regex_engine import RegexEngine
from core.detection.nlp_engine import NLPEngine
from core.detection.merge_engine import MergeEngine
from core.scoring.risk_classifier import RiskClassifier
from core.redaction.text_redactor import TextRedactor
from core.redaction.image_redactor import ImageRedactor

class JobOrchestrator:
    def __init__(self, db: Session):
        self.db = db
        self.file_router = FileRouter()
        self.regex_engine = RegexEngine()
        self.nlp_engine = NLPEngine()
        self.merge_engine = MergeEngine()
        self.risk_classifier = RiskClassifier()
        self.image_redactor = ImageRedactor()

    def run_job(self, job_id: int, config: Dict[str, Any]):
        job = self.db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return
            
        job.status = "Running"
        self.db.commit()
        
        try:
            # Setup redactor
            redactor = TextRedactor(mode=job.redaction_mode)
            
            files = self.db.query(File).filter(File.job_id == job.id).all()
            total_entities = 0
            
            for file_record in files:
                try:
                    start_time = time.time()
                    
                    # 1. Parse file
                    parse_result = self.file_router.route_file(file_record.stored_input_path)
                    text = parse_result.get("text", "")
                    
                    # 2. Detect PII
                    regex_entities = self.regex_engine.detect(text)
                    nlp_entities = self.nlp_engine.detect(text)
                    
                    # 3. Merge entities
                    merged_entities = self.merge_engine.merge(regex_entities, nlp_entities)
                    
                    # 4. Filter by confidence and categories
                    confidence_threshold = job.confidence_threshold or 0.0
                    selected_categories = config.get("pii_categories", [])
                    
                    filtered_entities = [
                        ent for ent in merged_entities 
                        if ent['confidence_score'] >= confidence_threshold
                        and (not selected_categories or ent['entity_type'] in selected_categories)
                    ]
                    
                    # 5. Risk classification
                    for ent in filtered_entities:
                        ent['risk_level'] = self.risk_classifier.classify_entity(ent)
                        
                    file_record.risk_level = self.risk_classifier.classify_file(filtered_entities)
                    
                    # 6. Redaction
                    if file_record.file_type in ['.png', '.jpg', '.jpeg']:
                        # Image redaction
                        output_filename = f"redacted_{file_record.file_uuid}{os.path.splitext(file_record.original_filename)[1]}"
                        output_path = str(settings.OUTPUT_DIR / output_filename)
                        self.image_redactor.redact(file_record.stored_input_path, parse_result.get("boxes", []), output_path)
                        file_record.stored_output_path = output_path
                        file_record.ocr_applied = True
                    else:
                        # Text redaction
                        redacted_text = redactor.redact(text, filtered_entities)
                        output_filename = f"redacted_{file_record.file_uuid}{os.path.splitext(file_record.original_filename)[1]}"
                        output_path = str(settings.OUTPUT_DIR / output_filename)
                        with open(output_path, 'w', encoding='utf-8') as f:
                            f.write(redacted_text)
                        file_record.stored_output_path = output_path
                    
                    # 7. Save entities to DB
                    for ent_data in filtered_entities:
                        entity = Entity(
                            file_id=file_record.id,
                            entity_text=ent_data['entity_text'],
                            entity_type=ent_data['entity_type'],
                            source=ent_data['source'],
                            start_char=ent_data['start_char'],
                            end_char=ent_data['end_char'],
                            confidence_score=ent_data['confidence_score'],
                            risk_level=ent_data['risk_level'],
                            replacement_text=ent_data.get('replacement_text')
                        )
                        self.db.add(entity)
                    
                    file_record.entity_count = len(filtered_entities)
                    file_record.processing_time_ms = int((time.time() - start_time) * 1000)
                    file_record.status = "Success"
                    total_entities += len(filtered_entities)
                    
                    # Update job progress
                    job.processed_files += 1
                    self.db.commit()
                    
                except Exception as e:
                    file_record.status = "Failed"
                    file_record.error_message = str(e)
                    self.db.commit()
                    self.log_event(job.id, "ERROR", "File Processing", f"Error processing {file_record.original_filename}: {str(e)}", file_id=file_record.id)
            
            # Finalize job
            job.status = "Completed"
            job.completed_at = datetime.utcnow()
            job.total_entities_detected = total_entities
            self.db.commit()
            self.log_event(job.id, "INFO", "Job Completion", f"Job {job.job_uuid} completed successfully.")
            
        except Exception as e:
            job.status = "Failed"
            job.error_message = str(e)
            self.db.commit()
            self.log_event(job.id, "ERROR", "Job Execution", f"Critical job error: {str(e)}")

    def log_event(self, job_id: int, level: str, event_type: str, message: str, file_id: Optional[int] = None):
        log = AuditLog(
            job_id=job_id,
            file_id=file_id,
            log_level=level,
            event_type=event_type,
            message=message
        )
        self.db.add(log)
        self.db.commit()
