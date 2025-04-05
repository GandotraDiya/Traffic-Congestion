import cv2
from detect_plate import detect_plate
from read_plate import read_license_plate

cap = cv2.VideoCapture(2)  

if not cap.isOpened():
    print("Error: Cannot open Iriun Webcam. Make sure it's running.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Couldn't read frame.")
        break

 
    plate_image, frame_with_box = detect_plate(frame)

    if plate_image is not None:
        plate_number = read_license_plate(plate_image)
        print("Detected License Plate:", plate_number)  

 
    cv2.imshow("License Plate Recognition", frame_with_box)

    if cv2.waitKey(1) & 0xFF == ord('q'):  
        break

cap.release()
cv2.destroyAllWindows()
