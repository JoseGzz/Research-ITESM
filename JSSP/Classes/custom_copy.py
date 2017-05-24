from copy import deepcopy as dc
from copy import copy as c
from solution import Solution

class Custom_copy():
    def __init_(self):
        pass

    def copy(current_solution):
        new_solution = Solution()
        new_solution.g = dc(current_solution.g)
        new_solution.no_machines = c(current_solution.no_machines)
        new_solution.machines = dc(current_solution.machines)
        new_solution.operations = dc(current_solution.operations)
        new_solution.ms = c(current_solution.ms)
        new_solution.no_jobs = c(current_solution.no_jobs)
        new_solution.jobs_graph = dc(current_solution.jobs_graph)
        new_solution.m_graph = dc(current_solution.m_graph)
        return new_solution