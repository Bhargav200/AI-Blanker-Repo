from PIL import Image, ImageDraw, ImageFont
import os

class RedactionVisualizer:
    def __init__(self, font_size: int = 20):
        self.font_size = font_size
        # Try to load common fonts
        self.font = None
        for font_name in ["arial.ttf", "DejaVuSans.ttf", "LiberationSans-Regular.ttf", "cour.ttf"]:
            try:
                self.font = ImageFont.truetype(font_name, self.font_size)
                break
            except:
                continue
        
        if self.font is None:
            self.font = ImageFont.load_default()

    def text_to_image(self, text: str, output_path: str):
        # Split text into lines
        lines = text.split('\n')
        
        # Calculate image size
        line_height = self.font_size + 5
        max_width = 800
        height = len(lines) * line_height + 40
        
        # Create image
        img = Image.new('RGB', (max_width, height), color=(255, 255, 255))
        d = ImageDraw.Draw(img)
        
        # Draw text
        y_offset = 20
        for line in lines:
            d.text((20, y_offset), line, font=self.font, fill=(0, 0, 0))
            y_offset += line_height
            
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img.save(output_path)
        return True
