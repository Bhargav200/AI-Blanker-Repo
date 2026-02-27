from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseParser(ABC):
    @abstractmethod
    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Parses a file and returns a dictionary with 'text' and 'structure' metadata.
        """
        pass
