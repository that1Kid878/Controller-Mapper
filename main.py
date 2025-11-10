from inputs import get_gamepad
from pynput.keyboard import Key, Controller
import time
import tkinter as tk
import threading
import math

# ----- Important lists -----#

Letters = [
    ['a','b','c','d','e','f','g','h'],
    ['i','j','k','l','m','n','o','p'],
    ['q','r','s','t','u','v','w','x'],
    ['y','z', '', '', '', '', '', '']
]

Numbers = [
    [1,2,3,4, 5,6,7,8],
    [9,0,'','','','','',''],
    [1,2,3,4, 5,6,7,8],
    [9,0,'','','','','',''],
]

Symbols = [
    ['(', ')', '{', '}','[',']', '_', "\""],
    [';', ':', '.', ',','#', '=', '!', '?'],
    ['+', '-', '*', '/', '<','>',"\\", "%"],
    ['@', '', '', '','', '', '', '']
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
root.geometry("400x650-0+100")
root.attributes('-topmost', True)

tk.Label(root, text="Press R (Right Bumper) to cycle", font=("Arial", 14)).pack(pady=10)

canvas = tk.Canvas(root, width=300, height=550, bg="#a3a3a3") 

#Texts
circle = canvas.create_oval(50,50,250,250,fill="#878787", outline = '')
arc = canvas.create_arc(50,50,250,250,fill="#878787",outline = '', start=22.5, extent=45) #"#515151"
text_radius = 0.7 * 100

corner_displacement = math.ceil((text_radius/math.sqrt(2)) * 1000) / 1000
Letter1 = canvas.create_text(150, 150 - text_radius, text='a', anchor='center', fill="#FFFFFF", justify='center', font= 24)
Letter2 = canvas.create_text(150 + corner_displacement, 150 - corner_displacement, text='b', anchor='center', fill="#FFFFFF", justify='center', font= 24)
Letter3 = canvas.create_text(150 + text_radius, 150, text='c', anchor='center', fill="#FFFFFF", justify='center', font= 24)
Letter4 = canvas.create_text(150 + corner_displacement, 150 + corner_displacement, text='d', anchor='center', fill="#FFFFFF", justify='center', font= 24)
Letter5 = canvas.create_text(150, 150 + text_radius, text='e', anchor='center', fill="#FFFFFF", justify='center', font= 24)
Letter6 = canvas.create_text(150 - corner_displacement, 150 + corner_displacement, text='f', anchor='center', fill="#FFFFFF", justify='center', font= 24)
Letter7 = canvas.create_text(150 - text_radius, 150, text='g', anchor='center', fill="#FFFFFF", justify='center', font= 24)
Letter8 = canvas.create_text(150 - corner_displacement, 150 - corner_displacement, text='h', anchor='center', fill="#FFFFFF", justify='center', font= 24)
LetterCycle = [Letter1, Letter2, Letter3, Letter4, Letter5, Letter6, Letter7, Letter8]

#Symbols
offset = 250
circle_sym = canvas.create_oval(50,50+offset,250,250+offset,fill="#878787", outline = '')
arc_sym = canvas.create_arc(50,50+offset,250,250+offset,fill="#878787",outline = '', start=22.5, extent=45)

Symbol1 = canvas.create_text(150, 150 - text_radius + offset, text='(', anchor='center', fill="#FFFFFF", justify='center', font=24)
Symbol2 = canvas.create_text(150 + corner_displacement, 150 - corner_displacement + offset, text=')', anchor='center', fill="#FFFFFF", justify='center', font=24)
Symbol3 = canvas.create_text(150 + text_radius, 150 + offset, text='{', anchor='center', fill="#FFFFFF", justify='center', font=24)
Symbol4 = canvas.create_text(150 + corner_displacement, 150 + corner_displacement + offset, text='}', anchor='center', fill="#FFFFFF", justify='center', font=24)
Symbol5 = canvas.create_text(150, 150 + text_radius + offset, text='[', anchor='center', fill="#FFFFFF", justify='center', font=24)
Symbol6 = canvas.create_text(150 - corner_displacement, 150 + corner_displacement + offset, text=']', anchor='center', fill="#FFFFFF", justify='center', font=24)
Symbol7 = canvas.create_text(150 - text_radius, 150 + offset, text='_', anchor='center', fill="#FFFFFF", justify='center', font=24)
Symbol8 = canvas.create_text(150 - corner_displacement, 150 - corner_displacement + offset, text='"', anchor='center', fill="#FFFFFF", justify='center', font=24)
SymbolCycle = [Symbol1, Symbol2, Symbol3, Symbol4, Symbol5, Symbol6, Symbol7, Symbol8]

canvas.pack()

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
        self.MaxValue = 4

    def UpdateRow(self):
        for i, TextLabel in enumerate(LetterCycle):
            canvas.itemconfig(TextLabel, text=Letters[self.ControllerCounter][i])
        for i, TextLabel in enumerate(SymbolCycle):
            canvas.itemconfig(TextLabel, text=Symbols[self.ControllerCounter][i])
        
    def IncrementCounter(self, code):
        if Button_states[code] != 1: return
        self.ControllerCounter = (self.ControllerCounter + 1) % self.MaxValue
        self.last_press_time = time.time()
        self.UpdateRow()

    def UpdateCounter(self):
        if time.time() - self.last_press_time > self.CounterPressDelay:
            self.ControllerCounter = 0
            self.last_press_time = time.time()
            self.UpdateRow()

counter = Counter()

keyboard = Controller()
class TypeWriter():
    def __init__(self, codeX, codeY, type):
        self.lastdirection = [0,0]
        self.direction = [0,0]
        self.type = type #0 for left, 1 for right
        self.Deadzone = 10000
        self.CenterRadius = 25000
        self.DiagRatio = 0.3
        self.codeX = codeX
        self.codeY = codeY
        self.LetterCode = 0
        self.has_written = True
        self.InvalidateUpdate = False

    def Centered(self):
        X = Button_states[self.codeX]
        Y = Button_states[self.codeY]

        return abs(X) < self.Deadzone and abs(Y) < self.Deadzone

    def UpdateDirection(self):
        if self.InvalidateUpdate: return
        X = Button_states[self.codeX]
        Y = Button_states[self.codeY]

        dx = 0
        dy = 0
        self.lastdirection = self.direction.copy()

        if abs(X) > abs(Y):
            if X > self.Deadzone:
                dx = 1
            elif X < -self.Deadzone:
                dx = -1
            if abs(Y) > self.Deadzone * self.DiagRatio:
                dy = 1 if Y > 0 else -1
        else:
            if Y > self.Deadzone:
                dy = 1
            elif Y < -self.Deadzone:
                dy = -1
            if abs(X) > self.Deadzone * self.DiagRatio:
                dx = 1 if X > 0 else -1

        self.direction = [dx, dy]

        #Update direction
        DirectionMode = {
            (0, 1): 0,     # UP
            (1, 1): 1,     # UP_RIGHT
            (1, 0): 2,     # RIGHT
            (1, -1): 3,    # DOWN_RIGHT
            (0, -1): 4,    # DOWN
            (-1, -1): 5,   # DOWN_LEFT
            (-1, 0): 6,    # LEFT
            (-1, 1): 7     # UP_LEFT
        }

        if math.pow(X,2) + math.pow(Y,2) >= math.pow(self.CenterRadius, 2):
            self.has_written = False

        if DirectionMode.get(tuple(self.direction)) != None:
            self.LetterCode = DirectionMode.get(tuple(self.direction))
            if self.type == 0:
                canvas.itemconfig(arc, start=67.5 - 45 * self.LetterCode, fill="#515151")
            elif self.type == 1:
                canvas.itemconfig(arc_sym, start=67.5 - 45 * self.LetterCode, fill="#515151")

    def DetectRelease(self):
        X = Button_states[self.codeX]
        Y = Button_states[self.codeY]
        if math.pow(X,2) + math.pow(Y,2) < math.pow(self.CenterRadius, 2):
            if self.has_written: return
            self.InvalidateUpdate = True
        if self.Centered():
            self.InvalidateUpdate = False
            if self.has_written: 
                canvas.itemconfig(arc if self.type == 0 else arc_sym, fill="#878787")
                return
            self.Write()
    def Write(self):
        if self.type == 0:
            letter = Letters[counter.ControllerCounter][self.LetterCode]
            if letter == None: return
            if Alt:
                letter = letter.upper()
            keyboard.type(letter)
            canvas.itemconfig(arc, fill="#878787")
            self.has_written = True
            
        elif self.type == 1:
            if Alt:
                number = Numbers[counter.ControllerCounter][self.LetterCode]
                if number == None: return
                keyboard.type(str(number))
                canvas.itemconfig(arc_sym, fill="#878787")
                self.has_written = True
            else:
                symbol = Symbols[counter.ControllerCounter][self.LetterCode]
                if symbol == None: return
                keyboard.type(symbol)
                canvas.itemconfig(arc_sym, fill="#878787")
                self.has_written = True

LeftStickWriter = TypeWriter('ABS_X', 'ABS_Y', 0)
RightStickWriter = TypeWriter('ABS_RX', 'ABS_RY', 1)

def ManageLeftStick(code):
    LeftStickWriter.DetectRelease()

def ManageRightStick(code):
    RightStickWriter.DetectRelease()

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
root.after(0, counter.UpdateRow)

root.mainloop()