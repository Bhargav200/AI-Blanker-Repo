from typing import Dict, Any, List

class ComplianceMapper:
    PROFILES = {
        "GDPR": {
            "name": "General Data Protection Regulation (GDPR)",
            "description": "Focuses on personal data protection for EU residents.",
            "mappings": [
                {"principle": "Data Minimization", "feature": "PII Detection & Redaction", "status": "Implemented"},
                {"principle": "Anonymization", "feature": "Pseudonymization Mode", "status": "Implemented"},
                {"principle": "Traceability", "feature": "Audit Logging", "status": "Implemented"}
            ]
        },
        "HIPAA": {
            "name": "Health Insurance Portability and Accountability Act (HIPAA)",
            "description": "Protects sensitive patient health information.",
            "mappings": [
                {"principle": "Safe Harbor Method", "feature": "18 PHI Identifiers Detection", "status": "Implemented"},
                {"principle": "Integrity", "feature": "Structure Preservation", "status": "Implemented"}
            ]
        },
        "DPDP": {
            "name": "Digital Personal Data Protection Act (DPDP - India)",
            "description": "Data protection framework for India.",
            "mappings": [
                {"principle": "Lawful Processing", "feature": "Consent-based Redaction", "status": "Implemented"},
                {"principle": "Storage Limitation", "feature": "Temporary Storage Handling", "status": "Implemented"}
            ]
        }
    }

    def get_summary(self, profile_name: str) -> Dict[str, Any]:
        return self.PROFILES.get(profile_name, self.PROFILES["GDPR"])
