from sqlalchemy import Column, Integer, String, DateTime, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database.db import Base
import uuid

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_uuid = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    status = Column(String, default="Pending") # Pending, Running, Completed, Failed
    total_files = Column(Integer, default=0)
    processed_files = Column(Integer, default=0)
    total_entities_detected = Column(Integer, default=0)
    high_risk_count = Column(Integer, default=0)
    medium_risk_count = Column(Integer, default=0)
    low_risk_count = Column(Integer, default=0)
    average_confidence = Column(Float, default=0.0)
    redaction_mode = Column(String)
    confidence_threshold = Column(Float)
    compliance_profile = Column(String)
    language_hint = Column(String)
    config_json = Column(JSON, nullable=True)
    error_message = Column(String, nullable=True)

    files = relationship("File", back_populates="job")
    audit_logs = relationship("AuditLog", back_populates="job")
    batch_report = relationship("BatchReport", back_populates="job", uselist=False)
    pseudonym_mappings = relationship("PseudonymMapping", back_populates="job")
    compliance_summary = relationship("ComplianceSummary", back_populates="job", uselist=False)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    file_id = Column(Integer, nullable=True)
    log_level = Column(String) # INFO, WARNING, ERROR
    event_type = Column(String)
    message = Column(String)
    metadata_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    job = relationship("Job", back_populates="audit_logs")
