import cv2

cap = cv2.VideoCapture(2)  

if not cap.isOpened():
    print("Error: Cannot open Iriun Webcam. Make sure it's running.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Couldn't read frame.")
        break

    cv2.imshow("iPhone Camera Feed", frame)  

    if cv2.waitKey(1) & 0xFF == ord('q'):  
        break

cap.release()
cv2.destroyAllWindows()
