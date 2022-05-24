import board
import busio
import adafruit_pca9685
import time


class MotorController(object):

    MOTOR_1_CHANNEL = 12
    MOTOR_2_CHANNEL = 13
    MINIMUM = int(hex(65535 // 20), 16)
    MAXIMUM = int(hex(65535 // 10), 16)
    DISTANCE = MAXIMUM - MINIMUM
    NUM_STEPS = 10
    STEP = DISTANCE // NUM_STEPS
    NEUTRAL = int(hex(MINIMUM + ((MAXIMUM - MINIMUM) // 2)), 16)

    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.hat = adafruit_pca9685.PCA9685(self.i2c)
        self.hat.frequency = 50
        self.hat.channels[
            MotorController.MOTOR_1_CHANNEL
        ].duty_cycle = MotorController.NEUTRAL
        self.hat.channels[
            MotorController.MOTOR_2_CHANNEL
        ].duty_cycle = MotorController.NEUTRAL
        time.sleep(1)

    def start(self):
        try:
            while True:
                gear = input("Enter gear: ")
                if not gear:
                    gear = 0
                self.hat.channels[MotorController.MOTOR_1_CHANNEL].duty_cycle = (
                    int(gear) * MotorController.STEP + MotorController.NEUTRAL
                )
                print(
                    "Motor 1: {}".format(
                        self.hat.channels[MotorController.MOTOR_1_CHANNEL].duty_cycle
                    )
                )
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.hat.channels[
                MotorController.MOTOR_1_CHANNEL
            ].duty_cycle = MotorController.NEUTRAL
            self.hat.deinit()
            exit()


if __name__ == "__main__":
    motor = MotorController()
    motor.start()
