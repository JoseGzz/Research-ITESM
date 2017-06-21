from abc import abstractmethod
from heuristic import Heuristic
import copy as cp
import random


class KMoves(Heuristic):
    def __init__(self, k=1, displacements=1):
        self.k = k
        self.displacements = displacements
    
    def _do_displacements(self, graph, moves, term, machine_index, operation_index):
        for _ in range(moves):
            operation = graph[machine_index][operation_index]
            t_operation = graph[machine_index][operation_index + term]
            
            self.m_graph[machine_index][operation_index] = t_operation
            self.m_graph[machine_index][operation_index + term] = operation
            
            """DATA COLLECTION"""
            
            operation_index += term
    
    def _get_movement_details(self, possible_moves):
        # Determine the number of moves to do, calculated randomly and from 1 to k
        moves = 1 if self.displacements == 1 else random.choice(range(1,
                                                                      min(self.displacements, abs(possible_moves))))
        # Determine the direction of the movement
        term = 1 if possible_moves >= 0 else -1
        
        return moves, term
    
    def _get_operation_details(self, graph, displacements):
        # Select a machine randomly. Note that machine indeces start start at one.
        machine_index = random.choice(range(1, len(graph)))
        # Get operation displacements for that machine
        machine_displacements = displacements[machine_index]
        # Choose an operation to move randomly
        operation_index = random.choice(range(len(machine_displacements) - 1))
        # Get max number of moves for selected operation
        moves = machine_displacements.get(machine_index)[operation_index]
        
        """DATA COLLECTION"""
        
        return machine_index, operation_index, moves
    
    def _calculate_displacements(graph):
        result = {}
        for machine_id, operations in graph.items():
            possible_displacements = []
            
            for operation_index in range(len(operations)):
                # when it is the first operation
                if operation_index == 0:
                    possible_displacements.append(len(operations) - 1)
                # when it is the last operation
                elif operation_index == len(operations) - 1:
                    possible_displacements.append(-1 * (len(operations) - 1))
                # for all other operatons
                else:
                    move_left = -operation_index
                    move_right = len(operations) - 1 - operation_index
                    possible_displacements.append((move_left, move_right))
            
            result[machine_id] = possible_displacements
    
    def _generate_solution(graph, solution, jobs_graph):
        # Generamos el grafo con orden de maquinas asignadas
        jobs_graph_aux = cp.deepcopy(solution.jobs_graph)
        m_graph_aux = cp.deepcopy(graph)
        final_graph = solution.fill_graph(jobs_graph_aux, m_graph_aux)
        
        # Verificamos que no existan ciclos debido a un error en el codigo
        if solution.cycle_exists(final_graph):
            raise ValueError("Se produjo un ciclo en el" +
                             " grafo disyuntivo al momento de perturbar la solucion.")
            import sys
            sys.exit()
        
        # Creamos una nueva solucion y hacemos el recorrido hacia adelante para calcular el makespan
        result = Solution(no_machines=solution.no_machines, machines=solution.machines,
                          no_jobs=solution.no_jobs, m_graph=graph, jobs_graph=jobs_graph,
                          operations=solution.operations)
        
        result.forward_traversal(final_graph, solution.operations)
        return result
    
    @property
    def k(self):
        return self._k
    
    @k.setter
    def k(self, k):
        if k <= 0:
            self._k = 1
        else:
            self._k = k
    
    @property
    def displacements(self):
        return self._displacements
    
    @displacements.setter
    def displacements(self, displacements):
        if displacements <= 0:
            self._displacements = 1
        else:
            self._displacements = displacements
    
    @abstractmethod
    def perturb_solution(self, current_solution):
        pass
