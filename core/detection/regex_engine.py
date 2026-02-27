import re
from typing import List, Dict, Any

class RegexEngine:
    def __init__(self, custom_regex: List[Dict[str, str]] = None):
        self.patterns = {
            "EMAIL": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            "PHONE": r'\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
            "SSN": r'\d{3}-\d{2}-\d{4}',
            "CREDIT_CARD": r'\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}',
            "IP_ADDRESS": r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b',
            "BANK_ACCOUNT": r'\b\d{9,18}\b',
            "PASSPORT": r'[A-Z][0-9]{7}',
            "DRIVER_LICENSE": r'[A-Z0-9]{5,15}'
        }
        if custom_regex:
            for item in custom_regex:
                self.patterns[item['name']] = item['pattern']

    def detect(self, text: str) -> List[Dict[str, Any]]:
        entities = []
        for entity_type, pattern in self.patterns.items():
            for match in re.finditer(pattern, text):
                entities.append({
                    "entity_text": match.group(),
                    "entity_type": entity_type,
                    "start_char": match.start(),
                    "end_char": match.end(),
                    "source": "Regex",
                    "confidence_score": 1.0 # Regex is high precision by default
                })
        return entities
