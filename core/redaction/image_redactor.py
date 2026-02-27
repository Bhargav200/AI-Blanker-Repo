import cv2
import os
from typing import List, Dict, Any

class ImageRedactor:
    def redact(self, image_path: str, boxes: List[Dict[str, Any]], output_path: str):
        img = cv2.imread(image_path)
        if img is None:
            return False
            
        for box in boxes:
            # Draw black rectangle over the detected PII
            left = box['left']
            top = box['top']
            width = box['width']
            height = box['height']
            
            cv2.rectangle(img, (left, top), (left + width, top + height), (0, 0, 0), -1)
            
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cv2.imwrite(output_path, img)
        return True
