import ImageGrab
import Image
import os
import time
from random import *
import win32api, win32con
import threading
from pytesser import *

# Globals

# Bounding box for QWOP
start_x, start_y = 9, 105
end_x, end_y = 640 + start_x, 400 + start_y

frame = (start_x, start_y, end_x, end_y)

# Bounding box for the "metres" dialogue box
metres_start_x, metres_start_y = 170, 24
metres_end_x, metres_end_y = 413, 46

metres_box = (metres_start_x, metres_start_y, metres_end_x, metres_end_y)

# x, y coordinate of the ribbon that pops up when you die
ribbon_x, ribbon_y = 155, 125

ribbon_pixel = (ribbon_x, ribbon_y)

# QWOP codes
QWOP_CODE = {
    'P': (False, False, False, False),
    'D': (False, False, False, True),
    'C': (False, False, True, False),
    'J': (False, False, True, True),
    'B': (False, True, False, False),
    'I': (False, True, False, True),
    'H': (False, True, True, False),
    'N': (False, True, True, True),
    'A': (True, False, False, False),
    'G': (True, False, False, True),
    'F': (True, False, True, False),
    'M': (True, False, True, True),
    'E': (True, True, False, False),
    'L': (True, True, False, True),
    'K': (True, True, True, False),
    'O': (True, True, True, True)
}

# Key codes
VK_CODE = {
    'SPACE':0x20,
    'O':0x4F,
    'P':0x50,
    'Q':0x51,
    'W':0x57
    }

def sendKey(key, duration=0.1):
    win32api.keybd_event(key, 0, 0, 0)
    time.sleep(duration)
    win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)

def leftClick(coords, duration=0.1):
    win32api.SetCursorPos((start_x + coords[0], start_y + coords[1]))
    
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    
    time.sleep(duration)
    
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def sendKeys(keys):
    """
    Send a list of (key, duration) pairs concurrently
    """
    threads = []
    for (key, duration) in keys:
        t = threading.Thread(target=sendKey, args=(VK_CODE[key], duration))
        threads.append(t)
    for thread in threads:
        thread.start()

def sendQwopCode(key):
    """
    Send a QWOP-encoded key to the game. 
    """
    (q, w, o, p) = QWOP_CODE[key]
    keys = []

    if q:
        keys.append(('Q', 0.15))
    if w:
        keys.append(('W', 0.15))
    if o:
        keys.append(('O', 0.15))
    if p:
        keys.append(('P', 0.15))

    # Send the keys
    sendKeys(keys)

    # wait for them to finish before moving on to the next one
    time.sleep(0.15)

def getRandomQwopString(numChars=5):
    qwopString = ""
    for i in xrange(numChars):
        qwopString += chr(randint(65, 80))
    return qwopString

class AutoQwopper:   
    def __init__(self):
        self.update()
    
    def update(self):
        self.qwop_frame = ImageGrab.grab(frame)
        self.metres_frame = self.qwop_frame.crop(metres_box)

    def die(self):
        print('Killing qwopper.')
        sendKey(VK_CODE['Q'], duration=1.5)
        sendKey(VK_CODE['W'], duration=1.5)

    def isDead(self):
        return (self.qwop_frame.getpixel(ribbon_pixel) == (255, 255, 0))

    def beginGame(self):
        leftClick((100, 100))

    def restartGame(self):
        sendKey(VK_CODE['SPACE'])

    def getMetres(self):
        metres = float(image_to_string(self.metres_frame)[:-9])
        self.metres = metres

    def randomKeyPress(self):
        keys = ['Q', 'W', 'O', 'P']

        # Send up to all 4 keys in parallel
        for i in xrange(4):
            if (random() < 0.5):
                key = keys[i]

                print ("Pressing key: " + key)

                duration = random() + 0.5

                t = threading.Thread(target=sendKey, args=(VK_CODE[key], duration))
                t.start()

    def run(self, qwopString):
        self.beginGame()
        if (self.isDead()):
            # restart game if this isn't the first time playing
            self.restartGame()
            self.update()
            self.getMetres()
        
        print ("Evaluating qwop string: " + qwopString)

        start = time.time()
        running = True

        while running:
            for qwopCode in qwopString:
                
                sendQwopCode(qwopCode)
                self.update()

                if (self.isDead()):
                    running = False
                    # Set fitness to 0 if crashed
                    self.metres = 0
                    print("Qwopper died")
                    break

                if (time.time() - start > 60 * 1000):
                    running = False
                    print("Time exceeded")
                    # Do one final update
                    time.sleep(0.5)
                    self.update()
                    break

        if (not self.isDead()):
            self.die()

        print ("Went a total of " + str(self.metres) + " metres before dying.")

        return self.metres

def evaluate(ind):
    qwopper = AutoQwopper()
    return qwopper.run(ind)

def main():
    qwopper = AutoQwopper()
    qwopper.run(getRandomQwopString(15))
 
if __name__ == '__main__':
    main()