import os
import shutil
import uuid
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File as FastAPIFile, BackgroundTasks, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database.db import get_db, Base, engine
from models.job import Job, AuditLog
from models.entity import File as FileModel, Entity, PseudonymMapping
from models.report import BatchReport, FileReport, ComplianceSummary, EvaluationRun
from core.job_orchestrator import JobOrchestrator
from config.settings import settings
from pydantic import BaseModel

app = FastAPI(title=settings.APP_NAME)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Schemas
class JobConfig(BaseModel):
    redaction_mode: str = "Mask"
    confidence_threshold: float = 0.5
    compliance_profile: str = "Default"
    language_hint: str = "English"
    pii_categories: List[str] = []

class JobCreate(BaseModel):
    config: JobConfig

@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.APP_NAME} API"}

@app.post("/jobs/create")
async def create_job(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = FastAPIFile(...), 
    redaction_mode: str = "Mask",
    confidence_threshold: float = 0.5,
    compliance_profile: str = "Default",
    language_hint: str = "English",
    pii_categories: str = "[]", # JSON string for pii_categories
    db: Session = Depends(get_db)
):
    import json
    try:
        pii_categories_list = json.loads(pii_categories)
    except:
        pii_categories_list = []
        
    config = {
        "redaction_mode": redaction_mode,
        "confidence_threshold": confidence_threshold,
        "compliance_profile": compliance_profile,
        "language_hint": language_hint,
        "pii_categories": pii_categories_list
    }
    
    # 1. Create Job record
    job = Job(
        redaction_mode=redaction_mode,
        confidence_threshold=confidence_threshold,
        compliance_profile=compliance_profile,
        language_hint=language_hint,
        config_json=config,
        total_files=len(files)
    )
    db.add(job)
    db.flush() # Get job.id
    
    # 2. Save uploaded files
    for file in files:
        file_uuid = str(uuid.uuid4())
        file_ext = os.path.splitext(file.filename)[1]
        stored_filename = f"{file_uuid}{file_ext}"
        input_path = settings.INPUT_DIR / stored_filename
        
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        file_record = FileModel(
            job_id=job.id,
            file_uuid=file_uuid,
            original_filename=file.filename,
            stored_input_path=str(input_path),
            file_type=file_ext,
            file_size_bytes=os.path.getsize(input_path)
        )
        db.add(file_record)
        
    db.commit()
    
    # 3. Trigger job in background
    orchestrator = JobOrchestrator(db)
    background_tasks.add_task(orchestrator.run_job, job.id, config)
    
    return {"job_id": job.id, "job_uuid": job.job_uuid, "status": "Pending"}

@app.get("/jobs/{job_id}")
def get_job_status(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    files = db.query(FileModel).filter(FileModel.job_id == job.id).all()
    
    return {
        "job_id": job.id,
        "job_uuid": job.job_uuid,
        "status": job.status,
        "total_files": job.total_files,
        "processed_files": job.processed_files,
        "total_entities_detected": job.total_entities_detected,
        "files": [
            {
                "id": f.id,
                "filename": f.original_filename,
                "status": f.status,
                "entity_count": f.entity_count,
                "risk_level": f.risk_level
            } for f in files
        ]
    }

@app.get("/files/{file_id}")
def get_file_details(file_id: int, db: Session = Depends(get_db)):
    file_record = db.query(FileModel).filter(FileModel.id == file_id).first()
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")
        
    entities = db.query(Entity).filter(Entity.file_id == file_id).all()
    
    return {
        "file_id": file_record.id,
        "filename": file_record.original_filename,
        "file_type": file_record.file_type,
        "risk_level": file_record.risk_level,
        "entity_count": file_record.entity_count,
        "entities": [
            {
                "text": e.entity_text,
                "type": e.entity_type,
                "confidence": e.confidence_score,
                "risk_level": e.risk_level,
                "replacement": e.replacement_text
            } for e in entities
        ]
    }

from core.evaluation.metrics import EvaluationMetrics
from core.compliance.mapper import ComplianceMapper

@app.get("/jobs/{job_id}/compliance")
def get_job_compliance(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    mapper = ComplianceMapper()
    summary = mapper.get_summary(job.compliance_profile)
    return summary

@app.get("/evaluation/metrics")
def get_evaluation_metrics():
    eval_metrics = EvaluationMetrics()
    # In a real scenario, this would compare against ground truth
    # For MVP, we return calculated metrics from the module
    return eval_metrics.calculate([], [])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
