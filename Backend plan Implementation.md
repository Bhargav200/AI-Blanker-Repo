PHASE 1 — Project Foundation Setup

1️⃣ Create Project Structure
Create the following directory layout:
pii_redactor/
│
├── core/
│   ├── file_router.py
│   ├── parser/
│   ├── ocr/
│   ├── detection/
│   ├── redaction/
│   ├── scoring/
│   ├── compliance/
│   ├── evaluation/
│   └── utils/
│
├── models/
│   ├── entity.py
│   ├── job.py
│   └── report.py
│
├── database/
│   ├── db.py
│   └── schema.sql
│
├── storage/
│   ├── input/
│   ├── output/
│   ├── logs/
│   └── temp/
│
├── config/
│   └── settings.py
│
└── main.py
Checklist:
Folder structure created


Virtual environment configured


Requirements file prepared



2️⃣ Install Dependencies
Core:
spaCy + transformer model


Tesseract


pytesseract


OpenCV


pandas


python-docx


PyMuPDF or pdfplumber


faker


scikit-learn


sqlite3 (built-in)


Checklist:
spaCy model downloaded


Tesseract installed and verified


All imports validated



✅ PHASE 2 — Database Layer (SQLite)

3️⃣ Define Database Schema
Tables:
jobs
id


created_at


status


total_files


total_entities


risk_level


config_json


files
id


job_id


filename


file_type


entity_count


risk_level


entities
id


file_id


entity_text


entity_type


confidence


source


start_pos


end_pos


Checklist:
schema.sql created


SQLite file initialized


DB connection module implemented


CRUD helpers created



✅ PHASE 3 — File Ingestion Layer

4️⃣ Implement File Router
Function:
route_file(file_path)
Logic:
Detect extension


Call appropriate parser


Return standardized text + metadata


Checklist:
Extension detection


Error handling for unsupported formats


Unit tests for each type



5️⃣ Implement Parsers
TXT
Read raw text


CSV
Use pandas


Extract cell-level text


Preserve structure metadata


JSON
Recursive traversal


Capture full path for each string value


PDF
Text extraction


DOCX
Paragraph + table extraction


Checklist:
Unified return format:


{
 "text": "...",
 "structure": metadata_object
}

✅ PHASE 4 — OCR Module

6️⃣ Build OCR Pipeline
Steps:
Load image


Apply grayscale


Noise reduction


Skew correction (basic)


Run pytesseract


Capture bounding boxes


Return:
{
 "text": "...",
 "boxes": [...]
}
Edge cases:
Empty image


Low confidence



✅ PHASE 5 — Detection Engine

7️⃣ Regex Detection Module
Implement patterns for:
Email


Phone


SSN


Credit card


IP address


Bank account


Passport


Driver license


Features:
Custom regex input


Regex safety validation


Return list of Entity objects.

8️⃣ NLP Detection Module
Load spaCy transformer


Detect PERSON, ORG, GPE, DATE


Extract span positions


Assign base confidence



9️⃣ Hybrid Merge Engine
Steps:
Combine regex + NLP results


Sort by start position


Remove overlapping spans


Deduplicate identical spans


Attach source label


Assign confidence


Edge case handling:
Nested entities


Partial overlaps



✅ PHASE 6 — Confidence & Risk Scoring

🔟 Confidence Scoring
Implement:
Base score (Regex = high default)


NLP probability score


Penalty for OCR text


Final weighted score


Checklist:
Threshold filtering implemented


Score attached to each entity



1️⃣1️⃣ Risk Classification
Logic:
High if SSN/credit card


Medium if name + location


Low if single date


Attach risk level to:
File


Job



✅ PHASE 7 — Redaction Engine

1️⃣2️⃣ Text Redaction
Implement modes:
Mask mode


Label mode


Pseudonym mode


Synthetic mode


Ensure:
Reverse sorting before replacement


No offset corruption


CSV/JSON structure preserved



1️⃣3️⃣ Pseudonym Mapping Engine
Create mapping dictionary


Maintain consistency


Optional cross-file consistency



1️⃣4️⃣ Synthetic Replacement
Integrate Faker


Match entity type


Preserve realistic formatting



1️⃣5️⃣ Image Redaction Rendering
If enabled:
Draw black boxes on bounding boxes


Save redacted image



✅ PHASE 8 — Output Generation

1️⃣6️⃣ Save Redacted Files
Maintain folder structure


Append _redacted


Preserve CSV/JSON formatting



1️⃣7️⃣ Generate Reports
Per-file report:
Entity count


Breakdown


Average confidence


Risk level


Batch report:
Total entities


Distribution


Summary metrics



1️⃣8️⃣ JSON Audit Log
Serialize job + file + entity data


Save structured JSON



1️⃣9️⃣ Compliance Summary Generator
Generate:
Feature mapping table


Risk coverage summary


Output as PDF or text file



✅ PHASE 9 — Evaluation Module

2️⃣0️⃣ Offline Evaluation Script
Input:
Labeled dataset


Ground truth JSON


Process:
Compare predicted vs actual


Compute:


Precision


Recall


F1


Confusion matrix


Save evaluation report


Export CSV summary



✅ PHASE 10 — Main Job Controller

2️⃣1️⃣ Job Orchestrator
Create central function:
run_redaction_job(config, file_list)
Flow:
Create DB job entry


Parse files


OCR (if needed)


Detect PII


Score


Redact


Save output


Save DB records


Generate reports


Update job status



✅ PHASE 11 — Logging & Error Handling

2️⃣2️⃣ Structured Logging
Log start/end time


Log entity counts


Log errors


Save logs to storage/logs



2️⃣3️⃣ Exception Handling
Unsupported file


Corrupted PDF


OCR failure


Regex failure


System should:
Continue processing other files


Mark failed file status



✅ PHASE 12 — Integration with UI

2️⃣4️⃣ Create Public Interface Layer
Expose:
start_job(config, file_paths)
get_job_summary(job_id)
get_file_details(file_id)
export_results(job_id)
UI should never call lower-level modules directly.

✅ PHASE 13 — Final Validation Checklist
Before launch:
Test single file processing


Test batch processing


Test all redaction modes


Test image OCR flow


Test threshold filtering


Validate DB entries


Validate audit logs


Run evaluation script


Test edge cases


Validate large file handling

