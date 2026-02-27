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
from fastapi.staticfiles import StaticFiles

app = FastAPI(title=settings.APP_NAME)

# Mount storage for direct access (optional but helpful)
app.mount("/storage", StaticFiles(directory=str(settings.BASE_DIR / "storage")), name="storage")

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
    from database.db import SessionLocal
    def run_job_wrapper(job_id, config):
        db_job = SessionLocal()
        try:
            orchestrator = JobOrchestrator(db_job)
            orchestrator.run_job(job_id, config)
        finally:
            db_job.close()

    background_tasks.add_task(run_job_wrapper, job.id, config)
    
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
                "file_type": f.file_type,
                "status": f.status,
                "entity_count": f.entity_count,
                "risk_level": f.risk_level
            } for f in files
        ]
    }

from fastapi.responses import FileResponse

@app.get("/files/{file_id}/download/original")
def download_original(file_id: int, db: Session = Depends(get_db)):
    file_record = db.query(FileModel).filter(FileModel.id == file_id).first()
    if not file_record or not os.path.exists(file_record.stored_input_path):
        raise HTTPException(status_code=404, detail="Original file not found")
    
    # Determine media type
    ext = os.path.splitext(file_record.original_filename)[1].lower()
    media_type = "application/octet-stream"
    if ext in ['.png', '.jpg', '.jpeg']:
        media_type = f"image/{ext[1:]}"
    elif ext == '.pdf':
        media_type = "application/pdf"
        
    return FileResponse(file_record.stored_input_path, filename=file_record.original_filename, media_type=media_type)

@app.get("/files/{file_id}/download/redacted")
def download_redacted(file_id: int, db: Session = Depends(get_db)):
    file_record = db.query(FileModel).filter(FileModel.id == file_id).first()
    if not file_record or not file_record.stored_output_path or not os.path.exists(file_record.stored_output_path):
        raise HTTPException(status_code=404, detail="Redacted file not found")
    
    ext = os.path.splitext(file_record.original_filename)[1]
    filename = f"redacted_{file_record.original_filename}"
    return FileResponse(file_record.stored_output_path, filename=filename)

@app.get("/files/{file_id}/visual")
def get_visual_redacted(file_id: int, db: Session = Depends(get_db)):
    file_record = db.query(FileModel).filter(FileModel.id == file_id).first()
    if not file_record or not file_record.visual_output_path or not os.path.exists(file_record.visual_output_path):
        raise HTTPException(status_code=404, detail="Visual preview not found")
    return FileResponse(file_record.visual_output_path, media_type="image/png")

@app.get("/files/{file_id}/visual-original")
def get_visual_original(file_id: int, db: Session = Depends(get_db)):
    file_record = db.query(FileModel).filter(FileModel.id == file_id).first()
    if not file_record or not file_record.visual_input_path or not os.path.exists(file_record.visual_input_path):
        raise HTTPException(status_code=404, detail="Original visual preview not found")
    
    # Determine media type based on the file stored at visual_input_path
    ext = os.path.splitext(file_record.visual_input_path)[1].lower()
    media_type = "image/png"
    if ext in ['.jpg', '.jpeg']:
        media_type = "image/jpeg"
        
    return FileResponse(file_record.visual_input_path, media_type=media_type)

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
        "raw_content": file_record.raw_content,
        "redacted_content": file_record.redacted_content,
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
