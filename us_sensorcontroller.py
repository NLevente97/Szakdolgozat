import time
import board
import adafruit_hcsr04
import RPi.GPIO as GPIO

THRESH_HOLD = 10
a = 1
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D21, echo_pin=board.D20)

try:
    b = 1
    if b == 0:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(20, GPIO.OUT)
        GPIO.output(20, GPIO.HIGH)
    while b == 0:
        pass
except:
    pass
# finally:
# GPIO.output(20, GPIO.LOW)
# GPIO.cleanup()
if a == 1:
    while True:
        try:
            if sonar.distance < THRESH_HOLD:
                print("BRAKE!!")
            print(f"{(sonar.distance):.3f}")
        except RuntimeError as e:
            print(str(e))
        time.sleep(0.2)
