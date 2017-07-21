# Simulated Annealing for Vehicle Routing Problems with Time Windows
# Author: Santiago E. Conant-Pablos, January 30, 2017

from QAP import QAP
import matplotlib.pyplot as plt
import time
import copy
import math
import random
import cProfile
import settings

def create_neighbor(current):
    """modifies the current solution"""
    candidate = copy.deepcopy(current)
    candidate = copy.deepcopy(candidate.create_neighbor())
    return candidate

def should_accept(candidate, current, temperature):
    """decides if candidate solution should substitute the current solution"""
    ncost = candidate.cost()
    ccost = current.cost()
    if ncost <= ccost:
        ###################### START DATA COLLECTION ########################
        if settings.options.collect_data:
            settings.collector.add_data("should_accept", True)
        ###################### END DATA COLLECTION ##########################
        return True
    else:
        result = math.exp((ccost - ncost) / temperature) >= random.random()

        ###################### START DATA COLLECTION ########################
        if settings.options.collect_data:
            settings.collector.add_data("should_accept", result)
            settings.collector.add_data("prob_acceptance", math.exp((ccost - ncost) / temperature))
        ###################### END DATA COLLECTION ##########################
        
        return result

def simulated_annealing(filename, max_temp, min_temp, eq_iter, temp_change,
                        trace=True):
    """implements the Simulated Annealing algorithm"""
    if trace:
        global fig
        fig = plt.figure()
        plt.ion()
        fig.canvas.set_window_title('Simulated Annealing')

    ###################### START DATA COLLECTION ########################
    if settings.options.collect_data:
        settings.collector.new_entry()
        settings.collector.add_data("max_temperature", max_temp)
        settings.collector.add_data("min_temperature", min_temp)
        settings.collector.add_data("iter_per_temp", eq_iter)
        settings.collector.add_data("temp_change_ratio", temp_change)
    ###################### END DATA COLLECTION ##########################
    
    problem = QAP()
    problem.read_data(filename)
    start_time = time.time()
    # current parece ser de tipo Solution
    current = problem.random_solution() #random_solution(problem)
    temp = max_temp
    best = copy.deepcopy(current)
    worst = copy.deepcopy(current)
    
    if trace:
        best.plot(fig)
        fig.canvas.draw()
        plt.pause(0.0001)
    i = 0
    while temp > min_temp:
        eiter = 0
        while eiter < eq_iter:
            i += 1

            ###################### START DATA COLLECTION ########################
            if settings.options.collect_data:
                settings.collector.new_entry()
                settings.collector.add_data("iter_number_in_temp", eiter)
                settings.collector.add_data("max_temperature", max_temp)
                settings.collector.add_data("min_temperature", min_temp)
                settings.collector.add_data("iter_per_temp", eq_iter)
                settings.collector.add_data("temp_change_ratio", temp_change)
                settings.collector.add_data("current_temp", temp)
            ###################### END DATA COLLECTION ##########################
            
            candidate = create_neighbor(current)
            
            ###################### START DATA COLLECTION ########################
            if settings.options.collect_data:
                settings.collector.add_data("num_jobs", len(candidate.facilities))
                settings.collector.add_data("num_machines", len(candidate.locations))
            ###################### END DATA COLLECTION ##########################
            
            if should_accept(candidate, current, temp):
                current = candidate
                
            if candidate.cost() > worst.cost():
                worst = copy.deepcopy(candidate)

            ###################### START DATA COLLECTION ########################
            if settings.options.collect_data:
                settings.collector.add_data("worst_makespan", worst.cost())
            ###################### END DATA COLLECTION ##########################
            
            if candidate.cost() < best.cost():
                best = copy.deepcopy(candidate)
                if trace:
                   best.plot(fig)
                   fig.canvas.draw()
                   plt.pause(0.0001)

            ###################### START DATA COLLECTION ########################
            if settings.options.collect_data:
               settings.collector.add_data("best_makespan", best.cost())
               settings.collector.add_data("current_makespan", candidate.cost())
            ###################### END DATA COLLECTION ##########################
            
            if trace:
                print(" > iteration=%d, temp=%g, curr= %g, best=%g" %
                      (i,temp,candidate.cost(), best.cost()))
            eiter += 1
        temp *= temp_change
    end_time = time.time()
    print("Execution time", end_time - start_time)
    if trace:
        best.plot(fig, True)
        plt.ioff()
    return best

if __name__ == "__main__":
    settings.init()
    # algorithm configuration
    max_temp = 100.0  # initial temperature
    min_temp = 0.05    # final temperature
    eq_iter = 100     # iterations at same temperature
    temp_change = 0.9  # temperature reduction factor
    # execute the algorithm    
    filename = settings.options.data_filename
    if not filename:
        raise UserWarning("enter data filename through the -df flag.")
        exit(1)
        
    trace = settings.options.trace
    best = simulated_annealing(filename, max_temp, min_temp, eq_iter, temp_change, trace)

    # store the data
    if settings.options.collect_filename:
        settings.collector.append_to_file(settings.options.collect_filename)
  
    #cProfile.run('simulated_annealing(filename, max_temp, min_temp, eq_iter,\
    #                           temp_change, True)')

    print(best.permutation())
    print(best.cost())
    plt.pause(1000)