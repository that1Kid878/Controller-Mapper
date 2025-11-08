from inputs import get_gamepad
from pynput.keyboard import Key, Controller
import time
import tkinter as tk
import threading

# ----- Important lists -----#

Letters = [
    ['a','b','c','d'],
    ['e','f','g','h'],
    ['i','j','k','l'],
    ['m','n','o','p'],
    ['q','r','s','t'],
    ['u','v','w','x'],
    ['y','z', '', '']
]

Numbers = [
    [1,2,3,4],
    [5,6,7,8],
    [9,0,'',''],
    ['','','',''],
    ['','','',''],
    ['','','',''],
    ['','','','']
]

Symbols = [
    ['(', ')', '{', '}'],
    ['[',']', '_', "\""],
    [';', ':', '.', ','],
    ['#', '=', '!', '?'],
    ['+', '-', '*', '/'],
    ['<','>',"\\", "%"],
    ['@', '', '', '']
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

# ----- GUI Setup -----#
root = tk.Tk()
root.title("Controller Alphabet Cycler")
root.geometry("300x200")
root.attributes('-topmost', True)

tk.Label(root, text="Press R (Right Bumper) to cycle", font=("Arial", 14)).pack(pady=10)

display_label = tk.Label(root, text="", font=("Arial", 20))
display_label.pack()

# ----- Keybind Functions -----#

Alt = False
def AltBTN(code):
    global Alt
    if Button_states.get(code) == 0:
        Alt = False
    else:
        Alt = True

def Backspace(code):
    if Button_states.get(code) == 1:
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

def Selection(code):
    global Selected
    if Button_states.get(code) == 255:
        keyboard.press(Key.shift)
    elif Button_states.get(code) == 0:
        keyboard.release(Key.shift)

def CopyPaste(code):
    global Alt
    if Button_states.get(code) == 1:
        with keyboard.pressed(Key.ctrl):
            if Alt:
                keyboard.press('c')
            else:
                keyboard.press('v')

def UndoRedo(code):
    global Alt
    if Button_states.get(code) == 1:
        with keyboard.pressed(Key.ctrl):
            if Alt:
                keyboard.press('y')
            else:
                keyboard.press('z')

def Navigation(code):
    if Alt:
        with keyboard.pressed(Key.ctrl):
            if code == 'ABS_HAT0X':
                if Button_states.get(code) == 1:
                    keyboard.press(Key.right)
                if Button_states.get(code) == -1:
                    keyboard.press(Key.left)
            else:
                if Button_states.get(code) == 1:
                    keyboard.press(Key.down)
                if Button_states.get(code) == -1:
                    keyboard.press(Key.up)
    else:
        if code == 'ABS_HAT0X':
            if Button_states.get(code) == 1:
                keyboard.press(Key.right)
            if Button_states.get(code) == -1:
                keyboard.press(Key.left)
        else:
            if Button_states.get(code) == 1:
                keyboard.press(Key.down)
            if Button_states.get(code) == -1:
                keyboard.press(Key.up)

# ----- Classes -----#

class Counter():
    def __init__(self):
        self.ControllerCounter = 0
        self.last_press_time = time.time()
        self.CounterPressDelay = 2

    def CycleRows(self):
        display_label.config(text=" || ".join(Letters[self.ControllerCounter]) + '\n' + " || ".join(Symbols[self.ControllerCounter]))
        
    def IncrementCounter(self, code):
        if Button_states[code] != 1: return
        self.ControllerCounter = (self.ControllerCounter + 1) % 7
        self.last_press_time = time.time()
        self.CycleRows()

    def UpdateCounter(self):
        if time.time() - self.last_press_time > self.CounterPressDelay:
            self.ControllerCounter = 0
            self.last_press_time = time.time()
            self.CycleRows()

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

Mapping = {
    'ABS_RZ': Selection, #ZR
    'ABS_Z': AltBTN, #ZL
    'BTN_TL': CopyPaste, #L
    'BTN_TR': counter.IncrementCounter, #R
    'BTN_NORTH': Tab, #X
    'BTN_EAST': Space, #A
    'BTN_WEST': Backspace, # Y
    'BTN_SOUTH': Enter, #B
    'ABS_HAT0X': Navigation, #Nav up or down
    'ABS_HAT0Y': Navigation, #Nav left or right
    'ABS_X': ManageLeftStick, #Left stick left or right
    'ABS_Y': ManageLeftStick, #Left stick up or down
    'ABS_RX': ManageRightStick, #Right stick left or right
    'ABS_RY': ManageRightStick, #Right stick up or down
    'BTN_SELECT': UndoRedo #+
}

# ----- Execution -----#
events = []
def GetEvents():
    global events
    while True:
        events = get_gamepad()
        time.sleep(0.01)

def Update():
    while True:
        #Update states
        for event in events:
            if (event.ev_type == 'Sync'): continue
        
            Button_states[event.code] = event.state

        counter.UpdateCounter()
        LeftStickWriter.UpdateDirection()
        RightStickWriter.UpdateDirection()

        for event in events:
            if (event.ev_type == 'Sync'): continue
            if Mapping.get(event.code) != None:
                Mapping[event.code](event.code)
     
        time.sleep(0.01)

threading.Thread(target=Update, daemon=True).start()
threading.Thread(target=GetEvents, daemon=True).start()
root.after(0, counter.CycleRows)

root.mainloop()