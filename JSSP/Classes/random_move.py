from kmoves import KMoves
import copy as cp
import random
from collections import OrderedDict


class RandomMove(KMoves):
    """Creates a new neighbor for the JSSP by permuting the current solution once.
    """
    
    def perturb_solution(self, current_solution):
        original_graph = current_solution.m_graph
        original_jobs_graph = current_solution.jobs_graph
        
        graph = cp.deepcopy(original_graph)
        machine_graph_copy = OrderedDict(graph)
        
        # Calculate the max number of displacements that each operation is capable of having
        # negative numbers mean movements to the left, while positive ones movements to the right
        displacements = self._calculate_displacements(machine_graph_copy)
        # Get the machine index alongside the operation to move and its corresponding move capability
        machine_index, operation_index, moves = self._get_operation_details(machine_graph_copy, displacements)
        # Choose a direction randomly if it is neither the first or the second for each candidate
        if type(moves) == tuple:
            moves = int(random.choice(moves))
        
        # Find the actual operation index in time for the selected machine
        machine_operations = graph.get(machine_index)
        operation = machine_operations[operation_index]
        operation_index = machine_operations.index(operation)
        
        """DATA COLLECTION"""
        
        moves, term = self._get_movement_details(moves)
        
        """DATA COLLECTION"""
        
        self._do_displacements(graph, moves, term, machine_index, operation_index)
        
        # make copy
        t_jobs_graph = cp.deepcopy(original_jobs_graph)
        t_machines_graph = cp.deepcopy(graph)
        
        # Si se violo alguna restriccion en el plan generado
        if current_solution.violates_constraints(t_jobs_graph, t_machines_graph):
            """DATA COLLECTION"""
            return current_solution
        else:
            """DATA COLLECTION"""
        
        return self._generate_solution(graph, current_solution, t_jobs_graph)