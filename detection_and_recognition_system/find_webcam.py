import cv2

for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Webcam found at index: {i}")
        cap.release()

cv2.destroyAllWindows()
