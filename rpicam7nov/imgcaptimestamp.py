from gpiozero import MotionSensor
from time import sleep, strftime
import os

pir = MotionSensor(4)

print("Waiting for sensor to stabilize...")
sleep(30)  # Wait for 30 seconds to let the PIR sensor stabilize

print("Sensor ready.")

while True:
    if pir.motion_detected:
        print("Motion detected!")
        # Generate a timestamped filename in the format DDMM_Time
        timestamp = strftime("%d%m_%H%M%S")
        filename = f"~/Desktop/img-{timestamp}.jpg"
        
        # Capture an image using the camera
        os.system(f"rpicam-still -o {filename}")
        print(f"Image captured: {filename}")
        
        sleep(2)  # Delay to avoid multiple captures in a short time
    else:
        print("No motion detected.")
    sleep(2)
