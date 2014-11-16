import ImageGrab
import os
import time
 
start_x, start_y = 520, 270
end_x, end_y = 1159, 668

def screenGrab():
    box = (start_x, start_y, end_x, end_y)
    im = ImageGrab.grab(box)
    im.save(os.getcwd() + '\\qwop__' + str(int(time.time())) +
'.png', 'PNG')
 
def main():
    screenGrab()
 
if __name__ == '__main__':
    main()