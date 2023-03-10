import time
import board
import adafruit_hcsr04

THRESH_HOLD = 10

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D15, echo_pin=board.D14)
while True:
    try:
        if sonar.distance < THRESH_HOLD:
            print("BRAKE!!")
        print(f"{(sonar.distance):.3f}")
    except RuntimeError as e:
        print(str(e))
    time.sleep(0.2)
