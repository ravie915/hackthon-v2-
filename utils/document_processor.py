import pytesseract
from PIL import Image
import os

def validate_document(file):
    """Validate uploaded document."""
    max_size = 10 * 1024 * 1024  # 10MB
    
    if file.size > max_size:
        return False, "File too large (max 10MB)"
    
    allowed_types = ['application/pdf', 'image/jpeg', 'image/png', 'application/msword']
    if file.type not in allowed_types:
        return False, "File type not supported"
    
    return True, "Valid"

def extract_text_from_image(file):
    """Extract text from image using OCR."""
    try:
        image = Image.open(file)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return f"Error extracting text: {e}"