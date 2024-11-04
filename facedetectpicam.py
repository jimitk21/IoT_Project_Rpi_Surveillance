import cv2

# Load the pre-trained Haar Cascade Classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detect_faces():
    # Open a connection to the default camera (0)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Cannot open camera")
        return
    
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        # If frame read is successful
        if not ret:
            print("Error: Failed to capture image")
            break
        
        # Convert the frame to grayscale (face detection works better in grayscale)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces in the grayscale frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        # Draw rectangles around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        # Display the resulting frame
        cv2.imshow('Real-Time Face Detection', frame)
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()

# Run the face detection function
detect_faces()
