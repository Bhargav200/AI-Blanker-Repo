from database.db import Base, engine
from models.job import Job, AuditLog
from models.entity import File, Entity, PseudonymMapping
from models.report import BatchReport, FileReport, ComplianceSummary, EvaluationRun

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()
