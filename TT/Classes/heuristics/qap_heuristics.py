# -*- coding: utf-8 -*-
from heuristics.heuristic import Heuristic
from solutions.qap_solution import QapSolution
from solutions.solution import Solution
import random
import copy as cp
import settings.qap_settings as settings


class RandomMove(Heuristic):
    def __init__(self, solver):
        self.solver = solver
        
    def permute(self, solution: QapSolution):
        # escogemos dos facilities al azar
        fac1, fac2 = random.sample(solution.p, 2)
        # las intercambiamos
        fac1_index, fac2_index = solution.p.index(fac1), solution.p.index(fac2)

        ###################### START DATA COLLECTION ########################
        if settings.options.collect_data:
            if fac1_index == 0 or fac2_index == 0:
                settings.collector.add_data("first_fac_moved", True)
            else:
                settings.collector.add_data("first_fac_moved", False)
    
            if fac1_index == len(solution.p) - 1 or fac2_index == len(solution.p) - 1:
                settings.collector.add_data("last_fac_moved", True)
            else:
                settings.collector.add_data("last_fac_moved", False)
    
            settings.collector.add_data("moves", abs(fac1_index - fac2_index))
        ###################### END DATA COLLECTION ##########################

        solution.p[fac2_index], solution.p[fac1_index] = solution.p[fac1_index], solution.p[fac2_index]
        solution.calculate_cost()
        solution.moved = 1
        return solution


class BestMoveGreedy(Heuristic):
    @property
    def k(self):
        return self._k
    
    def __init__(self, k, solver):
        self._k = k
        self.solver = solver
        
    def permute(self, solution: QapSolution):
        result = solution
        moved = 0

        ###################### START DATA COLLECTION ########################
        if settings.options.collect_data:
            data = []
        ###################### END DATA COLLECTION ##########################
        
        for i in range(self.k):
            ###################### START DATA COLLECTION ########################
            if settings.options.collect_data:
                data.append({})
            ###################### END DATA COLLECTION ##########################
            candidate = cp.deepcopy(solution)
            # escogemos dos facilities al azar
            fac1, fac2 = random.sample(candidate.p, 2)
            # las intercambiamos
            fac1_index, fac2_index = candidate.p.index(fac1), candidate.p.index(fac2)

            ####################### START DATA COLLECTION ########################
            if settings.options.collect_data:
                if fac1_index != 0 and fac1_index != len(solution.p) - 1 and fac2_index != 0 and \
                                fac2_index != len(solution.p) - 1:
                    data[i]["first_fac_moved"] = False
                    data[i]["last_fac_moved"] = False
                else:
                    if fac1_index == 0 or fac2_index == 0:
                        data[i]["first_fac_moved"] = True
                    else:
                        data[i]["first_fac_moved"] = False

                    if fac1_index == len(solution.p) - 1 or fac2_index == len(solution.p) - 1:
                        data[i]["last_fac_moved"] = True
                    else:
                        data[i]["last_fac_moved"] = False

                data[i]["moves"] = abs(fac1_index - fac2_index)
            ###################### END DATA COLLECTION ##########################
            
            candidate.p[fac2_index], candidate.p[fac1_index] = candidate.p[fac1_index], candidate.p[fac2_index]
            candidate.calculate_cost()
            moved += 1
            if candidate.cost() < result.cost():
                candidate.moved = moved

                ###################### START DATA COLLECTION ########################
                if settings.options.collect_data:
                    fields = ["first_fac_moved", "last_fac_moved", "moves"]
                    for field in fields:
                        entry = ""
                        for j in range(self.k):
                            entry += str(data[j][field]) + "|"
                        settings.collector.add_data(field, entry)
                ###################### END DATA COLLECTION ##########################
                
                return candidate
        
        result.moved = moved
        
        ###################### START DATA COLLECTION ########################
        if settings.options.collect_data:
            fields = ["first_fac_moved", "last_fac_moved", "moves"]
            for field in fields:
                entry = ""
                for j in range(self.k):
                    entry += str(data[j][field]) + "|"
                settings.collector.add_data(field, entry)
        ###################### END DATA COLLECTION ##########################
        
        return result


class BestMove(Heuristic):
    @property
    def k(self):
        return self._k

    def __init__(self, k, solver):
        self._k = k
        self.solver = solver

    def permute(self, solution: QapSolution):
        result = None
        moved = 0

        ###################### START DATA COLLECTION ########################
        if settings.options.collect_data:
            data = []
        ###################### END DATA COLLECTION ##########################
        for i in range(self.k):
            ###################### START DATA COLLECTION ########################
            if settings.options.collect_data:
                data.append({})
            ###################### END DATA COLLECTION ##########################
            
            candidate = cp.deepcopy(solution)
            # escogemos dos facilities al azar
            fac1, fac2 = random.sample(candidate.p, 2)
            # las intercambiamos
            fac1_index, fac2_index = candidate.p.index(fac1), candidate.p.index(fac2)

            ####################### START DATA COLLECTION ########################
            if settings.options.collect_data:
                if fac1_index != 0 and fac1_index != len(solution.p) - 1 and fac2_index != 0 and \
                                fac2_index != len(solution.p) - 1:
                    data[i]["first_fac_moved"] = False
                    data[i]["last_fac_moved"] = False
                else:
                    if fac1_index == 0 or fac2_index == 0:
                        data[i]["first_fac_moved"] = True
                    else:
                        data[i]["first_fac_moved"] = False
        
                    if fac1_index == len(solution.p) - 1 or fac2_index == len(solution.p) - 1:
                        data[i]["last_fac_moved"] = True
                    else:
                        data[i]["last_fac_moved"] = False
    
                data[i]["moves"] = abs(fac1_index - fac2_index)
            ###################### END DATA COLLECTION ##########################
        
            candidate.p[fac2_index], candidate.p[fac1_index] = candidate.p[fac1_index], candidate.p[fac2_index]
            candidate.calculate_cost()
            moved += 1
            if result is None:
                result = candidate
            elif candidate.cost() < result.cost():
                result = candidate
    
        result.moved = moved

        ###################### START DATA COLLECTION ########################
        if settings.options.collect_data:
            fields = ["first_fac_moved", "last_fac_moved", "moves"]
            for field in fields:
                entry = ""
                for j in range(self.k):
                    entry += str(data[j][field]) + "|"
                settings.collector.add_data(field, entry)
        ###################### END DATA COLLECTION ##########################
        
        return result


class FirstMove(Heuristic):
    @property
    def k(self):
        return self._k
    
    def __init__(self, k, solver):
        self._k = k
        self.solver = solver
    
    def permute(self, solution: QapSolution):
        result = solution
        moved = 0
        
        ###################### START DATA COLLECTION ########################
        if settings.options.collect_data:
            data = []
        ###################### END DATA COLLECTION ##########################
        for i in range(self.k):
            ###################### START DATA COLLECTION ########################
            if settings.options.collect_data:
                data.append({})
            ###################### END DATA COLLECTION ##########################
            
            candidate = cp.deepcopy(solution)
            # escogemos dos facilities al azar
            fac1, fac2 = random.sample(candidate.p, 2)
            # las intercambiamos
            fac1_index, fac2_index = candidate.p.index(fac1), candidate.p.index(fac2)

            ####################### START DATA COLLECTION ########################
            if settings.options.collect_data:
                if fac1_index != 0 and fac1_index != len(solution.p) - 1 and fac2_index != 0 and \
                                fac2_index != len(solution.p) - 1:
                    data[i]["first_fac_moved"] = False
                    data[i]["last_fac_moved"] = False
                else:
                    if fac1_index == 0 or fac2_index == 0:
                        data[i]["first_fac_moved"] = True
                    else:
                        data[i]["first_fac_moved"] = False
        
                    if fac1_index == len(solution.p) - 1 or fac2_index == len(solution.p) - 1:
                        data[i]["last_fac_moved"] = True
                    else:
                        data[i]["last_fac_moved"] = False
    
                data[i]["moves"] = abs(fac1_index - fac2_index)
            ###################### END DATA COLLECTION ##########################
            
            candidate.p[fac2_index], candidate.p[fac1_index] = candidate.p[fac1_index], candidate.p[fac2_index]
            candidate.calculate_cost()
            moved += 1
            if candidate.cost() < result.cost():
                candidate.moved = moved

                ###################### START DATA COLLECTION ########################
                if settings.options.collect_data:
                    fields = ["first_fac_moved", "last_fac_moved", "moves"]
                    for field in fields:
                        entry = ""
                        for j in range(self.k):
                            entry += str(data[j][field]) + "|"
                        settings.collector.add_data(field, entry)
                ###################### END DATA COLLECTION ##########################
                
                return candidate
        
        result.moved = moved

        ###################### START DATA COLLECTION ########################
        if settings.options.collect_data:
            fields = ["first_fac_moved", "last_fac_moved", "moves"]
            for field in fields:
                entry = ""
                for j in range(self.k):
                    entry += str(data[j][field]) + "|"
                settings.collector.add_data(field, entry)
        ###################### END DATA COLLECTION ##########################
        
        return result


class SequentialSearch(Heuristic):
    def __init__(self, solver):
        self.solver = solver
        
    def permute(self, solution: QapSolution):
        result = solution
        moved = 0
        for i in range(len(solution.facilities) - 1):
            candidate = cp.deepcopy(solution)
            # escogemos dos facilities al azar
            fac1, fac2 = candidate.p[i], candidate.p[i + 1]
            # las intercambiamos
            fac1_index, fac2_index = candidate.p.index(fac1), candidate.p.index(fac2)
            
            candidate.p[fac2_index], candidate.p[fac1_index] = candidate.p[fac1_index], candidate.p[fac2_index]
            candidate.calculate_cost()
            moved += 1
            
            if candidate.cost() < result.cost():
                candidate.moved = moved
                ###################### START DATA COLLECTION ########################
                if settings.options.collect_data:
                    settings.collector.add_data("times_moved", moved)
                ###################### END DATA COLLECTION ##########################
                return candidate
            
        result.moved = moved
        ###################### START DATA COLLECTION ########################
        if settings.options.collect_data:
            settings.collector.add_data("times_moved", moved)
        ###################### END DATA COLLECTION ##########################
        return result


class ReverseSequentialSearch(Heuristic):
    def __init__(self, solver):
        self.solver = solver
        
    def permute(self, solution: QapSolution):
        result = solution
        moved = 0
        for i in range(len(solution.facilities) - 1):
            candidate = cp.deepcopy(solution)
            # escogemos dos facilities al azar
            index = len(solution.facilities) - 1
            fac1, fac2 = candidate.p[index - i], candidate.p[index - i - 1]
            # las intercambiamos
            fac1_index, fac2_index = candidate.p.index(fac1), candidate.p.index(fac2)
            
            candidate.p[fac2_index], candidate.p[fac1_index] = candidate.p[fac1_index], candidate.p[fac2_index]
            candidate.calculate_cost()
            moved += 1
            
            if candidate.cost() < result.cost():
                candidate.moved = moved
                ###################### START DATA COLLECTION ########################
                if settings.options.collect_data:
                    settings.collector.add_data("times_moved", moved)
                ###################### END DATA COLLECTION ##########################
                return candidate
        
        result.moved
        ###################### START DATA COLLECTION ########################
        if settings.options.collect_data:
            settings.collector.add_data("times_moved", moved)
        ###################### END DATA COLLECTION ##########################
        return result
    
    
class DoubleExchange(Heuristic):
    def __init__(self, solver):
        self.solver = solver
        
    def permute(self, solution: QapSolution):
        candidate = cp.deepcopy(solution)
        # escogemos dos facilities al azar
        fac1, _ = random.sample(candidate.p, 2)
        
        # caso en el que fac1 es el primer elemento
        # las intercambiamos
        fac1_index = candidate.p.index(fac1)
        
        if fac1_index < 3:
            fac2_index = fac1_index + 1
            fac3_index = fac1_index + 2
            fac4_index = fac1_index + 3
        elif fac1_index > len(candidate.facilities) - 4:
            fac2_index = fac1_index - 1
            fac3_index = fac1_index - 2
            fac4_index = fac1_index - 3
        else:
            direction = random.randint(0, 1)
            
            if direction == 0:
                fac2_index = fac1_index + 1
                fac3_index = fac1_index + 2
                fac4_index = fac1_index + 3
            else:
                fac2_index = fac1_index - 1
                fac3_index = fac1_index - 2
                fac4_index = fac1_index - 3

        ###################### START DATA COLLECTION ########################
        if settings.options.collect_data:
            if fac1_index == 0 or fac2_index == 0:
                settings.collector.add_data("first_fac_moved", True)
            else:
                settings.collector.add_data("first_fac_moved", False)

            if fac1_index == len(solution.p) - 1 or fac2_index == len(solution.p) - 1:
                settings.collector.add_data("last_fac_moved", True)
            else:
                settings.collector.add_data("last_fac_moved", False)

            settings.collector.add_data("moves", abs(fac1_index - fac2_index))
        ###################### END DATA COLLECTION ##########################
    
        candidate.p[fac2_index], candidate.p[fac1_index] = candidate.p[fac1_index], candidate.p[fac2_index]
        candidate.p[fac4_index], candidate.p[fac3_index] = candidate.p[fac3_index], candidate.p[fac4_index]
        candidate.calculate_cost()
        candidate.moved = 1
        
        return candidate


class PredecessorAndSuccessor(Heuristic):
    def __init__(self, solver):
        self.solver = solver
        
    def permute(self, solution: QapSolution):
        candidate = cp.deepcopy(solution)
        # escogemos dos facilities al azar
        fac1, _ = random.sample(candidate.p, 2)
        
        # caso en el que fac1 es el primer elemento
        # las intercambiamos
        fac1_index = candidate.p.index(fac1)
        
        if fac1_index < 2:
            fac2_index = fac1_index + 2
        else:
            fac2_index = fac1_index - 2

        ###################### START DATA COLLECTION ########################
        if settings.options.collect_data:
            if fac1_index == 0 or fac2_index == 0:
                settings.collector.add_data("first_fac_moved", True)
            else:
                settings.collector.add_data("first_fac_moved", False)

            if fac1_index == len(solution.p) - 1 or fac2_index == len(solution.p) - 1:
                settings.collector.add_data("last_fac_moved", True)
            else:
                settings.collector.add_data("last_fac_moved", False)

            settings.collector.add_data("moves", abs(fac1_index - fac2_index))
        ###################### END DATA COLLECTION ##########################
        
        candidate.p[fac2_index], candidate.p[fac1_index] = candidate.p[fac1_index], candidate.p[fac2_index]
        candidate.calculate_cost()
        candidate.moved = 1
        
        return candidate
