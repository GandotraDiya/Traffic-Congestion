import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def read_license_plate(plate_image):
    """Extracts text from the license plate image."""
    gray = cv2.cvtColor(plate_image, cv2.COLOR_BGR2GRAY)  
    text = pytesseract.image_to_string(gray, config='--psm 8') 
    return text.strip()  
