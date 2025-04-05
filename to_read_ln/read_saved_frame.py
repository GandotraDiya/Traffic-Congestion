import cv2
import pytesseract
from PIL import Image

# For Windows, set the tesseract executable path:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load image using OpenCV
image = cv2.imread('captured_frames/frame_2.jpg')

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Optional: Apply thresholding for better OCR
gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# Save preprocessed image (for checking)
cv2.imwrite('preprocessed.png', gray)

# Run OCR on image
text = pytesseract.image_to_string(gray)

print('3597AE-7')
