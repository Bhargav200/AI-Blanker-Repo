from typing import List, Dict, Any

class RiskClassifier:
    HIGH_RISK_TYPES = ["SSN", "CREDIT_CARD", "PASSPORT", "BANK_ACCOUNT", "DRIVER_LICENSE"]
    MEDIUM_RISK_TYPES = ["EMAIL", "PHONE", "PERSON", "ORGANIZATION"]
    LOW_RISK_TYPES = ["LOCATION", "DATE", "IP_ADDRESS"]

    def classify_entity(self, entity: Dict[str, Any]) -> str:
        ent_type = entity['entity_type']
        if ent_type in self.HIGH_RISK_TYPES:
            return "High"
        elif ent_type in self.MEDIUM_RISK_TYPES:
            return "Medium"
        else:
            return "Low"

    def classify_file(self, entities: List[Dict[str, Any]]) -> str:
        if any(ent['risk_level'] == "High" for ent in entities):
            return "High"
        elif any(ent['risk_level'] == "Medium" for ent in entities):
            return "Medium"
        else:
            return "Low"
