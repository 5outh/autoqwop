from deap import base
from deap import creator
from deap import tools
import random
import math

#Luke Grantham
#python 3 compatible

#variables
IND_SIZE    = 5   #number of key presses
POP_SIZE    = 1   #number of individuals
T_SIZE      = 3   #tournament size
generations = 1000 #number of generations
selb        = 1   #how many individuals to select when you call toolbox.selectBest
selw        = 5   #how many individuals to select whe nyou call toolbox.selectWorst
    
def evaluate(ind):
	return 0,#evaluate fitness of an individual

def generateGene():
	#generate a gene
	return chr(random.randint(65, 80))
    
def mutate(ind):
    #select a random character and randomize it
    #mutation as described in google's paper
    ind[random.randint(0, len(ind)-1)] = chr(random.randint(65, 80))
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

population = [toolbox.individual() for i in range(POP_SIZE)] #generate population
#individuals are lists of chars A through P

for i in range(len(population)):
	#evaluate populations
    population[i].fitness.values = evaluate(population[i])
	 
    
for i in range(generations):
    selected = toolbox.select(population) 	#select
	
    parent1 = toolbox.clone(selected[0])
    parent2 = toolbox.clone(selected[1])
    
    child = toolbox.onePoint(parent1, parent2)[0] #crossover
    child = mutate(child)
    
    child.fitness.values = evaluate(child) #evaluate child
    
    population.remove(random.choice(toolbox.selectWorst(population))) #survivor select
    population.append(child) #replacement
    