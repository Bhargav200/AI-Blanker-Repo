import pdfplumber
from core.parser.base import BaseParser
from typing import Dict, Any

class PDFParser(BaseParser):
    def parse(self, file_path: str) -> Dict[str, Any]:
        text = ""
        pages_metadata = []
        with pdfplumber.open(file_path) as pdf:
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text() or ""
                text += page_text + "\n"
                pages_metadata.append({
                    "page_number": i + 1,
                    "width": page.width,
                    "height": page.height
                })
        return {
            "text": text,
            "structure": {
                "type": "pdf",
                "pages": pages_metadata
            }
        }
