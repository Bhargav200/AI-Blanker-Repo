from typing import List, Dict, Any, Optional
from faker import Faker

class TextRedactor:
    def __init__(self, mode: str = "Mask", pseudonym_mappings: Optional[Dict[str, str]] = None):
        self.mode = mode
        self.faker = Faker()
        self.pseudonym_mappings = pseudonym_mappings or {}
        self.entity_counters = {}

    def get_replacement(self, entity_text: str, entity_type: str) -> str:
        if self.mode == "Mask":
            return "[REDACTED]"
        elif self.mode == "Label":
            return f"[{entity_type}]"
        elif self.mode == "Pseudonym":
            key = f"{entity_type}_{entity_text}"
            if key not in self.pseudonym_mappings:
                counter = self.entity_counters.get(entity_type, 1)
                self.pseudonym_mappings[key] = f"{entity_type}_{counter:03d}"
                self.entity_counters[entity_type] = counter + 1
            return self.pseudonym_mappings[key]
        elif self.mode == "Synthetic":
            if entity_type == "PERSON":
                return self.faker.name()
            elif entity_type == "EMAIL":
                return self.faker.email()
            elif entity_type == "PHONE":
                return self.faker.phone_number()
            elif entity_type == "LOCATION":
                return self.faker.city()
            elif entity_type == "DATE":
                return self.faker.date()
            else:
                return f"[SYNTHETIC_{entity_type}]"
        return "[REDACTED]"

    def redact(self, text: str, entities: List[Dict[str, Any]]) -> str:
        # Sort entities in reverse order of their position to avoid offset shifts
        sorted_entities = sorted(entities, key=lambda x: x['start_char'], reverse=True)
        
        redacted_text = text
        for ent in sorted_entities:
            replacement = self.get_replacement(ent['entity_text'], ent['entity_type'])
            ent['replacement_text'] = replacement
            
            start = ent['start_char']
            end = ent['end_char']
            redacted_text = redacted_text[:start] + replacement + redacted_text[end:]
            
        return redacted_text
