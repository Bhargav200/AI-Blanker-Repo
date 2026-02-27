import spacy
from typing import List, Dict, Any
from config.settings import settings

class NLPEngine:
    def __init__(self, model_name: str = None):
        model = model_name or settings.SPACY_MODEL
        try:
            self.nlp = spacy.load(model)
        except OSError:
            print(f"Warning: Model {model} not found. Using blank 'en' model for now.")
            self.nlp = spacy.blank("en")

    def detect(self, text: str) -> List[Dict[str, Any]]:
        doc = self.nlp(text)
        entities = []
        for ent in doc.ents:
            # Map spaCy entities to our internal types if needed
            entity_type = ent.label_
            if entity_type == "PERSON":
                entity_type = "PERSON"
            elif entity_type in ["GPE", "LOC"]:
                entity_type = "LOCATION"
            elif entity_type == "ORG":
                entity_type = "ORGANIZATION"
            elif entity_type == "DATE":
                entity_type = "DATE"
                
            entities.append({
                "entity_text": ent.text,
                "entity_type": entity_type,
                "start_char": ent.start_char,
                "end_char": ent.end_char,
                "source": "NLP",
                "confidence_score": 0.85 # Base confidence for NLP
            })
        return entities
