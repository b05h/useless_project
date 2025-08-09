import cv2
import numpy as np

# Load Haar cascades (make sure OpenCV can find these XML files)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

def detect_sunglasses_from_frame(frame):
    """
    Detect if the person in the frame is wearing sunglasses.

    Args:
        frame: BGR image (numpy array)

    Returns:
        detected (bool): True if sunglasses detected, False otherwise
        annotated_frame: frame annotated with detection boxes and info
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    if len(faces) == 0:
        return False, frame  # No face found

    for (x, y, w, h) in faces:
        face_roi = frame[y:y+h, x:x+w]
        gray_roi = gray[y:y+h, x:x+w]

        eyes = eye_cascade.detectMultiScale(gray_roi)
        if len(eyes) == 0:
            # No eyes detected – possibly sunglasses or closed eyes
            cv2.putText(frame, "No eyes detected - Possible sunglasses", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            return True, frame

        dark_eye_count = 0
        for (ex, ey, ew, eh) in eyes:
            eye_region = gray_roi[ey:ey+eh, ex:ex+ew]
            _, thresh = cv2.threshold(eye_region, 50, 255, cv2.THRESH_BINARY_INV)
            dark_ratio = cv2.countNonZero(thresh) / (ew * eh)
            if dark_ratio > 0.4:
                dark_eye_count += 1
            # Draw rectangles around eyes
            cv2.rectangle(frame, (x+ex, y+ey), (x+ex+ew, y+ey+eh), (255, 0, 0), 2)

        if dark_eye_count >= 2:
            cv2.putText(frame, "Sunglasses Detected! Access Granted 😎", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            return True, frame
        else:
            cv2.putText(frame, "No Sunglasses Detected", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            return False, frame

    return False, frame