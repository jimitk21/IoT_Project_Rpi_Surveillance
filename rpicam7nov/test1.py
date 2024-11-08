from gpiozero import MotionSensor
from time import sleep
import os

pir = MotionSensor(4)

print("Waiting for sensor to stabilize...")
sleep(30)  # Wait for 30 seconds to let the PIR sensor stabilize

print("Sensor ready.")

while True:
    if pir.motion_detected:
        print("Motion detected!")
        # Capture an image using the camera
        os.system("rpicam-still -o ~/Desktop/img1234.jpg")
        print("Image captured.")
        sleep(2)  # Delay to avoid multiple captures in a short time
    else:
        print("No motion detected.")
    sleep(2)
