import board
import busio
import adafruit_pca9685
import time


class MotorController(object):

    MOTOR_1_CHANNEL = 12
    MOTOR_2_CHANNEL = 13
    SERVO_1_CHANNEL = 14
    LED_CHANNEL = 15
    MINIMUM = int(hex(65535 // 20), 16)
    MAXIMUM = int(hex(65535 // 10), 16)
    DISTANCE = MAXIMUM - MINIMUM
    NUM_STEPS = 10
    STEP = DISTANCE // NUM_STEPS
    NEUTRAL = int(hex(MINIMUM + ((MAXIMUM - MINIMUM) // 2)), 16)
    DISTANCE_TO_NEUTRAL = NEUTRAL - MINIMUM

    def __init__(self, **kwargs):
        self.carcontroller = kwargs["carcontroller"]

        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.hat = adafruit_pca9685.PCA9685(self.i2c)
        self.hat.frequency = 50
        self.hat.channels[MotorController.LED_CHANNEL].duty_cycle = 65535
        self.hat.channels[
            MotorController.MOTOR_1_CHANNEL
        ].duty_cycle = MotorController.NEUTRAL
        self.hat.channels[
            MotorController.MOTOR_2_CHANNEL
        ].duty_cycle = MotorController.NEUTRAL
        time.sleep(1)

    def reset(self):
        self.hat.channels[
            MotorController.MOTOR_1_CHANNEL
        ].duty_cycle = MotorController.NEUTRAL
        self.hat.channels[MotorController.LED_CHANNEL].duty_cycle = 0
        self.hat.deinit()

    def throttle(self, value):
        # print(self.carcontroller.data)
        # print(MotorController.NEUTRAL + value * MotorController.DISTANCE_TO_NEUTRAL)
        self.hat.channels[MotorController.MOTOR_1_CHANNEL].duty_cycle = int(
            MotorController.NEUTRAL + value * MotorController.DISTANCE_TO_NEUTRAL
        )

    def run(self):
        pass
        # print(self.data)
        # self.hat.channels[MotorController.MOTOR_1_CHANNEL].duty_cycle = int(
        # gear = input("Enter gear: ")
        # if not gear:
        #    gear = 0
        # self.hat.channels[MotorController.MOTOR_1_CHANNEL].duty_cycle = (
        #    int(gear) * MotorController.STEP + MotorController.NEUTRAL
        # )
        # print(
        #    "Motor 1: {}".format(
        #        self.hat.channels[MotorController.MOTOR_1_CHANNEL].duty_cycle
        #    )
        # )
        # time.sleep(0.1)

    # except KeyboardInterrupt:
    #    self.hat.channels[
    #        MotorController.MOTOR_1_CHANNEL
    #    ].duty_cycle = MotorController.NEUTRAL
    #    self.hat.channels[MotorController.LED_CHANNEL].duty_cycle = 0
    #    self.hat.deinit()
    #    exit()
