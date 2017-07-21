# -*- coding: utf-8 -*-
import settings.qap_settings as settings
from data_readers.tt_data_reader import TtDataReader
from hyper_heuristics.h1 import H1
from simulated_annealing import SimulatedAnnealing
import time
import random

from plotters.tt_plotter import TtPlotter

if __name__ == "__main__":
    settings.init()
    random.seed(time.time())
    # algorithm configuration
    max_temp = settings.options.max_temp  # initial temperature
    min_temp = settings.options.min_temp  # final temperature
    eq_iter = settings.options.iters  # iterations at same temperature
    temp_change = settings.options.temp_rate  # temperature reduction factor
    # execute the algorithm
    filename = settings.options.data_filename
    if not filename:
        raise UserWarning("enter data filename through the -df flag.")

    solver = SimulatedAnnealing(TtDataReader(), H1())
    solver.register_plotter(TtPlotter())
    best_solution = solver.solve(filename)
    # TODO: remove this line.
    #solution = solver.data_reader.read(filename)
    #plotter = TtPlotter()
    #plotter.plot(solution)
    
    # print(best_solution)
    # print(best_solution.cost())
