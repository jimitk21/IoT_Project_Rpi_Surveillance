from gpiozero import MotionSensor
from time import sleep
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Configure motion sensor
pir = MotionSensor(4)

# Email credentials
sender_email = "YOUR_EMAIL"
sender_password = "YOUR_PASSWORD"
recipient_email = "RECIPIENT_EMAIL"

print("Waiting for sensor to stabilize...")
sleep(30)  # Wait for 30 seconds to let the PIR sensor stabilize
print("Sensor ready.")

def send_email(image_path):
    try:
        # Set up the MIME
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = "Motion Detected - Image Attached"
        body = "Motion was detected. Please find the captured image attached."
        msg.attach(MIMEText(body, 'plain'))

        # Attach the image file
        with open(image_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(image_path)}')
            msg.attach(part)

        # Connect to the Gmail server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())

        print("Email sent successfully.")

    except Exception as e:
        print(f"Error: {e}")

while True:
    if pir.motion_detected:
        print("Motion detected!")
        
        # Capture an image using the camera
        image_path = "~/Desktop/img1234.jpg"
        os.system(f"rpicam-still -o {image_path}")
        print("Image captured.")

        # Send email with the captured image
        send_email(image_path)

        # Delay to avoid multiple captures and emails in a short time
        sleep(15)
    else:
        print("No motion detected.")
    sleep(5)