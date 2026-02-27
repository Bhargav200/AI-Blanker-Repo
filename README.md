# AI PII Redactor for Public Datasets

An end-to-end, multi-format AI-powered PII detection and redaction system.

## Features
- Support for TXT, CSV, JSON, PDF, DOCX, PNG, JPG.
- Hybrid Detection (Regex + spaCy NLP).
- Multiple Redaction Modes (Mask, Label, Pseudonym, Synthetic).
- Compliance reporting (GDPR, HIPAA, DPDP).
- REST API and Streamlit UI.

## Prerequisites
- Python 3.10+
- Tesseract OCR (for image support)
  - Windows: [Download Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
  - Update `TESSERACT_CMD` in `.env` if not in default path.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Download spaCy model:
   ```bash
   python -m spacy download en_core_web_sm
   # Or for better accuracy:
   python -m spacy download en_core_web_trf
   ```
3. Initialize database:
   ```bash
   python database/init_db.py
   ```

## Running the App
Start both backend and frontend:
```bash
python start.py
```
- Backend: http://localhost:8000
- Frontend: http://localhost:8501

## Project Structure
- `core/`: Core logic (detection, redaction, parsing).
- `models/`: SQLAlchemy models.
- `database/`: DB connection and initialization.
- `storage/`: Input/Output file storage.
- `main.py`: FastAPI application.
- `app.py`: Streamlit application.
