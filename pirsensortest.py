from gpiozero import MotionSensor
from time import sleep

pir = MotionSensor(4)

print("Waiting for sensor to stabilize...")
sleep(30)  # Wait for 30 seconds to let the PIR sensor stabilize

print("Sensor ready.")

while True:
    if pir.motion_detected:
        print("Motion detected!")
    else:
        print("No motion detected.")
    sleep(2)