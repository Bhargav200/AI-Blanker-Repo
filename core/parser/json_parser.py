import json
from core.parser.base import BaseParser
from typing import Dict, Any

class JSONParser(BaseParser):
    def parse(self, file_path: str) -> Dict[str, Any]:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        text = json.dumps(data, indent=2)
        return {
            "text": text,
            "structure": {
                "type": "json",
                "data": data
            }
        }
