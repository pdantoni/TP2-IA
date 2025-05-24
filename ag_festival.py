# Funciones DEAP

from deap import algorithms, base, creator, tools
from festival import CANT_CHEF, TAM_CHEF
from festival import imprimir_ind, evaluar_aptitud, crear_ind
import numpy

import matplotlib.pyplot as plt

#Busca el menor peso
creator.create("FitnessMax", base.Fitness, weights = (1.0,))

#Crea individuo
creator.create("Individual", list,  fitness=creator.FitnessMax)
creator.create("Strategy", list, typecode="d")

#Registra
toolbox = base.Toolbox()

IND_SIZE = TAM_CHEF * CANT_CHEF

#funcion creadora de individuo
toolbox.register("individual", crear_ind, creator.Individual, creator.Strategy)
#funcion creadora de poblacion
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
#funcion evaluadora de pesos
toolbox.register("evaluate", evaluar_aptitud)
toolbox.register("select", tools.selTournament, tournsize = 4)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate",  tools.mutUniformInt, low=1, up=5, indpb=0.1)

npop = 1000 # tamaño población
pop = toolbox.population(n=npop)

hof = tools.HallOfFame(1)
stats = tools.Statistics(lambda ind: ind.fitness.values)

stats.register("avg", lambda fits: numpy.mean([f[0] for f in fits]))
stats.register("std", numpy.std, axis=0)
stats.register("min", numpy.min, axis=0)
stats.register("max", numpy.max, axis=0)

# Evolution
ngen = 50 # número de generaciones
cxpb = 0.7 # probabilidad de cruce
mutpb = 0.3 # probabilidad de mutación
# la suma de cxpb + mutpb =< 1.0
pop, logbook = algorithms.eaMuPlusLambda(pop, toolbox, mu=npop, lambda_=npop, cxpb=cxpb, mutpb=mutpb, ngen=ngen, stats=stats, halloffame=hof)

best_solution = tools.selBest(pop, 1)[0]
print("\nMejor solución:")
print(best_solution)
print("\t")

imprimir_ind(best_solution)

fitness_ag = hof[0].fitness.values[0]        # p.e.  forty puntos
porcentaje = (fitness_ag / 55) * 100
print(f"El AG cumplió el {porcentaje:.1f}% de las condiciones.")

# History AVG
plt.figure(figsize=(10,8))
front = numpy.array([(c['gen'], c['avg']) for c in logbook])
plt.plot(front[:,0][1:-1], front[:,1][1:-1], "-bo")
plt.axis("tight")
plt.show()