import ImageGrab
import Image
import os
import time
import win32api, win32con

start_x, start_y = 520, 270
end_x, end_y = 1159, 668

metres_start_x, metres_start_y = 170, 24
metres_end_x, metres_end_y = 413, 46

def screenGrab():
    box = (start_x, start_y, end_x, end_y)
    im = ImageGrab.grab(box)
    impath = os.getcwd() + '\\qwop\\qwop__' + str(int(time.time())) + '.png' 
    im.save(impath, 'PNG')

    box = (metres_start_x, metres_start_y, metres_end_x, metres_end_y)

    metres = im.crop(box)
    metres_path = impath[:-4] + '_metres.png'

    metres.save(metres_path, 'PNG')

def leftDown():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    print 'left Down'
         
def leftUp():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(.1)
    print 'left release'

def leftClick(coords, duration=0):
    win32api.SetCursorPos((start_x + coords[0], start_y + coords[1]))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1 + duration)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    print "Click." #completely optional. But nice for debugging purposes.

def getCoords():
    x,y = win32api.GetCursorPos()
    x = x - start_x
    y = y - start_y
    print x,y

def beginGame():
    leftClick((10, 10))

def main():
    beginGame()
 
if __name__ == '__main__':
    main()