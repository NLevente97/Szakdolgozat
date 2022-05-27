import board
import busio
import adafruit_pca9685
import time

# the class that controls the motors using the hat module for PCA9685 chip, which is a 12 bit PWM and servo control hat,
# the i2c bus of the raspberry pi board and the adafruit library for the PCA9685 chip
class MotorController(object):

    # constants for the motor controller
    MOTOR_1_CHANNEL = 12  # channel for motor 1
    MOTOR_2_CHANNEL = 13  # channel for motor 2
    SERVO_1_CHANNEL = 14  # channel for servo 1 (currently not used)
    LED_CHANNEL = 15  # channel for the LED that indicates that the program is running

    # the duty cycle values are 16 bit integers, but the PCA9685 chip only supports 12 bit resolution,
    # so the duty cycle values are a not accurate, because of the shifting
    # the controlling pwm signal should have 20 ms period, the minimum duty cycle should be 1 ms (5%)
    # and the maximum duty cycle should be 2 ms (10%)
    MINIMUM = int(hex(65535 // 20), 16)  # minimum value for the motors PWM signal
    MAXIMUM = int(hex(65535 // 10), 16)  # maximum value for the motors PWM signal
    # neutral value for the motors PWM signal (the value that is used when the motors are not moving,
    # middlepoint between the minimum and maximum value)
    NEUTRAL = int(hex(MINIMUM + ((MAXIMUM - MINIMUM) // 2)), 16)
    # distance between the minimum and the neutral value,
    # used for the throttle function to be able to control the motors both way (forward/backwards)
    # with a value between -1 and 1 with the neutral value as 0
    DISTANCE_TO_NEUTRAL = NEUTRAL - MINIMUM

    # initialize the motor controller
    def __init__(self, **kwargs) -> None:
        # reference to the robot controller object
        self.robotcontroller = kwargs["robotcontroller"]
        # setting up the i2c bus for the communication with the PCA9685 chip
        self.i2c = busio.I2C(board.SCL, board.SDA)
        # creating the hat object to control the PCA9685 chip
        self.hat = adafruit_pca9685.PCA9685(self.i2c)
        # setting the frequency of the PCA9685 chip to 50 Hz, because the ESCs are designed to work with a signal with 20 ms period
        self.hat.frequency = 50

        # the hat object's channels list can be used to control the individual motors
        # connected to the pins corresponding to the channel's index

        # setting the duty cycle of the LED channel to 65535, which means that the LED is fully on,
        # signaling that the program is running
        self.hat.channels[MotorController.LED_CHANNEL].duty_cycle = 65535

        # setting the duty cycle of the motor channels to the neutral value, so the ESCs can self calibrate
        self.hat.channels[
            MotorController.MOTOR_1_CHANNEL
        ].duty_cycle = MotorController.NEUTRAL
        self.hat.channels[
            MotorController.MOTOR_2_CHANNEL
        ].duty_cycle = MotorController.NEUTRAL
        # waiting for the ESCs to self calibrate
        time.sleep(1)

    # the function that is called when the program is terminated
    def reset(self) -> None:
        # setting the duty cycle of the motor channels to the neutral value, so the motors stop
        self.hat.channels[
            MotorController.MOTOR_1_CHANNEL
        ].duty_cycle = MotorController.NEUTRAL
        # setting the duty cycle of the LED channel to 0, which means that the LED is fully off, signaling that the program has terminated
        self.hat.channels[MotorController.LED_CHANNEL].duty_cycle = 0
        # deinitializing the hat object
        self.hat.deinit()

    # the function that is called to control the motor 1 forward/backwards
    def throttle_motor_1(self, value: float) -> None:
        # setting the duty cycle of the motor channels to the value which calculated as:
        # the neutral value plus the distance to the neutral value multiplied by the value parameter,
        # the middlepoint is the neutral value, the value parameter is the scaled value of the joystick input (-1 to 1),
        # the distance to the neutral value is the distance between the minimum and the neutral value
        self.hat.channels[MotorController.MOTOR_1_CHANNEL].duty_cycle = int(
            MotorController.NEUTRAL + value * MotorController.DISTANCE_TO_NEUTRAL
        )

    # the function that is called to control the motor 2 forward/backwards
    def throttle_motor_2(self, value: float) -> None:
        self.hat.channels[MotorController.MOTOR_2_CHANNEL].duty_cycle = int(
            MotorController.NEUTRAL + value * MotorController.DISTANCE_TO_NEUTRAL
        )
