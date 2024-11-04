import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

# Email setup
sender_email = "your_email@example.com"
receiver_email = "recipient@example.com"
password = "your_email_password"

# Load the image and read it as binary data
with open('/home/jimit/Pictures/Screenshots/test1.png', 'rb') as img_file:
    img_data = img_file.read()

# Create the email message
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = "Here is your image"

# Attach the image
image_attachment = MIMEImage(img_data, name="test1.png")
msg.attach(image_attachment)

# Add an email body
msg.attach(MIMEText("Please find the attached image.", "plain"))

# Send the email
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, msg.as_string())

print("Email sent successfully with the image attachment.")