import pytesseract
import cv2
import numpy as np
from PIL import Image
from config.settings import settings
from typing import Dict, Any

class OCRPipeline:
    def __init__(self):
        if settings.TESSERACT_CMD:
            pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD

    def preprocess_image(self, image_path: str):
        # Load image
        img = cv2.imread(image_path)
        if img is None:
            return None
            
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Noise reduction
        denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
        
        # Thresholding
        _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return thresh

    def process(self, image_path: str) -> Dict[str, Any]:
        processed_img = self.preprocess_image(image_path)
        if processed_img is None:
            return {"text": "", "boxes": [], "error": "Could not read image"}
            
        # Get OCR data including bounding boxes
        data = pytesseract.image_to_data(processed_img, output_type=pytesseract.Output.DICT)
        
        text = ""
        boxes = []
        n_boxes = len(data['text'])
        for i in range(n_boxes):
            if int(data['conf'][i]) > 0: # Filter out empty or low confidence detections
                text += data['text'][i] + " "
                boxes.append({
                    "text": data['text'][i],
                    "left": data['left'][i],
                    "top": data['top'][i],
                    "width": data['width'][i],
                    "height": data['height'][i],
                    "conf": data['conf'][i]
                })
                
        return {
            "text": text.strip(),
            "boxes": boxes,
            "structure": {"type": "image"}
        }
