# -*- coding: utf-8 -*-
import math
from data_readers.data_reader import DataReader
from hyper_heuristics.hyper_heuristic import HyperHeuristic
from solutions.solution import Solution
import random
import copy as cp
import settings.qap_settings as settings


class SimulatedAnnealing:
    @property
    def data_reader(self):
        return self._data_reader
    
    @property
    def hyper_heuristic(self):
        return self._hyper_heuristic

    @property
    def current_solution(self):
        return self._current_solution
    
    @property
    def max_temperature(self):
        return self._max_temperature

    @property
    def min_temperature(self):
        return self._min_temperature
    
    @property
    def iterations(self):
        return self._iterations

    @property
    def temp_change_rate(self):
        return self._temp_change_rate
    
    @current_solution.setter
    def current_solution(self, new_solution: Solution):
        self._current_solution = new_solution
        
    @max_temperature.setter
    def max_temperature(self, new_max_temperature: float):
        self._max_temperature = new_max_temperature

    @min_temperature.setter
    def min_temperature(self, new_min_temperature: float):
        self._min_temperature = new_min_temperature
        
    @iterations.setter
    def iterations(self, new_iterations):
        self._iterations = new_iterations
        
    @temp_change_rate.setter
    def temp_change_rate(self, new_temp_change_rate):
        self._temp_change_rate = new_temp_change_rate
    
    def __init__(self, data_reader: DataReader, hyper_heuristic: HyperHeuristic):
        self._data_reader = data_reader
        self._hyper_heuristic = hyper_heuristic
        self._current_solution = None
        self._max_temperature = 100
        self._min_temperature = 0.5
        self._iterations = 100
        self._temp_change_rate = 0.9
        self.eiter = 0
        self.plotter = None
    
    def solve(self, filename):
        self._current_solution = self.data_reader.read(filename)
        self.hyper_heuristic.register(self)

        ###################### START DATA COLLECTION ########################
        if settings.options.collect_data:
            settings.collector.new_entry()
            settings.collector.add_data("max_temperature", self.max_temperature)
            settings.collector.add_data("min_temperature", self.min_temperature)
            settings.collector.add_data("iter_per_temp", self.iterations)
            settings.collector.add_data("temp_change_ratio", self.temp_change_rate)
        ###################### END DATA COLLECTION ##########################

        temp = self.max_temperature
        best = cp.deepcopy(self.current_solution)
        worst = cp.deepcopy(self.current_solution)

        while float(temp) > self.min_temperature:
            self.eiter = 0
            while self.eiter < self.iterations:
                ###################### START DATA COLLECTION ########################
                if settings.options.collect_data:
                    settings.collector.new_entry()
                    settings.collector.add_data("iter_number_in_temp", self.eiter)
                    settings.collector.add_data("max_temperature", self.max_temperature)
                    settings.collector.add_data("min_temperature", self.min_temperature)
                    settings.collector.add_data("iter_per_temp", self.iterations)
                    settings.collector.add_data("temp_change_ratio", self.temp_change_rate)
                    settings.collector.add_data("current_temp", temp)
                ###################### END DATA COLLECTION ##########################
        
                candidate = self.__create_neighbor()
                #print(self.hyper_heuristic.get_heuristic(candidate))

                if self.__should_accept(candidate, temp):
                    self.current_solution = candidate
        
                if candidate.cost() > worst.cost():
                    worst = cp.deepcopy(candidate)

                ###################### START DATA COLLECTION ########################
                if settings.options.collect_data:
                    settings.collector.add_data("worst_makespan", worst.cost())
                ###################### END DATA COLLECTION ##########################
        
                if candidate.cost() < best.cost():
                    best = cp.deepcopy(candidate)
                    
                    if settings.options.trace:
                        self.plotter.plot(best)
                    
                #print(len(best.solution_space))

                ###################### START DATA COLLECTION ########################
                if settings.options.collect_data:
                    settings.collector.add_data("best_makespan", best.cost())
                    settings.collector.add_data("current_makespan", candidate.cost())
                ###################### END DATA COLLECTION ##########################
                
                #if settings.options.trace:
                #    print(" > iteration=%d, temp=%g, curr= %g, best=%g" %
                #        (self.eiter, temp, candidate.cost(), best.cost()))
                
                self.eiter += candidate.moved
                self.hyper_heuristic.add_best_makespan(best.cost())
                self.hyper_heuristic.iteration += candidate.moved
            temp *= self.temp_change_rate

        return best

    def __create_neighbor(self):
        """modifies the current solution"""
        candidate = cp.deepcopy(self.current_solution)
        candidate = cp.deepcopy(candidate.permute(self.hyper_heuristic.get_heuristic(candidate)))
        return candidate
    
    def __should_accept(self, candidate: Solution, temperature: float):
        """decides if candidate solution should substitute the current solution"""
        ncost = candidate.cost()
        ccost = self.current_solution.cost()
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
        
    def register_plotter(self, plotter):
        self.plotter = plotter
