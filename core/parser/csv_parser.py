import pandas as pd
from core.parser.base import BaseParser
from typing import Dict, Any

class CSVParser(BaseParser):
    def parse(self, file_path: str) -> Dict[str, Any]:
        df = pd.read_csv(file_path)
        # Convert to a string representation that preserves structure for detection
        # but we also need to keep the dataframe for redaction
        text = df.to_string()
        return {
            "text": text,
            "structure": {
                "type": "csv",
                "columns": df.columns.tolist(),
                "data": df.to_dict(orient='records')
            }
        }
