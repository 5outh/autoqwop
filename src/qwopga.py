from deap import base
from deap import creator
from deap import tools
import random
import math

#Luke Grantham
#python 3 compatible

#variables
IND_SIZE    = 5   #number of key presses
POP_SIZE    = 30   #number of individuals
T_SIZE      = 3   #tournament size
generations = 100 #number of generations
selb        = 1   #how many individuals to select when you call toolbox.selectBest
selw        = 5   #how many individuals to select whe nyou call toolbox.selectWorst
    
def evaluate(ind):
    return 0, #evaluate fitness of an individual

def generateGene():
    #generate a gene
    return chr(random.randint(65, 80))
    
def mutate(ind):
    #select a random character and randomize it
    #mutation as described in google's paper
    ind[random.randint(0, len(ind)-1)] = chr(random.randint(65, 80))
    return ind
    
def orderedx(list1, list2):
    result = [0 for x in range(len(list1))]
    
    point1 = random.randint(0, 4)
    point2 = random.randint(0, 4)
            
    if point2 < point1:
        temp = point1
        point1 = point2
        point2 = temp
    
    if(point2 == 4 and point1 == 0):
        #prevents child being the same as parent
        point2 = random.randint(0,3)

    #Order Crossover Step1: copy randomly selected
    #segment from first parent into offspring
    for x in range(point1, point2+1):
        result[x] = list1[x]
        
    list2newOrder = []
    for x in list2[point2+1:]:
        list2newOrder.append(x)
    for x in list2[:point2+1]:
        list2newOrder.append(x)
    
    #Order Crossover steop2: copy rest of alleles
    #in order they appear in second parent
    for x in list2newOrder:
        continueflag = 0
        for y in range(point2+1, len(list2)):
            if result[y] == 0:
                result[y] = x
                continueflag = 1
                break
        if(continueflag == 1):
            continueflag = 0
            continue
        for y in range(point2+1):
            if result[y] == 0:
                result[y] = x
                break
    
    return result
    
toolbox = base.Toolbox()
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness = creator.FitnessMax)

toolbox.register("individual", tools.initRepeat, creator.Individual, generateGene, n=IND_SIZE)

toolbox.register("select", tools.selTournament, k=2, tournsize=T_SIZE)
toolbox.register("onePoint", tools.cxOnePoint)
toolbox.register("twoPoint", tools.cxTwoPoint)
toolbox.register("orderedCross", myOrderedx)
toolbox.register("selectBest", tools.selBest, k=selb)
toolbox.register("selectWorst", tools.selWorst, k=selw)

population = [toolbox.individual() for i in range(POP_SIZE)] #generate population
#individuals are lists of chars A through P

for i in range(len(population)):
    #evaluate populations
    population[i].fitness.values = evaluate(population[i])
     
    
for i in range(generations):
    selected = toolbox.select(population)   #select
    
    parent1 = toolbox.clone(selected[0])
    parent2 = toolbox.clone(selected[1])
    
    child = orderedx(parent1, parent2) #crossover
    child = mutate(child)
    
    child.fitness.values = evaluate(child) #evaluate child
    
    population.remove(random.choice(toolbox.selectWorst(population))) #survivor select
    population.append(child) #replacement
    