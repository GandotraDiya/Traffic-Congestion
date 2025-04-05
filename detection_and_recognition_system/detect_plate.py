import cv2


plate_cascade = cv2.CascadeClassifier("haarcascades/haarcascade_russian_plate_number.xml")

def detect_plate(frame):
    """Detects the license plate in a video frame."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

    for (x, y, w, h) in plates:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draws rectangle around the plate
        plate_image = frame[y:y + h, x:x + w]  # Crop the detected plate
        return plate_image, frame 

    return None, frame  
