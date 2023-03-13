import time
import board
import adafruit_hcsr04
import numpy as np
from collections import deque


class US_SensorController(object):

    # Constans for the braking threshold and the moving averaga filter window size
    THRESHOLD = 10
    WINDOW_SIZE = 5

    def __init__(self, **kwargs) -> None:

        self.robotcontroller = kwargs.get("robotcontroller")

        # The sensors
        self.front = adafruit_hcsr04.HCSR04(trigger_pin=board.D21, echo_pin=board.D20)
        self.left = adafruit_hcsr04.HCSR04(trigger_pin=board.D19, echo_pin=board.D18)
        self.right = adafruit_hcsr04.HCSR04(trigger_pin=board.D17, echo_pin=board.D16)
        self.back = adafruit_hcsr04.HCSR04(trigger_pin=board.D15, echo_pin=board.D14)

        # The arrays for the sensor data
        self.front_data = deque()  # raw input
        self.front_data_avaraged = (
            deque()
        )  # filered data used for controlling the robot
        self.front_temporary = deque()  # used for the moving average filter

    def start(self) -> None:
        # while not self.robotcontroller.data["DONE"]:
        while True:
            try:
                self.front_data.append(self.front.distance)

                self.front_temporary.append(self.front.distance)

                if len(self.front_temporary) >= US_SensorController.WINDOW_SIZE:
                    self.front_temporary.popleft()
                self.front_data_avaraged.append(np.average(self.front_temporary))
                # print(f"{(self.front.distance):.3f}", end="\r") # printing out the current distance
                time.sleep(0.05)
            except RuntimeError as e:
                print(str(e))
            except KeyboardInterrupt:
                break

    # function to plot sensor data, only used for testing
    def plot(self) -> None:
        # importing matplotlib to plot
        import matplotlib

        # setting backend to the non-interactive pdf, so it can work on a headless raspberry pi
        matplotlib.use("pdf")
        import matplotlib.pyplot as plt  # importing the plotting module

        # ONLY THE FRONT SENSOR IS USED
        # printing out the arrays to cmd for reference
        print("normal: ", self.front_data, len(self.front_data))
        print(
            "averaged: ",
            self.front_data_avaraged,
            len(self.front_data_avaraged),
        )

        # plotting the data
        plt.plot(list(self.front_data), label="raw data")
        plt.plot(list(self.front_data_avaraged), label="averaged")

        # plot settings
        plt.legend(frameon=False)
        plt.xlabel("Number of data (dt=0.05s)")
        plt.ylabel("Distance [cm]")

        # saving to a pdf file
        plt.savefig("us_sensor_test.pdf")
