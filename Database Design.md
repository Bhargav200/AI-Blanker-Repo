Overview
The database supports:
Job lifecycle tracking


File-level metadata storage


Entity-level detection storage


Configuration versioning


Risk classification


Reporting and analytics


Evaluation metrics storage


Audit logging


The design follows a job-centric model, where each redaction run creates a Job record, and all associated files, entities, and reports are linked to that Job.

1. Table: jobs
Purpose
The jobs table stores metadata about each redaction run.
 Each time the user initiates processing (single file or batch), a new job record is created.
This table acts as the parent entity for the entire processing lifecycle.

Columns
id (INTEGER, PRIMARY KEY, AUTOINCREMENT)


job_uuid (TEXT, UNIQUE)


created_at (DATETIME)


completed_at (DATETIME)


status (TEXT) — Pending, Running, Completed, Failed


total_files (INTEGER)


processed_files (INTEGER)


total_entities_detected (INTEGER)


high_risk_count (INTEGER)


medium_risk_count (INTEGER)


low_risk_count (INTEGER)


average_confidence (REAL)


redaction_mode (TEXT)


confidence_threshold (REAL)


compliance_profile (TEXT)


language_hint (TEXT)


config_json (TEXT) — full serialized config snapshot


error_message (TEXT, NULLABLE)



Relationships
One job → Many files


One job → Many audit_logs


One job → One batch_report



2. Table: files
Purpose
The files table stores metadata for every file processed within a job.
Each record represents one uploaded file (TXT, CSV, JSON, PDF, DOCX, PNG, JPG).

Columns
id (INTEGER, PRIMARY KEY, AUTOINCREMENT)


job_id (INTEGER, FOREIGN KEY → jobs.id)


file_uuid (TEXT, UNIQUE)


original_filename (TEXT)


stored_input_path (TEXT)


stored_output_path (TEXT)


file_type (TEXT)


file_size_bytes (INTEGER)


entity_count (INTEGER)


high_risk_count (INTEGER)


medium_risk_count (INTEGER)


low_risk_count (INTEGER)


average_confidence (REAL)


risk_level (TEXT)


ocr_applied (BOOLEAN)


processing_time_ms (INTEGER)


status (TEXT) — Success / Failed


error_message (TEXT, NULLABLE)



Relationships
Many files → One job


One file → Many entities


One file → One file_report



3. Table: entities
Purpose
The entities table stores every detected PII entity for each file.
This table enables:
Entity-level review in UI


Heatmap visualization


Confidence analysis


Evaluation comparisons



Columns
id (INTEGER, PRIMARY KEY, AUTOINCREMENT)


file_id (INTEGER, FOREIGN KEY → files.id)


entity_text (TEXT)


entity_type (TEXT) — EMAIL, PHONE, PERSON, etc.


source (TEXT) — Regex / NLP


start_char (INTEGER)


end_char (INTEGER)


confidence_score (REAL)


risk_level (TEXT)


is_redacted (BOOLEAN)


replacement_text (TEXT)


bounding_box_json (TEXT, NULLABLE) — For images


created_at (DATETIME)



Relationships
Many entities → One file



4. Table: batch_reports
Purpose
Stores summary statistics at job level for dashboard display and export.
This avoids recalculating metrics repeatedly.

Columns
id (INTEGER, PRIMARY KEY, AUTOINCREMENT)


job_id (INTEGER, FOREIGN KEY → jobs.id)


total_files (INTEGER)


total_entities (INTEGER)


entity_distribution_json (TEXT)


confidence_distribution_json (TEXT)


overall_risk_level (TEXT)


report_generated_at (DATETIME)



5. Table: file_reports
Purpose
Stores summary metrics per file for quick dashboard retrieval.

Columns
id (INTEGER, PRIMARY KEY, AUTOINCREMENT)


file_id (INTEGER, FOREIGN KEY → files.id)


entity_count (INTEGER)


entity_distribution_json (TEXT)


average_confidence (REAL)


risk_level (TEXT)


report_generated_at (DATETIME)



6. Table: audit_logs
Purpose
Stores structured logs for compliance and traceability.
Each action in a job lifecycle may create log entries.

Columns
id (INTEGER, PRIMARY KEY, AUTOINCREMENT)


job_id (INTEGER, FOREIGN KEY → jobs.id)


file_id (INTEGER, NULLABLE)


log_level (TEXT) — INFO, WARNING, ERROR


event_type (TEXT)


message (TEXT)


metadata_json (TEXT)


created_at (DATETIME)



7. Table: pseudonym_mappings
Purpose
Maintains consistent pseudonymization across documents.
Ensures:
 John Smith → PERSON_001 consistently across file or job.

Columns
id (INTEGER, PRIMARY KEY, AUTOINCREMENT)


job_id (INTEGER, FOREIGN KEY → jobs.id)


original_value (TEXT)


entity_type (TEXT)


replacement_value (TEXT)



8. Table: evaluation_runs
Purpose
Stores results from offline evaluation script.
Each evaluation run corresponds to a dataset benchmark.

Columns
id (INTEGER, PRIMARY KEY, AUTOINCREMENT)


run_name (TEXT)


dataset_name (TEXT)


precision (REAL)


recall (REAL)


f1_score (REAL)


confusion_matrix_json (TEXT)


entity_metrics_json (TEXT)


evaluated_at (DATETIME)



9. Table: compliance_summaries
Purpose
Stores compliance report metadata for export.
Allows regeneration without recomputing everything.

Columns
id (INTEGER, PRIMARY KEY, AUTOINCREMENT)


job_id (INTEGER, FOREIGN KEY → jobs.id)


profile_name (TEXT)


compliance_mapping_json (TEXT)


generated_at (DATETIME)



Key Relationships Overview
jobs → files (1:N)


files → entities (1:N)


jobs → batch_reports (1:1)


files → file_reports (1:1)


jobs → audit_logs (1:N)


jobs → pseudonym_mappings (1:N)


jobs → compliance_summaries (1:1)


evaluation_runs (standalone table)



Indexing Recommendations (SQLite)
To ensure performance:
Create indexes on:
jobs.job_uuid


files.job_id


entities.file_id


entities.entity_type


entities.confidence_score


audit_logs.job_id

