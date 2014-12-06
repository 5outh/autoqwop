import ImageGrab
import Image
import os
import time
from random import *
import win32api, win32con
import threading
from pytesser import *
from deap import base
from deap import creator
from deap import tools
import numpy
import math

# Globals

# DEAP stuff
IND_SIZE    = 5   #number of key presses
POP_SIZE    = 1  #number of individuals
T_SIZE      = 3   #tournament size
generations = 1000 #number of generations
selb        = 1   #how many individuals to select when you call toolbox.selectBest
selw        = 5   #how many individuals to select whe nyou call toolbox.selectWorst

# QWOP stuff
# Bounding box for QWOP
start_x, start_y = 9, 105
end_x, end_y = 640 + start_x, 400 + start_y

frame = (start_x, start_y, end_x, end_y)

# Bounding box for the "metres" dialogue box
metres_start_x, metres_start_y = 170, 24
metres_end_x, metres_end_y = 413, 50

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
    'O': (True, True, True, True),
    None: (False, False, False, False)
}

# Key codes
VK_CODE = {
    'SPACE':0x20,
    'O':0x4F,
    'P':0x50,
    'Q':0x51,
    'W':0x57
    }

def sendKey(key, duration=0.1, up=True):
    win32api.keybd_event(key, 0, 0, 0)
    time.sleep(duration)
    if(up):
        win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)

def leftClick(coords, duration=0.1, up=True):
    win32api.SetCursorPos((start_x + coords[0], start_y + coords[1]))
    
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    
    time.sleep(duration)
    if (up):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def sendKeys(keys):
    """
    Send a list of (key, duration) pairs concurrently
    """
    threads = []
    for (key, duration, up) in keys:
        t = threading.Thread(target=sendKey, args=(VK_CODE[key], duration, up))
        threads.append(t)
    for thread in threads:
        thread.start()

def sendQwopCode(key, next=None):
    """
    Send a QWOP-encoded key to the game. 
    """
    (q, w, o, p) = QWOP_CODE[key]
    (_q, _w, _o, _p) = QWOP_CODE[next]

    keys = []

    if q:
        keys.append(('Q', 0.15, not _q))
    if w:
        keys.append(('W', 0.15, not _w))
    if o:
        keys.append(('O', 0.15, not _o))
    if p:
        keys.append(('P', 0.15, not _p))

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
    
    def getMetres(self):
        metres = float(image_to_string(self.metres_frame)[:-9].replace(' ', ''))
        self.metres = metres

    def update(self):
        self.qwop_frame = ImageGrab.grab(frame)
        self.metres_frame = self.qwop_frame.crop(metres_box)
        self.getMetres()

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

    def run(self, qwopString):
        self.beginGame()
        if (self.isDead()):
            # restart game if this isn't the first time playing
            self.restartGame()
            self.update()
            self.getMetres()
        
        print ("Evaluating qwop string: " + "".join(qwopString))

        start = time.time()
        running = True

        while running:
            for qwopCode, next in zip(qwopString, qwopString[1:] + [None]):

                sendQwopCode(qwopCode, next)
                self.update()

                if (self.isDead()):
                    running = False
                    # Set fitness to 0 if crashed
                    # self.metres = 0
                    print("Qwopper died")
                    break

                if (time.time() - start > 60):
                    running = False
                    print("Time exceeded")
                    # Do one final update
                    time.sleep(0.5)
                    self.update()
                    break

        if (not self.isDead()):
            self.die()

        print ("Went a total of " + str(self.metres) + " metres before dying.")
        
        time.sleep(2)

        return self.metres

# The main GA

def evaluate(ind):
    qwopper = AutoQwopper()
    return qwopper.run(ind),

def generateGene():
    #generate a gene
    return chr(randint(65, 80))

def mutate(ind):
    #select a random character and randomize it
    #mutation as described in google's paper
    ind[randint(0, len(ind)-1)] = chr(randint(65, 80))
    return ind

toolbox = base.Toolbox()
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness = creator.FitnessMax)

toolbox.register("individual", tools.initRepeat, creator.Individual, generateGene, n=IND_SIZE)

toolbox.register("select", tools.selTournament, k=2, tournsize=T_SIZE)
toolbox.register("onePoint", tools.cxOnePoint)
toolbox.register("twoPoint", tools.cxTwoPoint)
toolbox.register("selectBest", tools.selBest, k=selb)
toolbox.register("selectWorst", tools.selWorst, k=selw)

# GENERATE STATISTICS
stats = tools.Statistics(key=lambda ind: ind.fitness.values)
hallOfFame = tools.HallOfFame(1)
logbook = tools.Logbook()

stats.register('max', max)
stats.register('min', min)
stats.register('mean', numpy.mean)

def updateStatistics(population, generation):
    hallOfFame.update(population)
    record = stats.compile(population)
    record['best'] = "".join(hallOfFame[0])
    record['generation'] = generation
    logbook.record(**record)

def main():
    population = [toolbox.individual() for i in range(POP_SIZE)] #generate population

    for i in range(len(population)):
        #evaluate populations
        population[i].fitness.values = evaluate(population[i])
     
    for i in range(generations):

        updateStatistics(population, i)
        
        print(logbook)

        selected = toolbox.select(population)   #select
        
        parent1 = toolbox.clone(selected[0])
        parent2 = toolbox.clone(selected[1])
        
        child = toolbox.onePoint(parent1, parent2)[0] #crossover
        child = mutate(child)
        
        child.fitness.values = evaluate(child) #evaluate child

        population.remove(choice(toolbox.selectWorst(population))) #survivor select
        population.append(child) #replacement
 
if __name__ == '__main__':
    main()