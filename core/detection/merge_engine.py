from typing import List, Dict, Any

class MergeEngine:
    def merge(self, regex_entities: List[Dict[str, Any]], nlp_entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Combine all entities
        all_entities = regex_entities + nlp_entities
        
        # Sort by start character and length (longer first for overlaps)
        all_entities.sort(key=lambda x: (x['start_char'], -(x['end_char'] - x['start_char'])))
        
        merged = []
        last_end = -1
        
        for ent in all_entities:
            # If the current entity starts after the last merged entity ends, it's not an overlap
            if ent['start_char'] >= last_end:
                merged.append(ent)
                last_end = ent['end_char']
            else:
                # Overlap detected
                # Prioritize Regex over NLP, or higher confidence
                last_ent = merged[-1]
                if ent['source'] == 'Regex' and last_ent['source'] == 'NLP':
                    merged[-1] = ent
                    last_end = ent['end_char']
                elif ent['confidence_score'] > last_ent['confidence_score']:
                    merged[-1] = ent
                    last_end = ent['end_char']
                    
        return merged
