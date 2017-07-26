# -*- coding: utf-8 -*-
import settings.qap_settings as settings
from data_readers.tt_data_reader import TtDataReader
from hyper_heuristics.h1 import H1
from simulated_annealing import SimulatedAnnealing
from TT.Classes.solutions.tt_solution.restrictions.different_time import DifferentTime
from TT.Classes.solutions.tt_solution.restrictions.precedence import Precedence
from TT.Classes.solutions.tt_solution.restrictions.preference_room import PreferenceRoom
from TT.Classes.solutions.tt_solution.restrictions.room_cost import RoomCost
from TT.Classes.solutions.tt_solution.restrictions.same_instructor import SameInstructor
from TT.Classes.solutions.tt_solution.restrictions.same_room_and_time import SameRoomAndTime
from TT.Classes.solutions.tt_solution.restrictions.same_students import SameStudents
from TT.Classes.solutions.tt_solution.restrictions.spread import Spread
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

    constraints = [SameRoomAndTime(), SameStudents(), DifferentTime(), Precedence(), SameInstructor(),
                   Spread()]
    soft_constraints = [RoomCost(), PreferenceRoom()]
    
    solver = SimulatedAnnealing(TtDataReader(), H1())
    plotter = TtPlotter()
    plotter.register_constraints(constraints)
    plotter.register_soft_constraints(soft_constraints)
    solver.register_plotter(plotter)
    solver.register_constraints(constraints)
    solver.register_soft_constraints(soft_constraints)
    best_solution = solver.solve(filename)

    # print(best_solution)
    # print(best_solution.cost())
