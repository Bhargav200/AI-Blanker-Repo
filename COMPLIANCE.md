# Privacy Compliance Documentation

## AI PII Redactor for Public Datasets

### Overview
This document outlines how the AI PII Redactor ensures data privacy compliance according to major global regulations like GDPR, HIPAA, and India's DPDP Act.

### 1. Core Privacy Principles Implemented
- **Data Minimization**: The tool automatically identifies and removes personal data that is not necessary for the intended purpose (e.g., training AI models).
- **Anonymization & Pseudonymization**: Supports multiple redaction modes, including deterministic pseudonymization, allowing data to be used for research without identifying individuals.
- **Storage Limitation**: Input and output files are handled securely with configurable retention policies (manual or automated).
- **Integrity & Confidentiality**: All processing is done locally or in a secure environment, ensuring data does not leak to public clouds before redaction.

### 2. Compliance Mapping

| Principle | System Feature | Implementation Status |
|-----------|----------------|-----------------------|
| Right to Privacy | PII Detection & Redaction | Fully Implemented |
| De-identification | Masking, Labeling, Pseudonymization | Fully Implemented |
| Auditability | Structured JSON Audit Logs | Fully Implemented |
| Accountability | Detailed Job History & Reporting | Fully Implemented |

### 3. Regulatory Support
- **GDPR (EU)**: Ensures "Privacy by Design" by sanitizing datasets before they enter the processing pipeline.
- **HIPAA (US)**: Supports the "Safe Harbor" method by detecting and redacting the 18 specific PHI identifiers.
- **DPDP (India)**: Aligns with the Digital Personal Data Protection Act by providing clear logs and consent-ready sanitized data.

### 4. Technical Safeguards
- **Hybrid Engine**: Combines high-precision Regex with contextual NLP to minimize False Negatives (missed PII).
- **OCR Security**: Processes images locally to extract and redact text without cloud-based OCR APIs.
- **Deterministic Pseudonyms**: Ensures that the same individual is assigned the same pseudonym across a dataset, maintaining data utility while protecting identity.
