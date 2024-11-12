from gpiozero import MotionSensor
from time import sleep
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from supabase import create_client, Client

# Configure motion sensor
pir = MotionSensor(4)

# Email credentials
sender_email = "YOUR_EMAIL"
sender_password = "YOUR_PASSWORD"
recipient_email = "RECIPIENT_EMAIL"

# Supabase configuration
url = "URL"
key = "APIKEY"
supabase: Client = create_client(url, key)
bucket_name = "jimit-bucket"

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

def upload_to_supabase(image_path):
    filename = os.path.basename(image_path)
    with open(image_path, "rb") as file:
        try:
            # Upload the image to Supabase
            result = supabase.storage.from_(bucket_name).upload(filename, file)
           
            # Get the public URL of the uploaded image
            public_url = supabase.storage.from_(bucket_name).get_public_url(filename)
           
            print(f"Image uploaded successfully. Public URL: {public_url}")
            return public_url
        except Exception as e:
            print(f"Error uploading image to Supabase: {e}")
            return None

while True:
    if pir.motion_detected:
        print("Motion detected!")
        
        # Generate timestamp and update the image path
        timestamp = datetime.now().strftime("%d%m%y_%H_%M_%S")
        image_path = f"/home/pi/Desktop/img_{timestamp}.jpg"  # Ensure this path matches your device setup
        
        # Capture an image using the camera
        os.system(f"rpicam-still -o {image_path}")
        print("Image captured.")

        # Send email with the captured image
        send_email(image_path)

        # Upload the image to Supabase
        upload_to_supabase(image_path)

        # Delay to avoid multiple captures and emails in a short time
        sleep(15)
    else:
        print("No motion detected.")
    sleep(5)
