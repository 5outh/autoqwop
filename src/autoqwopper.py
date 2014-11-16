import ImageGrab
import Image
import os
import time
import win32api, win32con

### GLOBALS

# Bounding box for QWOP
start_x, start_y = 520, 270
end_x, end_y = 1159, 668

# Bounding box for the "metres" dialogue box
metres_start_x, metres_start_y = 170, 24
metres_end_x, metres_end_y = 413, 46

# x, y coordinate of the ribbon that pops up when you die
ribbon_x, ribbon_y = 155, 125

VK_CODE = {
    'SPACE':0x20,
    'O':0x4F,
    'P':0x50,
    'Q':0x51,
    'W':0x57
    }

# TODO: Implement
class AutoQwopper:
    pass

def screenGrab():
    box = (start_x, start_y, end_x, end_y)
    im = ImageGrab.grab(box)
    impath = os.getcwd() + '\\qwop\\qwop__' + str(int(time.time())) + '.png' 
    im.save(impath, 'PNG')

    isDead(im);

    box = (metres_start_x, metres_start_y, metres_end_x, metres_end_y)

    metres = im.crop(box)
    metres_path = impath[:-4] + '_metres.png'

    metres.save(metres_path, 'PNG')

    return im

def leftClick(coords, duration=0.1):
    win32api.SetCursorPos((start_x + coords[0], start_y + coords[1]))
    
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    
    time.sleep(duration)
    
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def sendKey(key, duration=0.1):
    win32api.keybd_event(key, 0, 0, 0)
    time.sleep(duration)
    win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)

def getCoords():
    x,y = win32api.GetCursorPos()
    x = x - start_x
    y = y - start_y
    print x,y

def beginGame():
    leftClick((10, 10))

def restartGame():
    sendKey(VK_CODE['SPACE'])

def isDead(image):
    return (image.getpixel((ribbon_x, ribbon_y)) == (255, 255, 0))

def main():
    beginGame()
    im = screenGrab()
    while (not isDead(im)):
        time.sleep(0.5)
        im = screenGrab()
    restartGame()
 
if __name__ == '__main__':
    main()