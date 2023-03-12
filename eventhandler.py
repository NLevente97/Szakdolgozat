from threading import Thread
import numpy as np
import time

# the class to handle the input events
# handling the actions based on the difference during the current  and previous state of the system
class Eventhandler(object):
    # intialize the event handler
    def __init__(self, **kwargs) -> None:
        super().__init__()
        # reference to the robotcontroller
        self.robotcontroller = kwargs["robotcontroller"]
        # copying the data dictionary from the robotcontroller, so it wont be a reference but a new dictionary with the same values
        self.prev_state = self.robotcontroller.data.copy()
        self.current_state = self.robotcontroller.data.copy()
        # list of actions to be executed
        self.actions = []
        # flag to indicate if the state has changed
        self.changed = False

    # the function that checks the current state and compares it to the previous state and handles the changes,
    # and finally updates the previous state to the current state and the current state to the new state
    def handle_events(self) -> None:
        # looping until the program terminates
        while not self.robotcontroller.data["DONE"]:
            # checking the current state and the previous state for differences
            for key in self.current_state:
                if self.prev_state[key] != self.current_state[key]:
                    # if there is a change creating an event object with the current state value
                    e = Event(value=self.current_state[key])
                    # checking for the keys that are currently handled by the program and setting an event type accordingly
                    if key == "L":
                        self.changed = True
                        # if np.sign(self.prev_state[key]) != np.sign(
                        #    self.current_state[key]
                        # ):
                        #    e.type = EventType.REVERSE
                        # else:
                        e.type = EventType.MOVE
                    if key == "Brake":
                        self.changed = True
                        e.type = EventType.BRAKE

                    # adding the event object to the list of actions to be executed
                    self.actions.append(e)
            # updating the previous state to the current state
            self.prev_state = self.current_state.copy()
            # updating the current state to the new state
            self.current_state = self.robotcontroller.data.copy()
            # if there is a change in the state, the actions are executed in a new thread,
            # so it wont block the thread that is handling the events
            if self.changed:
                # resetting the changed flag
                self.changed = False
                # creating a new thread to execute the actions, passing the copy of the actions list as a parameter
                self.action_thread = Thread(
                    target=self.handle_actions, kwargs={"actions": self.actions.copy()}
                )
                # starting the thread
                self.action_thread.start()
            # resetting the actions list to be empty again
            self.actions = []

    # the function that handles the actions, it takes the actions list as a parameter and executes the actions in the list
    def handle_actions(self, **kwargs) -> None:
        # using the kwargs.get() function, so if there is no action, it will return None and not an error
        actions = kwargs.get("actions")
        # looping through the actions list
        for action in actions:
            print(action)
            # handling the actions based on the event type
            if action.type == EventType.BRAKE:
                if action.value:
                    self.robotcontroller.motorcontroller.brake()
            elif action.type == EventType.MOVE:
                # for the THROTTLE event, the value is passed to the motorcontroller to control both motors
                if self.robotcontroller.data["Brake"] == False:
                    self.robotcontroller.motorcontroller.throttle(action.value)
            # negative value because of the reverse direction of the motor
            # elif action.type == EventType.REVERSE:
            #    if self.robotcontroller.data["Brake"] == False:
            #        self.robotcontroller.motorcontroller.throttle_motor_1(action.value)
            #        self.robotcontroller.motorcontroller.throttle_motor_2(-action.value)
            elif action.type == EventType.STEER:
                pass
            elif action.type == EventType.PULL:
                pass
            else:
                pass
                # if the event type is not handled, print an error message
                # print(f"Event type not handled: {action.type}")


# the Event class
class Event:
    # initialize the event object, with the value and the type of the event,
    # using the enum class EventType, and the value of the event.
    # using the kwargs.get() function so if there is no value, it will return None and not an error
    def __init__(self, **kwargs) -> None:
        self.value = kwargs.get("value")
        self.type = kwargs.get("type")

    def __str__(self) -> str:
        return f"Event: \n type: { self.type},  value: {self.value}"


# the EventType enum class
class EventType:
    MOVE = 0
    BRAKE = 1
    PULL = 2
