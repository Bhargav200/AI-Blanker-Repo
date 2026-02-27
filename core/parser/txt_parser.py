from core.parser.base import BaseParser
from typing import Dict, Any

class TXTParser(BaseParser):
    def parse(self, file_path: str) -> Dict[str, Any]:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        return {
            "text": text,
            "structure": {"type": "txt"}
        }
