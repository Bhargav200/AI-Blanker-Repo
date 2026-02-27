# Product Requirements Document (PRD)

# AI PII Redactor for Public Datasets

Category: Privacy & Compliance Automation
Tech Stack: Python, NLP, OCR, Regex

---

# 1. Product Overview

## Product Name

AI PII Redactor for Public Datasets

## Vision

Enable organizations, researchers, and data teams to safely publish, share, or use datasets for AI/LLM training by automatically detecting and redacting Personally Identifiable Information (PII) in text and image-based documents.

## Core Value Proposition

Upload any dataset → Automatically detect sensitive data → Apply configurable redaction → Generate compliance-ready sanitized output and audit report.

---

# 2. Problem Statement

Public datasets frequently contain hidden PII such as:

* Names
* Emails
* Phone numbers
* Addresses
* National IDs
* IP addresses
* Financial details

When such data is:

* Uploaded to public clouds
* Shared with third parties
* Used to train Large Language Models
* Published as open datasets

It creates:

* Regulatory violations (GDPR, HIPAA, DPDP, etc.)
* Legal exposure
* Reputational damage
* Ethical risks

Current challenges:

* Manual redaction is slow and inconsistent.
* Simple regex tools miss contextual entities.
* NLP-only tools miss structured identifiers.
* Image-based datasets require OCR before detection.
* No unified tool supports text + image + compliance reporting.

There is a need for a hybrid, automated, compliance-ready redaction system that protects privacy before data leaves secure environments.

---

# 3. Goals & Non-Goals

## 3.1 Goals

* Detect PII in text documents and images
* Support TXT, CSV, JSON, PDF, DOCX, PNG, JPG
* Use hybrid detection (Regex + NLP)
* Integrate OCR for image-based inputs
* Automatically redact or anonymize PII
* Generate structured redacted outputs
* Provide redaction accuracy reporting
* Produce compliance-ready documentation
* Support LLM training data privacy
* Provide batch processing capability
* Ensure reproducible and auditable redaction

## 3.2 Non-Goals

* Real-time streaming redaction
* Legal certification of compliance
* Full enterprise RBAC system (MVP)
* Cloud-native distributed processing (MVP)
* Custom model training (MVP)

---

# 4. Target Users

| Persona                | Description                            | Primary Need              |
| ---------------------- | -------------------------------------- | ------------------------- |
| Data Scientists        | Preparing datasets for ML/LLM training | Clean training data       |
| Research Labs          | Publishing open datasets               | Public release compliance |
| Enterprises            | Sharing internal datasets              | Risk mitigation           |
| Legal/Compliance Teams | Reviewing data exposure                | Audit trail               |
| Government Agencies    | Releasing public records               | Privacy protection        |

---

# 5. Functional Requirements

## 5.1 Input & File Support

FR-1
System must accept:

* TXT
* CSV
* JSON
* PDF
* DOCX
* PNG
* JPG

FR-2
Support:

* Single file upload
* Batch upload
* Folder-based processing
* CLI
* Web dashboard
* REST API

FR-3
System must validate:

* File type
* File size
* Encoding

---

## 5.2 File Routing & Preprocessing

FR-4
System must route files by type:

| File Type    | Action             |
| ------------ | ------------------ |
| TXT/CSV/JSON | Direct parsing     |
| PDF          | Text extraction    |
| DOCX         | Structured parsing |
| PNG/JPG      | OCR processing     |

FR-5
OCR pipeline must:

* Preprocess image
* Remove noise
* Correct skew
* Extract text
* Preserve bounding box coordinates

---

## 5.3 PII Detection Engine

FR-6
Hybrid Detection:

### A. Regex Layer (High Precision)

Detect:

* Emails
* Phone numbers
* SSN
* Credit cards
* IP addresses
* Passport numbers (basic pattern)
* Bank numbers (basic pattern)

### B. NLP Layer (Contextual Detection)

Using spaCy transformer:

Detect:

* PERSON
* ORG
* GPE (locations)
* DATE

FR-7
Merge Engine must:

* Remove overlapping detections
* Deduplicate entities
* Assign confidence score
* Attach metadata:

  * Entity type
  * Location
  * Detection source
  * Confidence score

---

## 5.4 Redaction & Anonymization

FR-8
System must support redaction modes:

1. Mask Mode
   Replace with [REDACTED]

2. Label Mode
   Replace with [PERSON], [EMAIL], etc.

3. Pseudonym Mode
   Deterministic mapping (e.g., PERSON_001)

4. Synthetic Mode
   Replace with realistic synthetic data

FR-9
Redaction must:

* Preserve original document structure
* Maintain CSV schema
* Maintain JSON keys
* Preserve DOCX tables
* Preserve PDF formatting (best effort)
* Maintain consistency across document

---

## 5.5 Compliance Profiles

FR-10
System must support compliance modes:

* Default
* GDPR Mode
* HIPAA Mode
* DPDP Mode (India)

FR-11
Compliance profile must:

* Adjust severity scoring
* Flag regulated identifiers
* Generate compliance summary mapping

---

## 5.6 Reporting & Deliverables

FR-12
Per-file Detection Report must include:

* File name
* Timestamp
* Total PII detected
* Entity breakdown by type
* Confidence averages
* Risk score

FR-13
Batch Summary must include:

* Total files processed
* Total PII detected
* Most common entity type
* Compliance overview

FR-14
Accuracy Evaluation (Test Mode)

If labeled dataset provided:

* Precision
* Recall
* F1 Score
* Confusion matrix

FR-15
Structured Logs:

* JSON audit logs
* Detection metadata
* Redaction trace

FR-16
Privacy Compliance Summary:

* Data minimization statement
* Pseudonymization explanation
* Logging confirmation
* GDPR/DPDP/HIPAA alignment mapping

---

# 6. Non-Functional Requirements

## 6.1 Performance Targets

| Metric                   | Target        |
| ------------------------ | ------------- |
| Text processing speed    | < 10s per MB  |
| OCR latency              | < 5s per page |
| Structured PII precision | ≥ 90%         |
| Structured PII recall    | ≥ 85%         |
| Batch completion rate    | ≥ 95%         |

---

## 6.2 Reliability

* Tool failure must not crash entire batch
* Partial results must be returned
* Max retry logic (2 retries)
* Timeout protection

---

## 6.3 Security

* No hardcoded secrets
* Environment variable configuration
* Secure temporary file handling
* File size limits
* Path sanitization
* Structured error handling

---

## 6.4 Transparency

* Confidence scoring visible
* Entity metadata accessible
* Exportable audit logs
* Deterministic redaction trace

---

## 6.5 Modularity

Swappable components:

* Detection engine
* OCR engine
* Compliance rule sets
* UI layer
* Database layer

---

# 7. System Architecture

High-Level Flow:

User Upload
↓
File Router
↓
OCR (if required)
↓
Hybrid Detection Engine
↓
Merge & Confidence Scoring
↓
Redaction Engine
↓
Report Generator
↓
Compliance Mapper
↓
Structured Output + Audit Logs

---

# 8. Technical Architecture

## Recommended Stack

Backend:

* Python 3.11+
* FastAPI
* SQLAlchemy
* Pydantic

Detection:

* spaCy Transformer
* Python Regex

OCR:

* Tesseract
* Pillow

Parsing:

* pdfplumber
* python-docx
* pandas

CLI:

* Typer

UI:

* Streamlit

Database:

* PostgreSQL (MVP may use SQLite)

Logging:

* Structured JSON logs

---

# 9. Core Components

## 9.1 File Router

Determines pipeline path.

## 9.2 OCR Engine

Image preprocessing + bounding box extraction.

## 9.3 Hybrid Detection Engine

Regex + NLP entity extraction.

## 9.4 Merge & Scoring Layer

Confidence computation + overlap resolution.

## 9.5 Redaction Engine

Applies selected redaction strategy.

## 9.6 Compliance Engine

Maps findings to regulatory requirements.

## 9.7 Reporting Engine

Generates per-file + batch reports.

## 9.8 Dashboard

Displays:

* PII type distribution
* Entity counts
* Risk heatmap

---

# 10. Edge Case Handling

### 10.1 Poor OCR Quality

* Flag low-confidence areas
* Allow re-run

### 10.2 Overlapping Entities

* Prioritize higher confidence
* Log decision

### 10.3 No PII Found

* Return clean file
* State “No PII detected above threshold.”

### 10.4 Extremely Large Files

* Chunk processing
* Incremental logging

---

# 11. Evaluation Criteria

System will be evaluated on:

* Detection accuracy
* Redaction consistency
* Compliance documentation completeness
* Structure preservation
* Batch robustness
* Audit trace clarity

---

# 12. Deliverables (From Project Brief)

1. Working PII redaction tool
2. Text + image redaction demo
3. Redaction accuracy report
4. Privacy compliance documentation

---

# 13. Success Metrics

| Metric                          | Success Criteria |
| ------------------------------- | ---------------- |
| Precision                       | ≥ 90%            |
| Recall                          | ≥ 85%            |
| Compliance summary generation   | 100%             |
| Deterministic pseudonym mapping | 100%             |
| Audit log completeness          | 100%             |

---

# 14. Future Enhancements

* Multilingual NLP expansion
* Cloud-native distributed processing
* Role-based access control
* API authentication layer
* LLM dataset ingestion validation
* Real-time streaming support
* Active learning feedback loop

---

# User Experience Summary (One Sentence)

“Upload any dataset, automatically detect and redact sensitive personal information across text and images, and receive a compliance-ready sanitized output with a detailed audit report.”

