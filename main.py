from inputs import get_gamepad
from pynput.keyboard import Key, Controller
import types
import time

Letters = [
    ['a','b','c','d'],
    ['e','f','g','h'],
    ['i','j','k','l'],
    ['m','n','o','p'],
    ['q','r','s','t'],
    ['u','v','w','x'],
    ['y','z', None, None]
]

Numbers = [
    [1,2,3,4],
    [5,6,7,8],
    [9,0,None,None],
    [None,None,None,None],
    [None,None,None,None],
    [None,None,None,None],
    [None,None,None,None],
]

Symbols = [
    ['(', ')', '{', '}'],
    ['[',']', '_', "@"],
    [';', ':', '.', ','],
    ['#', '=', '!', '?'],
    ['+', '-', '*', '/'],
    ['<','>',"\\", "%"],
    [None, None, None, None]
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

Alt = False
def AltBTN(code):
    global Alt
    Alt = not Alt

class Counter():
    def __init__(self):
        self.ControllerCounter = 0
        self.last_press_time = time.time()
        self.CounterPressDelay = 1
        
    def IncrementCounter(self, code):
        if Button_states[code] != 1: return
        self.ControllerCounter += 1
        self.ControllerCounter %= 7
        self.last_press_time = time.time()

    def UpdateCounter(self):
        if time.time() - self.last_press_time > self.CounterPressDelay:
            self.ControllerCounter = 0
counter = Counter()

keyboard = Controller()
class TypeWriter():
    def __init__(self, codeX, codeY, type):
        self.lastdirection = [0,0]
        self.direction = [0,0]
        self.type = type #0 for left, 1 for right
        self.Deadzone = 8000
        self.codeX = codeX
        self.codeY = codeY

    def UpdateDirection(self):
        X = Button_states[self.codeX]
        Y = Button_states[self.codeY]
        self.lastdirection = self.direction.copy()

        #X axis
        if X > self.Deadzone:
            self.direction[0] = 1
        elif X < -self.Deadzone:
            self.direction[0] = -1
        else:
            self.direction[0] = 0

        #Y axis
        if Y > self.Deadzone:
            self.direction[1] = 1
        elif Y < -self.Deadzone:
            self.direction[1] = -1
        else:
            self.direction[1] = 0

    def Write(self):
        Mode = 0
        if self.lastdirection == [0,1]: #Up
            Mode = 0
        elif self.lastdirection == [1,0]: #Right
            Mode = 1
        elif self.lastdirection == [0,-1]: #Down
            Mode = 2
        elif self.lastdirection == [-1, 0]: #Left
            Mode = 3

        if self.type == 0:
            letter = Letters[counter.ControllerCounter][Mode]
            if letter == None: return
            if Alt:
                letter = letter.upper()
            keyboard.type(letter)
        elif self.type == 1:
            if Alt:
                number = Numbers[counter.ControllerCounter][Mode]
                if number == None: return
                keyboard.type(str(number))
            else:
                symbol = Symbols[counter.ControllerCounter][Mode]
                if symbol == None: return
                keyboard.type(symbol)

LeftStickWriter = TypeWriter('ABS_X', 'ABS_Y', 0)
RightStickWriter = TypeWriter('ABS_RX', 'ABS_RY', 1)

def ManageLeftStick(code):
    if LeftStickWriter.direction == [0,0] and LeftStickWriter.lastdirection != [0,0]:
        LeftStickWriter.Write()

def ManageRightStick(code):
    if RightStickWriter.direction == [0,0] and RightStickWriter.lastdirection != [0,0]:
        RightStickWriter.Write()

def Backspace(code):
    if Button_states.get(code) == 255:
        keyboard.press(Key.backspace)

def Enter(code):
    if Button_states.get(code) == 1:
        keyboard.press(Key.enter)

def Space(code):
    if Button_states.get(code) == 1:
        keyboard.press(Key.space)

def Tab(code):
    if Button_states.get(code) == 1:
        keyboard.press(Key.tab)

Mapping = {
    'ABS_RZ': Backspace, #ZR
    'ABS_Z': AltBTN, #ZL
    'BTN_TL': None, #L
    'BTN_TR': counter.IncrementCounter, #R
    'BTN_NORTH': Tab, #X
    'BTN_EAST': Space, #A
    'BTN_WEST': None, # Y
    'BTN_SOUTH': Enter, #B
    'ABS_HAT0X': None, #Nav up or down
    'ABS_HAT0Y': None, #Nav left or right
    'ABS_X': ManageLeftStick, #Left stick left or right
    'ABS_Y': ManageLeftStick, #Left stick up or down
    'ABS_RX': ManageRightStick, #Right stick left or right
    'ABS_RY': ManageRightStick, #Right stick up or down
}

while True:
    events = []
    try:
        events = get_gamepad()
    except:
        event = []
    
    #Update states
    for event in events:
        if (event.ev_type == 'Sync'): continue
        Button_states[event.code] = event.state

    counter.UpdateCounter()
    LeftStickWriter.UpdateDirection()
    RightStickWriter.UpdateDirection()

    for event in events:
        if Mapping.get(event.code): Mapping[event.code](event.code)
     
    time.sleep(0.01)
