from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database.db import Base

class BatchReport(Base):
    __tablename__ = "batch_reports"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    total_files = Column(Integer)
    total_entities = Column(Integer)
    entity_distribution_json = Column(JSON)
    confidence_distribution_json = Column(JSON)
    overall_risk_level = Column(String)
    report_generated_at = Column(DateTime, default=datetime.utcnow)

    job = relationship("Job", back_populates="batch_report")

class FileReport(Base):
    __tablename__ = "file_reports"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("files.id"))
    entity_count = Column(Integer)
    entity_distribution_json = Column(JSON)
    average_confidence = Column(Float)
    risk_level = Column(String)
    report_generated_at = Column(DateTime, default=datetime.utcnow)

    file = relationship("File", back_populates="file_report")

class ComplianceSummary(Base):
    __tablename__ = "compliance_summaries"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    profile_name = Column(String)
    compliance_mapping_json = Column(JSON)
    generated_at = Column(DateTime, default=datetime.utcnow)

    job = relationship("Job", back_populates="compliance_summary")

class EvaluationRun(Base):
    __tablename__ = "evaluation_runs"

    id = Column(Integer, primary_key=True, index=True)
    run_name = Column(String)
    dataset_name = Column(String)
    precision = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)
    confusion_matrix_json = Column(JSON)
    entity_metrics_json = Column(JSON)
    evaluated_at = Column(DateTime, default=datetime.utcnow)
