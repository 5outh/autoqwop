import ImageGrab
import Image
import os
import time
 
start_x, start_y = 9, 105
end_x, end_y = 640 + start_x, 400 + start_y

metres_start_x, metres_start_y = 170, 24
metres_end_x, metres_end_y = 413, 50

def screenGrab():
    box = (start_x, start_y, end_x, end_y)
    im = ImageGrab.grab(box)
    impath = os.getcwd() + '\\qwop\\qwop__' + str(int(time.time())) + '.png' 
    im.save(impath, 'PNG')

    box = (metres_start_x, metres_start_y, metres_end_x, metres_end_y)

    metres = im.crop(box)
    metres_path = impath[:-4] + '_metres.png'

    metres.save(metres_path, 'PNG')

def main():
    screenGrab()
 
if __name__ == '__main__':
    main()