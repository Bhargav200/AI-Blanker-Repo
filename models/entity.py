from sqlalchemy import Column, Integer, String, Float, Boolean, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database.db import Base
import uuid

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    file_uuid = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    original_filename = Column(String)
    stored_input_path = Column(String)
    visual_input_path = Column(String, nullable=True)
    stored_output_path = Column(String, nullable=True)
    visual_output_path = Column(String, nullable=True)
    file_type = Column(String)
    file_size_bytes = Column(Integer)
    entity_count = Column(Integer, default=0)
    high_risk_count = Column(Integer, default=0)
    medium_risk_count = Column(Integer, default=0)
    low_risk_count = Column(Integer, default=0)
    average_confidence = Column(Float, default=0.0)
    risk_level = Column(String, default="Low")
    ocr_applied = Column(Boolean, default=False)
    raw_content = Column(String, nullable=True)
    redacted_content = Column(String, nullable=True)
    processing_time_ms = Column(Integer, default=0)
    status = Column(String, default="Success") # Success / Failed
    error_message = Column(String, nullable=True)

    job = relationship("Job", back_populates="files")
    entities = relationship("Entity", back_populates="file")
    file_report = relationship("FileReport", back_populates="file", uselist=False)

class Entity(Base):
    __tablename__ = "entities"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("files.id"))
    entity_text = Column(String)
    entity_type = Column(String) # EMAIL, PHONE, PERSON, etc.
    source = Column(String) # Regex / NLP
    start_char = Column(Integer)
    end_char = Column(Integer)
    confidence_score = Column(Float)
    risk_level = Column(String)
    is_redacted = Column(Boolean, default=True)
    replacement_text = Column(String, nullable=True)
    bounding_box_json = Column(JSON, nullable=True) # For images
    created_at = Column(DateTime, default=datetime.utcnow)

    file = relationship("File", back_populates="entities")

class PseudonymMapping(Base):
    __tablename__ = "pseudonym_mappings"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    original_value = Column(String)
    entity_type = Column(String)
    replacement_value = Column(String)

    job = relationship("Job", back_populates="pseudonym_mappings")
