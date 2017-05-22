# Simulated Annealing for Vehicle Routing Problems with Time Windows
# Author: Santiago E. Conant-Pablos, January 30, 2017

from jssp import JSSP
import matplotlib.pyplot as plt
import time
import copy
import math
import random

def create_neighbor(current):
    """modifies the current solution"""
    candidate = copy.deepcopy(current)
    # escribir el código que perturba a la solución candidata
    return candidate

def should_accept(candidate, current, temperature):
    """decides if candidate solution should substitute the current solution"""
    ncost = candidate.cost()
    ccost = current.cost()
    if ncost <= ccost:
        return True
    else:
        return math.exp((ccost - ncost) / temperature) >= random.random()

def simulated_annealing(filename, max_temp, min_temp, eq_iter, temp_change,
                        trace=True):
    """implements the Simulated Annealing algorithm"""
    if trace:
        global fig
        plt.ion()
        fig = plt.figure()
        fig.canvas.set_window_title('Simulated Annealing')
    problem = JSSP()
    problem.read_data(filename)
    start_time = time.time()
    # current parece ser de tipo Solution
    current = problem.random_solution() #random_solution(problem)
    temp = max_temp
    best = copy.deepcopy(current)
    if trace:
        best.plot()
        fig.canvas.draw()
        plt.pause(0.0001)
    i = 0
    while temp > min_temp:
        eiter = 0
        while eiter < eq_iter:
            i += 1
            candidate = current.create_neighbor() #create_neighbor(current)
            if should_accept(candidate, current, temp): current = candidate
            if candidate.cost() < best.cost():
                best = copy.deepcopy(candidate)
                if trace:
                    best.plot()
                    fig.canvas.draw()
                    plt.pause(0.0001)
            if trace:
                print(" > iteration=%d, temp=%g, curr= %g, best=%g" %
                      (i,temp,candidate.cost(), best.cost()))
            eiter += 1
        temp *= temp_change
    end_time = time.time()
    print("Execution time", end_time - start_time)
    if trace:
        best.plot(True)
        plt.ioff()
    return best

if __name__ == "__main__":
    # algorithm configuration
    max_temp =  30.0   # initial temperature
    min_temp = 4.0     # final temperature
    eq_iter = 30       # iterations at same temperature
    temp_change = 0.9  # temperature reduction factor
    # execute the algorithm    
    filename = input("Nombre del archivo del problema? ")
    best = simulated_annealing(filename, max_temp, min_temp, eq_iter,
                               temp_change, True)
    print(best.cost())