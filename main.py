from inputs import get_gamepad
from pynput import keyboard
import types
import time

Letters = [
    ['a','b','c','d'],
    ['e','f','g','h'],
    ['i','j','k','l'],
    ['m','n','o','p'],
    ['q','r','s','t'],
    ['u','v','w','x'],
    ['y','z',None, None]
]

symbols = [
    ['(', ')', '{', '}'],
    ['[',']', '_', "@"],
    [';', ':', '.', ','],
    ['#', '=', '!', '?'],
    ['+', '-', '*', '/'],
    ['<','>',"\\", "%"]
]

Button_states = {
    'ABS_RZ': 0, #ZR
    'ABS_Z': 0, #ZL
    'BTN_TL': 0, #L
    'BTN_TR': 0, #R
    'BTN_NORTH': 0, #X
    'BTN_EAST': 0, #A
    'BTN_WEST': 0, # Y
    'BTN_SOUTH': 0, #B
    'ABS_HAT0X': 0, #Nav up or down
    'ABS_HAT0Y': 0, #Nav left or right
    'ABS_X': 0, #Left stick left or right
    'ABS_Y': 0, #Left stick up or down
    'ABS_RX': 0, #Right stick left or right
    'ABS_RY': 0, #Right stick up or down
}

class Counter():
    def __init__(self):
        self.ControllerCounter = 0
        self.last_press_time = time.time()
        self.CounterPressDelay = 1
        
    def IncrementCounter(self, code):
        if Button_states[code] != 1: return
        print(self.ControllerCounter)
        self.ControllerCounter += 1
        self.ControllerCounter %= 7
        self.last_press_time = time.time()

    def UpdateCounter(self):
        if time.time() - self.last_press_time > self.CounterPressDelay:
            self.ControllerCounter = 0
counter = Counter()

Mapping = {
    'ABS_RZ': None, #ZR
    'ABS_Z': None, #ZL
    'BTN_TL': None, #L
    'BTN_TR': counter.IncrementCounter, #R
    'BTN_NORTH': None, #X
    'BTN_EAST': None, #A
    'BTN_WEST': None, # Y
    'BTN_SOUTH': None, #B
    'ABS_HAT0X': None, #Nav up or down
    'ABS_HAT0Y': None, #Nav left or right
    'ABS_X': None, #Left stick left or right
    'ABS_Y': None, #Left stick up or down
    'ABS_RX': None, #Right stick left or right
    'ABS_RY': None, #Right stick up or down
}

while True:
    events = get_gamepad()
    counter.UpdateCounter()
    for event in events:
        if (event.ev_type == 'Sync'): continue
        Button_states[event.code] = event.state

        if not Mapping.get(event.code): 
            print("Unable to find button in Mapping dict or no value in key")
            continue
            
        if Mapping[event.code]: Mapping[event.code](event.code)