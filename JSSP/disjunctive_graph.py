# -*- coding: utf-8 -*
"""DisjunctiveGraph
Clase que genera el grafo disjuntivo para el problema de JSSP.
José González Ayerdi - A01036121
ITESM Campus Monterrey
02/2017
"""
from collections import OrderedDict
from random      import shuffle
from collections import defaultdict as dd
import copy as cp
import random

""" Constructor de la clase """
class DisjunctiveGraph:

	def __init__(self):
		self.debug = False
		pass

	""" Método find_makespan que calcula el makespan dadas listas de tareas, operaciones y máquinas,
		y regresa el grafo encontrado. El makespan es el tiempo en el que todas las operaciones terminan de ser
		procesadas por la máquina a la que fueron asignadas.

	    El objeto graph es un diccionario que tiene como llaves los id de las operaciones, y como valores
	    tenemos la lista de operaciones (objetos) adjacentes (incluyendo la operación misma al principio).
	""" 
	def find_makespan(self, jobs, operations, machines, no_machines):
		# creamos el diccionario ordenado (para facilitar el recorrido) en base a las listas recibidas
		graph = OrderedDict((operations[i].get_id(), [operations[i], operations[i + 1]])
			for i in range(len(operations) - 1) if operations[i].get_job_id() == operations[i+1].get_job_id())

		# creamos nodos finales apuntando a sí mismos solamente por el momento
		# ya que hay complicaciones para asignarles valores con compresión de listas
		graph_last = {}
		for op in operations:
			if op.get_self_id() == (no_machines-1):
				graph_last[op.get_id()] = [op]

		# agregamos los nodos finales ya con lista de adjacentes disponible
		graph = self.merge_graphs(graph, graph_last, jobs)

		if self.debug : print("Antes de asignacion de maquinas")
		# imprime el grafo para probar
		for k, v in graph.items():
			if self.debug : print('key: ' + k)
			for val in v:
				if self.debug : print(val.get_id())
			if self.debug : print('---')
		
		jobs_graph = cp.deepcopy(graph)
		# asignamos orden de ejecución de las operaciones en las máquinas aleatoriamente por el momento 
		#graph = self.assign_machine_order_iterative(graph)
		#graph = self.assign_machine_order_recursive(graph)
		graph, machines_graph = self.set_machines(graph, operations)
		

		# Ejecuta algoritmo para calcular makespan
		return self.forward_traversal(graph, jobs_graph, machines_graph, operations)

	"""Método para asignar tiempos a las operaciones por medio del recorrido hacia adelante:

	 ALGORITHM 1 : Calculate Makespan
	
	 while not all operations are fixed
	  for each operation
	    if not fixed then
	      if its a FIRST (no predecesors at all)
	        assign start-time 0 and end-time st + duration
	        then for all of its succesors add the end time of this node to their list of start times. From succesors 2 on, set those as machine time assigned.
	        Mark this node as 'fixed'.
	        continue to the next node and repeat.
	      else if not a FIRST node then 
	        if needs and waiting a start time based on machine order
	          if it depends on a posterior operation of the same job
	            continue to the next node and repeat
	          else 
	            then backtrack to the next job and repeat.
	        else if it has recived a start time based on machine order or it does not need one then
	          substract 1 from the pending machine times variable
	          calculate latest time from list of start times, add its duration and send to adyacents.
	          set to fixed.
	          continue to next node and repeat
	   else if fixed then continue to next node
	 repeat
	 """
	def forward_traversal(self, original_graph, jobs_graph, machines_graph, operations):
		graph = cp.deepcopy(original_graph)
		# imrpime diccionario después de asignación de máquinas para testing
		if self.debug :
			print("Despues de asignacion de maquinas")
			for k, v in graph.items():
				if self.debug : print('key: ' + str(k))
				for val in v:
					if self.debug : print(val.get_id())
				if self.debug : print('---')

		# creamos la lista de operaciones que no tienen predecesores para poder fijarlas desde el principio
		first_op_ids = self.find_first_operations(graph, operations)
		times = []
		if self.debug : print('Asignando tiempos...')
		while not self.all_fixed(graph):
			backtracking = False
			for op_id, lst in graph.items():
				if self.debug : print('Operación actual: ' + str(op_id) + '.')
				current_op = lst[0]
				# si no estamos buscando la siguiente tarea
				if not backtracking:
					if self.debug : print('Analizando operación...')
					# si la operación actual no tiene asignado un tiempo
					if not current_op.is_fixed():
						if self.debug : print('Operación sin asignación.')
						# si la operación actual no tiene predecesores
						if current_op.get_id() in first_op_ids:
							if self.debug : print('Operación es primera.')
							# le asignamos tiempo de inicio en cero
							current_op.add_possible_start_time(0)
							current_op.set_start_time(max(current_op.get_start_times()))
							# le asignamos tiempo de finalización en base a su duración
							current_op.set_end_time(current_op.get_start_time() + current_op.get_duration())
							# establecemos un tiempo de finalización
							end_time = current_op.get_end_time()
							# remplazamos el objeto ya con el tiempo asignado
							if self.debug : print('Se fija la operación ' + str(op_id) + '.')
							current_op.set_fixed(True)
							times.append(end_time)
							graph[current_op.get_id()][0] = current_op
							# se le asigna a los adjacentes siguientes (si tiene) un posible tiempo de inicio
							self.propagate_times(graph, lst, end_time, current_op)
							# se prende booleana de fijación para la operación actual
							graph[current_op.get_id()][0].set_fixed(True)
						else:
							if self.debug : print('Operación no es primera.')
							# si la operación actual espera una asignación de tiempo por máquina que no ha ocurrido
							if current_op.waits_for_machine() and not current_op.has_machine_time_assigned():
							    if self.debug : print('Operación espera tiempo de máquina.')
							    # si esto depende de una operación adelante entonces seguimos al siguiente nodo
							    if self.depends_on_posterior_op(graph, lst):
							        if self.debug : print('Operación depende de nodos posteriores.')
							    else:
							    	if self.debug : print('Backtracking activado.')
							    	# si no depende de una operación posterior entonces activamos backtracking
							    	# para pasar a la sig. tarea. Si estamos en la última tarea
							    	# pasamos a la primera, de lo contrario a la siguiente en el orden.
							    	if (int(lst[0].get_self_id() != lst[0].get_job().get_op_count()-1)):
							    		backtracking = True
							else:
								# si la operación no es primera y no espera un tiempo por máquina o ya lo tiene
								# entonces establecemos tiempo de inicio, lo marcamos como asignado, reemplazamos el objeto
								# y agregamos su tiempo de inicio a la lista de tiempos
								if self.debug : print('Operación no espera tiempo de máquina.')
								current_op.set_start_time(max(current_op.get_start_times()))
								current_op.set_end_time(current_op.get_start_time() + current_op.get_duration())
								current_op.set_fixed(True)
								if self.debug : print('Se fija la operación ' + str(op_id) + '.')
								end_time = current_op.get_end_time()
								graph[current_op.get_id()][0] = cp.copy(current_op)
								times.append(current_op.get_end_time())
								# se le asigna a los adjacentes un posible tiempo de inicio
								# a partir del primer adyacente (si existe y la operación es final) se trata de un adyacente 
								# conectado por máquina, así que se prende su booleana
								# en otros casos a partir del tercer elemento tenemos adyacentes por máquinas
								self.propagate_times(graph, lst, end_time, current_op)
								# se prende booleana de fijación para la operación actual
								graph[current_op.get_id()][0].set_fixed(True) 
				# si la siguiente operación corresponde a la primera operación de una tarea entonces nos detenemos 
				elif int(lst[0].get_self_id()) == (lst[0].get_job().get_op_count()-1):
					if self.debug : print('Se detiene el backtracking en la operación: ' + op_id)
					backtracking = False
		makespan = str(max(times)) 
		print("Makespan: " + makespan)
		return graph, makespan, jobs_graph, machines_graph, operations

	""" Método propagate_times que añade el tiempo de finalización de la operación actual a la lista
	de posibles tiempos de inicio de las operaciones adyacente. """
	def propagate_times(self, graph, lst, end_time, current_op):
		# si algún adyacente pertenece a otra tarea entonces se trata de un adyacente conectado
		# por máquina, así que se prende su booleana
		if self.debug : print("Propagando desde:", current_op.get_id())
		if len(lst[1:]) >= 1:
			for adjacent in lst[1:]:
				graph[adjacent.get_id()][0].add_possible_start_time(end_time)
				if current_op.get_machine_id() == adjacent.get_machine_id():
					graph[adjacent.get_id()][0].set_machine_time_assigned(True)

	""" Método merge_graphs para combinar grafo de operaciones finales con el resto de las operaciones. """
	def merge_graphs(self, first, second, jobs):
		graph_new = OrderedDict()
		for op_id, vals in first.items():
			if vals[0].get_self_id() == (jobs[vals[0].get_job_id()].get_op_count())-2:
				graph_new[op_id] = vals
				new_id = str(vals[0].get_self_id() + 1) + '_' + str(vals[0].get_job_id())
				graph_new[new_id] = second.get(new_id)
			else:
				graph_new[op_id] = vals
		return graph_new

	""" Método depends_on_posterior para saber si una operación debe de esperar a que una operación
	posterior termine de ser procesada por la máquina que se le asignó a ambas. """
	def depends_on_posterior_op(self, graph, op_lst):
		current_op = op_lst[0]
		iterops = iter(op_lst)
		next(iterops)
		for op in iterops:
			adjacents = graph.get(op.get_id())[1:]
			if current_op in adjacents:
				return True
		return False

	""" Método all_fixed para saber si todas las operaciones en el grafo han sido fijadas. """
	def all_fixed(self, graph):
		for op_id, lst in graph.items():
			if not lst[0].is_fixed():
				return False
		return True

	""" Método recursivo para asignar un orden de ejecución en máquinas a las operaciones """
	def assign_machine_order_recursive(self, graph):
		# copiamos el grafo actual para que en caso de que tenga ciclos, repitamos el proceso con el grafo como estaba
		graph2 = cp.deepcopy(graph)
		for op_id, lst in graph.items():
			if not lst[0].has_machine_order():
			    machine_id = lst[0].get_machine_id()
			    # obtenemos los objetos operaciones que comparten máquina y no se ha establecido su orden de ejecución
			    ops_with_common_machine = [
			    	lst2[0] for op_id2, lst2 in graph.items()
			    	if lst2[0].get_machine_id() == machine_id and not lst2[0].has_machine_order()
			    ]
			    ops_cm = ops_with_common_machine
			    vals = []
			    # a todas las operaciones obtenidas se les marca que ya se les asignó una máquina
			    for val in ops_cm:
			    	val.set_machine_order(True)
			    	vals.append(val)
			    ops = vals
			    # IMPORTANTE: la asignación del orden de ejecución en las máquinas se hace de manera aleatoria
			    shuffle(ops)
			    ops[0].set_waits_for_machine(False)
			    # se agrergan las operaciones comunes (por máquina) a la lista de adjacentes de la actual operación
			    for i in range(len(ops)-1):
			          graph[ops[i].get_id()].append(ops[i+1])
        # revisamos si existen ciclos en el grafo generado (se viola restricción), en tal caso hay que ejecutar el procedimiento nuevamente
		if self.cycle_exists(graph):
			if self.debug : print('El grafo generado está ciclado. Generando un nuevo grafo...')
			return self.assign_machine_order(graph2)
		else:
			if self.debug : print('Grafo sin ciclos.')
			return graph
	
	def machine_order(self, graph, operations):
		# dd por default dict
		machines = dd(str)
		machine_ids = []
		spr = []
		firsts_lst = self.find_first_operations(graph, operations)
		graph_aux = {}
		# Se voltea el diccionario actual de operaciones
		for _, lst in graph.items():
			if lst[0].get_id() in firsts_lst:
				if len(lst) > 1:
					graph_aux[lst[1].get_id()] = []
					graph_aux[lst[1].get_id()].append(lst[0])
				graph_aux[lst[0].get_id()] = []
			elif len(lst) > 1:
				if graph_aux.get(lst[1].get_id()) is None:
					graph_aux[lst[1].get_id()] = []
					graph_aux[lst[1].get_id()].append(lst[0])
				else:
					graph_aux[lst[1].get_id()].append(lst[0])
		graph_copy = cp.deepcopy(graph_aux)
		# Obtenemos las operaciones en orden de precedencias 
		while True:
			# buscamos las operaciones cuyo precedente ya haya sido asignado
			for op, lst in graph_aux.items():
				if len(lst) == 0 and not graph[op][0].has_machine_order():
						# estas operaciones las agregamos a la lista spr 
						spr.append(graph[op][0])
						# y las consideramos asignadas
						graph[op][0].set_machine_order(True)
						del graph_copy[op]
			# asignamos un orden aleatorio para comenzar
			shuffle(spr)
			# Se va armando el diccionario de maquinas
			# Siempre se utiliza el ultimo elemento de la lista
			# despues de la asignacion aleatoria
			if not spr[-1].get_machine_id() in machine_ids:
				machines[spr[-1].get_machine_id()] = [spr[-1]]
				machine_ids.append(spr[-1].get_machine_id())
				graph[spr[-1].get_id()][0].set_waits_for_machine(False)
			else:
				machines[spr[-1].get_machine_id()].append(spr[-1])
			# el antecesor de la operacion que ha sido asignada
			# queda libre para poder ser asignado despues
			used_op = spr[-1].get_id()
			self.find_and_delete(graph_aux, used_op)
			spr.pop()
			# si ya no hay operaciones que falten por considerar
			# y las que estan en consideracion ya se asignaron todas
			# entonces terminamos
			if (not graph_copy) and len(spr) == 0 : return machines
		
	def find_and_delete(self, graph_aux, used_op):
		for op, lst in graph_aux.items():
			if len(lst) != 0:
				if lst[0].get_id() == used_op:
					graph_aux[op] = []

	def set_machines(self, graph, operations):
		graph_aux = self.machine_order(graph, operations)
		for m_id, lst in graph_aux.items():
			for i in range(len(lst)-1):
				var = lst[i].get_id()
				var2 = lst[i+1].get_id()
				graph[lst[i].get_id()].append(lst[i+1])
		if self.cycle_exists(graph) :
			pass
			#if print("CICLADO")
			#import sys
			#sys.exit()
		else:
			pass
			#print("NO CICLADO")
		return graph, graph_aux

	""" Método iterativo para asignar un orden de ejecución en máquinas a las operaciones """
	def assign_machine_order_iterative(self, graph):
		# copiamos el grafo actual para que en caso de que tenga ciclos, repitamos el proceso con el grafo como estaba
		graph2 = cp.deepcopy(graph)
		contador = 0
		while True:
			for op_id, lst in graph.items():
				if not lst[0].has_machine_order():
					machine_id = lst[0].get_machine_id()
					# obtenemos los objetos operaciones que comparten máquina y no se ha establecido su orden de ejecución
					ops_with_common_machine = [
						lst2[0] for op_id2, lst2 in graph.items()
						if lst2[0].get_machine_id() == machine_id and not lst2[0].has_machine_order()
					]
					ops_cm = ops_with_common_machine
					vals = []
					# a todas las operaciones obtenidas se les marca que ya se les asignó una máquina
					for val in ops_cm:
						val.set_machine_order(True)
						vals.append(val)
					ops = vals
					# IMPORTANTE: la asignación del orden de ejecución en las máquinas se hace de manera aleatoria
					shuffle(ops)
					ops[0].set_waits_for_machine(False)
					# se agrergan las operaciones comunes (por máquina) a la lista de adjacentes de la actual operación
					for i in range(len(ops)-1):
					      graph[ops[i].get_id()].append(ops[i+1])
			# revisamos si existen ciclos en el grafo generado (se viola restricción), en tal caso hay que ejecutar el procedimiento nuevamente
			if not self.cycle_exists(graph):
				break
			else:
				if self.debug : print('El grafo generado está ciclado. Generando un nuevo grafo...')
				contador += 1
				if self.debug : print('Iteracion no.', contador)
				graph = cp.deepcopy(graph2)
		if self.debug : print('Grafo sin ciclos.')
		return graph

	""" Método cycle_exists que detecta ciclos en un grafo utilizando recorrido a profundidad (DFS)
	con coloreo de nodos.
	Código basado en: https://algocoding.wordpress.com/2015/04/02/detecting-cycles-in-a-directed-graph-with-dfs-python/
	TODO: reemplazar con implementación propia."""
	def cycle_exists(self, G):
	    color = { u : "white" for u in G  }
	    found_cycle = [False]
	    for u, lst in G.items():
	    	if color[u] == "white":
	    		self.dfs_visit(G, lst[0].get_id(), color, found_cycle)
	    	if found_cycle[0]:
	    		break
	    return found_cycle[0]
	
	""" Método dfs_visit recursivo que ejecuta el algoritmo DFS """
	def dfs_visit(self, G, u, color, found_cycle):
		if found_cycle[0]:                          
			return
		color[u] = "gray"
		for v in G[u][1:]:                              
			if color[v.get_id()] == "gray":                 
				found_cycle[0] = True       
				return 
			if color[v.get_id()] == "white":                 
				self.dfs_visit(G, v.get_id(), color, found_cycle)
		color[u] = "black"                          

	""" Método find_first_operations que regresa la lista con id de las operaciones que no tienen predecesores """
	def find_first_operations(self, graph, operations):
		id_list = []
		for op in operations:
			found = False
			for k, v in graph.items():
				ids = [id_op.get_id() for id_op in v[1:]]
				if op.get_id() in ids:
					found = True
			if not found:
				id_list.append(op.get_id())
		return id_list

	"""Funcion para perturbar la solucion actual y obtener un vecino."""
	def perturbate_solution(self, jobs_graph, m_graph, operations):
		displacements = []
		# Se genera la cantidad de desplazamientos posibles para cada operacion
		for m_id, ops in m_graph.items():
			pos = []
			for i in range(len(ops)):
				if i == 0:
					pos.append(len(ops) - 1)
				elif i == len(ops) - 1:
					pos.append(-1 * (len(ops) - 1))
				else:
					move_left = -i
					move_right = len(ops) - 1 - i 
					pos.append((move_left, move_right))
			displacements.append(pos)
		
		# Se escoge una maquina al azar
		machine = random.choice(range(len(displacements)))
		# Agarramos la lista de desplazamientos para las operaciones de esa maquina
		disps = displacements[machine]
		# Escogemos una operacion al azar para desplazarla
		operation_index = random.choice(range(len(disps)))
		# Agarramos la cantidad de movimientos posibles para la operacion obtenida
		moves = displacements[machine][operation_index]
		# Si la operacion no es ni la primera ni la segunda
		# agarramos una direccion de movimiento al azar
		if type(moves) == tuple:
			moves = int(random.choice(moves))
		# Lista con las operaciones de la maquina
		lst = m_graph[machine]
		# Operacion a desplazar
		operation = lst[operation_index]
		# Indice de la operacion a desplazar
		index = lst.index(operation)
		# Cantidad de espacios a moverse
		print("Moves:", moves)
		move = 1 if abs(moves) == 1 else random.choice(range(1, abs(moves)))
		# Determinar direccion del desplazamiento
		term = 1 if moves >= 0 else -1
		# Llevar a cabo el desplazamiento
		print("Move: ", move)
		for i in range(move):
			# Obtenemos la operacion a mover
			operation = m_graph[machine][index]
			# Obtenemos la operacion con la que se hara el shift
			operation_aux = m_graph[machine][index + term]
			# Se asignan las operaciones a sus nuevas ubicaciones
			m_graph[machine][index] = operation_aux
			m_graph[machine][index + term] = operation
			# Actualizamos el indice
			index += term
			# Si se violo alguna restriccion en el plan generado
			jobs_graph_aux = cp.deepcopy(jobs_graph)
			m_graph_aux = cp.deepcopy(m_graph)
			if self.violates_constraints(jobs_graph_aux, m_graph_aux):
				print("---CICLADO ADENTRO---")
				# Regresamos las operaciones a la ultima posicion factible
				index -= term
				operation_aux = m_graph[machine][index]
				operation = m_graph[machine][index + term]
				m_graph[machine][index] = operation
				m_graph[machine][index + term] = operation_aux
				# Y salimos del ciclo
				break
		
		# Generamos el grafo con las maquinas acomodadas
		m_graph, jobs_graph = self.set_machine_precedence(m_graph, jobs_graph)
		jobs_graph_aux = cp.deepcopy(jobs_graph)
		m_graph_aux = cp.deepcopy(m_graph)
		graph = self.fill_graph(jobs_graph_aux, m_graph_aux)
		# Hacemos el recorrido hacia adelante para calcular el makespan con la
		# posiblemente nueva configuracion
		if self.cycle_exists(graph):
			print("CICLADO2")
			import sys
			sys.exit()
		else:
			print("NO CICLADO2")

		return self.forward_traversal(graph, jobs_graph, m_graph, operations)

	def violates_constraints(self, jobs_graph, m_graph):
		return self.cycle_exists(self.fill_graph(jobs_graph, m_graph))
	
	def fill_graph(self, jobs_graph, machines_graph):
		for m_id, lst in machines_graph.items():
			op = lst[0]
			jobs_graph[op.get_id()][0].set_waits_for_machine(False)
			for i in range(len(lst)-1):
				var = lst[i].get_id()
				var2 = lst[i+1].get_id()
				jobs_graph[lst[i].get_id()].append(lst[i+1])
		return jobs_graph

	def set_machine_precedence(self, m_graph, jobs_graph):
		for m, lst in m_graph.items():
			lst[0].set_waits_for_machine(False)
			lst[0].set_machine_time_assigned(False)
			for op in lst[1:]:
				op.set_waits_for_machine(True)
				op.set_machine_time_assigned(False)
		return m_graph, jobs_graph
