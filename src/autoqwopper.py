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
start_x, start_y = 520, 270
end_x, end_y = 1159, 668

frame = (start_x, start_y, end_x, end_y)

# Bounding box for the "metres" dialogue box
metres_start_x, metres_start_y = 170, 24
metres_end_x, metres_end_y = 413, 46

metres_box = (metres_start_x, metres_start_y, metres_end_x, metres_end_y)

# x, y coordinate of the ribbon that pops up when you die
ribbon_x, ribbon_y = 155, 125

ribbon_pixel = (ribbon_x, ribbon_y)

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

class AutoQwopper:   
    def __init__(self):
        self.update()
    
    def update(self):
        self.qwop_frame = ImageGrab.grab(frame)
        self.metres_frame = self.qwop_frame.crop(metres_box)

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

    def run(self):
        self.beginGame()
        if (self.isDead()):
            # restart game if this isn't the first time playing
            self.restartGame()
            self.update()
            self.getMetres()

        while (not self.isDead()):
            self.getMetres()
            self.randomKeyPress()
            time.sleep(0.25)
            self.update()
        print ("Went a total of " + str(self.metres) + " metres before dying.")

def main():
    qwopper = AutoQwopper()
    qwopper.run()
 
if __name__ == '__main__':
    main()