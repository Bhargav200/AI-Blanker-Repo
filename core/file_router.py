import os
from typing import Dict, Any
from core.parser.txt_parser import TXTParser
from core.parser.csv_parser import CSVParser
from core.parser.json_parser import JSONParser
from core.parser.pdf_parser import PDFParser
from core.parser.docx_parser import DOCXParser
from core.ocr.pipeline import OCRPipeline

class FileRouter:
    def __init__(self):
        self.parsers = {
            ".txt": TXTParser(),
            ".csv": CSVParser(),
            ".json": JSONParser(),
            ".pdf": PDFParser(),
            ".docx": DOCXParser(),
            ".png": OCRPipeline(),
            ".jpg": OCRPipeline(),
            ".jpeg": OCRPipeline()
        }

    def route_file(self, file_path: str) -> Dict[str, Any]:
        ext = os.path.splitext(file_path)[1].lower()
        parser = self.parsers.get(ext)
        if not parser:
            raise ValueError(f"Unsupported file format: {ext}")
            
        if isinstance(parser, OCRPipeline):
            return parser.process(file_path)
        else:
            return parser.parse(file_path)
