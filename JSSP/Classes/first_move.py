from kmoves import KMoves
import copy as cp
import random
from collections import OrderedDict


class FirstMove(KMoves):
    def perturb_solution(self, current_solution):
        original_graph = current_solution.m_graph
        original_jobs_graph = current_solution.jobs_graph
        
        graph = cp.deepcopy(original_graph)
        machine_graph_copy = OrderedDict(graph)
        
        # Calculate the max number of displacements that each operation is capable of having
        # negative numbers mean movements to the left, while positive ones movements to the right
        displacements = self._calculate_displacements(machine_graph_copy)
        # Get the machine index alongside the operation to move and its corresponding move capability
        # for each candidate
        candidate_solutions = []
        candidates = []  # each tupple has: machine_index, operation_index, moves
        for _ in range(self.k):
            candidates.append(self._get_operation_details(machine_graph_copy, displacements))
            # Choose a direction randomly if it is neither the first or the second for each candidate
            moves = candidates[2]
            if type(moves) == tuple:
                candidates[2] = int(random.choice(moves))
            
            # Find the actual operation index in time for the selected machine
            machine_operations = graph.get(candidates[0])
            operation = machine_operations[candidates[1]]
            operation_index = machine_operations.index(operation)
            
            """DATA COLLECTION"""
            
            moves, term = self._get_movement_details(candidates[2])
            
            """DATA COLLECTION"""
            candidate_graph = cp.deepcopy(graph)
            self._do_displacements(candidate_graph, moves, term, candidates[0], operation_index)
            
            # make copy
            t_jobs_graph = cp.deepcopy(original_jobs_graph)
            t_machines_graph = cp.deepcopy(candidate_graph)
            
            # Si se violo alguna restriccion en el plan generado
            if current_solution.violates_constraints(t_jobs_graph, t_machines_graph):
                """DATA COLLECTION"""
                candidate_solutions.append(current_solution)
                break
            else:
                """DATA COLLECTION"""
            
            candidate_solutions.append(self._generate_solution(candidate_graph, current_solution))

        for candidate_solution in candidate_solutions:
            if candidate_solution.cost() < current_solution.cost():
                return candidate_solution

        return current_solution
