import board
import busio
import adafruit_pca9685
import time
from adafruit_servokit import ServoKit


i2c = busio.I2C(board.SCL, board.SDA)
hat = adafruit_pca9685.PCA9685(i2c)
kit = ServoKit(channels=16)
kit.servo[12].angle = 90
kit.servo[13].angle = 90
time.sleep(2)
try:
    while True:
        kit.servo[12].angle = 100
        kit.servo[13].angle = 100
except KeyboardInterrupt:
    kit.servo[12].angle = 90
    kit.servo[13].angle = 90
    exit()
