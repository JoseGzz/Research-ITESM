# -*- coding: utf-8 -*-
import settings.qap_settings as settings
from data_readers.qap_data_reader import QapDataReader
from hyper_heuristics.h1 import H1
from hyper_heuristics.h2 import H2
from hyper_heuristics.h3 import H3
from hyper_heuristics.h4 import H4
from simulated_annealing import SimulatedAnnealing
import time
import random

if __name__ == "__main__":
    settings.init()
    random.seed(settings.options.seed)
    # algorithm configuration
    max_temp = settings.options.max_temp  # initial temperature
    min_temp = settings.options.min_temp  # final temperature
    eq_iter = settings.options.iters  # iterations at same temperature
    temp_change = settings.options.temp_rate  # temperature reduction factor
    # execute the algorithm
    filename = settings.options.data_filename
    if not filename:
        raise UserWarning("enter data filename through the -df flag.")
    
    if settings.options.hh == "H1":
        solver = SimulatedAnnealing(QapDataReader(), H1())
    if settings.options.hh == "H2":
        solver = SimulatedAnnealing(QapDataReader(), H2())
    if settings.options.hh == "H3":
        solver = SimulatedAnnealing(QapDataReader(), H3())
    if settings.options.hh == "H4":
        solver = SimulatedAnnealing(QapDataReader(), H4())
        
    best_solution = solver.solve(filename)
    
    print(best_solution)
    print(best_solution.cost())
    
    if settings.options.collect_filename:
        settings.collector.append_to_file(settings.options.collect_filename)
