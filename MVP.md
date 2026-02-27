Product Overview – 1-Line Vision
An end-to-end, multi-format AI-powered PII detection and redaction system that automatically sanitizes text and image-based datasets while generating audit-ready compliance reports.

2️⃣ Finalized MVP Features (Phase 1 Scope)
Since you confirmed everything is included in MVP, this is the consolidated final feature set.

A. Multi-Format File Ingestion
Support for:
TXT


CSV


JSON


PDF (text-based)


DOCX


PNG


JPG


Capabilities:
Automatic file-type detection


Structured parsing


Folder-level ingestion (batch mode)



B. OCR Pipeline (Image Support)
Tesseract OCR integration


Basic preprocessing:


Noise removal


Skew correction


Extract text from PNG/JPG


Capture bounding box coordinates


Multi-language hint support (basic Hindi/Telugu mode)



C. Hybrid PII Detection Engine
1. Regex-Based Detection
Detect:
Emails


Phone numbers


SSN-like patterns


Credit card numbers


IP addresses


Bank accounts


Passport numbers


Driver licenses


Custom regex uploads


High precision structured detection.

2. NLP-Based Detection (spaCy Transformer)
Detect:
PERSON


ORG


GPE (Locations)


DATE


Context-based detection.

3. Hybrid Merge Layer
Combine Regex + NER results


Remove overlaps


Deduplicate entities


Attach metadata:


Entity type


Confidence score


Source (Regex / NLP)


Location in document



D. Confidence & Risk Scoring
Per-entity confidence score


Threshold-based filtering


Risk level classification (Low / Medium / High)


Confidence heatmap (visual overlay in dashboard)



E. Flexible Redaction Engine
Modes supported:
Mask Mode → [REDACTED]


Label Mode → [PERSON]


Pseudonym Mode → PERSON_001


Synthetic Replacement → Realistic fake data


Requirements:
Maintain consistency across document


Preserve CSV columns and JSON schema


Maintain DOCX/PDF structure (best effort)


Visual image masking (black box / blur)



F. Output Generation
System generates:
Redacted file (*_redacted.ext)


Detection report (per file)


Batch summary report


JSON audit log export


Accuracy report (if test dataset provided)


One-page compliance summary (GDPR / DPDP mapping)



G. Evaluation Module
On labeled dataset (50+ test files):
Precision


Recall


F1 Score


Confusion matrix



H. Interfaces
CLI interface


Web dashboard


REST API endpoint


Batch processing support



I. Dashboard & Visualization
Pie chart of entity types


Per-file entity counts


Confidence heatmap


Summary metrics



3️⃣ Detailed User Journey (End-to-End MVP Flow)

🟢 Step 1: User Access
User chooses entry mode:
CLI


Web UI


REST API



🟢 Step 2: File Upload / Selection
User:
Uploads one file


Or selects a folder (batch mode)


System:
Validates format


Displays file list


Shows size and count



🟢 Step 3: Configuration Panel
User selects:
Redaction Mode
Mask


Label


Pseudonym


Synthetic


PII Categories
Toggle:
Emails


Phones


SSNs


Credit cards


IPs


Names


Locations


Dates


Advanced PII


Confidence Threshold
0.50


0.75


0.90


Compliance Profile
Default


GDPR


HIPAA


DPDP


Language Hint
English


Hindi/Telugu assist mode



🟢 Step 4: Processing Pipeline Execution
System internally performs:
File parsing


OCR (if image)


Regex detection


NLP detection


Merge & deduplication


Confidence scoring


Risk classification


Redaction transformation


Output generation


Logging


Progress bar visible.

🟢 Step 5: Results Dashboard
User sees:
Total files processed


Total PII detected


Breakdown by entity type


Confidence distribution


Heatmap preview


Compliance summary



🟢 Step 6: Output Download
User downloads:
Redacted files


Detection reports


JSON audit logs


Accuracy report (if evaluation mode)


Compliance summary slide



🟢 Step 7: Optional Re-Run
User may:
Adjust threshold


Switch redaction mode


Toggle categories


Reprocess files



4️⃣ Edge Case Notes
Important edge cases to design for:

1. Overlapping Entities
Example:
 “John Smith from New York”
NER may detect:
PERSON: John Smith


GPE: New York


Ensure:
No double redaction


Proper offset recalculation



2. Nested JSON Structures
Deeply nested fields may contain PII.
Ensure:
Recursive parsing


Schema preservation



3. CSV Column Sensitivity
PII might appear in:
Column headers


Structured fields


Need:
Cell-level redaction


No column shift



4. OCR Misreads
Example:
O vs 0


l vs 1


Mitigation:
Post-OCR regex validation


Confidence filtering



5. False Positives
Example:
“May” detected as DATE


“Bill” detected as PERSON


Mitigation:
Confidence threshold


Allow user review option



6. Large Files
10MB+ PDFs or CSVs
Mitigation:
Stream processing


Memory optimization



7. Repeated Entities
Ensure consistent pseudonym mapping across entire file.

8. Multi-Language Names
Hindi/Telugu mixed with English.
Mitigation:
Extended regex patterns


Optional multilingual NER model in future phase



9. Image Without Text
Return:
“No detectable text found”



10. Custom Regex Conflicts
If user uploads custom regex:
Validate safely


Prevent catastrophic backtracking



5️⃣ Tech Stack

Backend
Python 3.10+


FastAPI (REST API)


spaCy (Transformer model)


HuggingFace (optional advanced models)


Tesseract OCR


OpenCV (image preprocessing)


pandas (CSV handling)


python-docx (DOCX parsing)


PyMuPDF / pdfplumber (PDF extraction)



Detection
Regex (Python re)


spaCy NER


Custom rule engine



Redaction & Replacement
Faker (synthetic data)


Custom mapping dictionary



Evaluation
scikit-learn (precision, recall, F1)


matplotlib / seaborn (charts)



Dashboard
Streamlit or React frontend


Plotly charts



Logging & Export
JSON structured logs


SQLite (optional metadata storage)



Deployment
Dockerized application


Local processing mode


Cloud-ready (AWS/GCP/Azure compatible)



🎯 Final MVP Definition (Clarity Statement)
At the end of Phase 1, we are building:
A production-grade, multi-format, AI-powered PII redaction system that:
Detects structured and contextual PII


Works on text and images


Supports multiple redaction strategies


Provides confidence scoring


Generates compliance-ready reports


Offers CLI, dashboard, and API access


Includes evaluation metrics and visualization

