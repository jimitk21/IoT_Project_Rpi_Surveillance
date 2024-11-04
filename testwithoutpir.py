import cv2
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

# Email setup
sender_email = "your_email@example.com"
receiver_email = "recipient@example.com"
password = "your_email_password"

# Load the Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Capture video from phone camera
url = "http://192.0.0.4:8080/video"
cap = cv2.VideoCapture(url)

face_detected_start = None  # Time when a face was first detected

def send_email_with_image(image_path):
    # Load the image and read it as binary data
    with open(image_path, 'rb') as img_file:
        img_data = img_file.read()

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Face Detected - Image Attached"

    # Attach the image
    image_attachment = MIMEImage(img_data, name="detected_face.png")
    msg.attach(image_attachment)

    # Add an email body
    msg.attach(MIMEText("A face was detected continuously for more than 3 seconds. See attached image.", "plain"))

    # Send the email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

    print("Email sent successfully with the image attachment.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize and convert the frame to grayscale
    frame = cv2.resize(frame, (320, 240))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Check if a face is detected
    if len(faces) > 0:
        if face_detected_start is None:
            face_detected_start = time.time()  # Start timer when face first detected

        elif time.time() - face_detected_start >= 3:  # Check if face has been detected for over 3 seconds
            # Save the image
            image_path = "/home/jimit/detected_face.png"
            cv2.imwrite(image_path, frame)
            print("Face detected continuously for 3 seconds. Image saved.")

            # Send the saved image via email
            send_email_with_image(image_path)
            
            # Reset the timer to avoid multiple emails
            face_detected_start = None
    else:
        face_detected_start = None  # Reset timer if no face is detected

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Blue rectangles

    # Display the resulting frame
    cv2.imshow("Phone Camera Feed with Face Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
