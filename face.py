import cv2
import time

# Load Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Open webcam
video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened():
    print("❌ ERROR: Could not access webcam!")
    exit()

face_present = False  # Track if a face is currently detected
last_seen = time.time()  # Time when the face was last seen

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("❌ ERROR: Could not read frame!")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # If faces are detected
    if len(faces) > 0:
        last_seen = time.time()  # Update last seen time
        face_present = True
    else:
        # If the face was there before but now it's gone, send an alert
        if face_present and time.time() - last_seen > 2:  # Alert after 2 seconds
            print("🚨 ALERT! Face disappeared!")
            face_present = False  # Reset flag to prevent repeated alerts

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    # Show the frame
    cv2.imshow("Face Detection", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("🔴 Exiting program...")
        break

video_capture.release()
cv2.destroyAllWindows()
