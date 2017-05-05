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

""" Constructor de la clase """
class DisjunctiveGraph:

	def __init__(self):
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

		"""
		# imprime el grafo para probar
		for k, v in graph.items():
			print('key: ' + k)
			for val in v:
				print(val.get_id())
			print('---')
		"""

		# asignamos orden de ejecución de las operaciones en las máquinas aleatoriamente por el momento 
		#graph = self.assign_machine_order_iterative(graph)
		#graph = self.assign_machine_order_recursive(graph)
		graph = self.set_machines(graph, operations)

		# creamos la lista de operaciones que no tienen predecesores para poder fijarlas desde el principio
		first_op_ids = self.find_first_operations(graph, operations)

		
		# imrpime diccionario después de asignación de máquinas para testing
		for k, v in graph.items():
			print('key: ' + str(k))
			for val in v:
				print(val.get_id())
			print('---')
		
		# comienza algoritmo para calcular makespan

		return self.forward_assignment(graph, first_op_ids)

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
	def forward_assignment(self, graph, first_op_ids):

		times = []
		print('Asignando tiempos...')
		while not self.all_fixed(graph):
			backtracking = False
			for op_id, lst in graph.items():
				print('Operación actual: ' + str(op_id) + '.')
				current_op = lst[0]
				# si no estamos buscando la siguiente tarea
				if not backtracking: 
					print('Analizando operación...')
					# si la operación actual no tiene asignado un tiempo
					if not current_op.is_fixed():
						print('Operación sin asignación.')
						# si la operación actual no tiene predecesores
						if current_op.get_id() in first_op_ids:
							print('Operación es primera.')
							# le asignamos tiempo de inicio en cero
							current_op.add_possible_start_time(0)
							current_op.set_start_time(max(current_op.get_start_times()))
							# le asignamos tiempo de finalización en base a su duración
							current_op.set_end_time(current_op.get_start_time() + current_op.get_duration())
							# establecemos un tiempo de finalización
							end_time = current_op.get_end_time()
							# remplazamos el objeto ya con el tiempo asignado
							print('Se fija la operación ' + str(op_id) + '.')
							current_op.set_fixed(True)
							times.append(end_time)
							graph[current_op.get_id()][0] = current_op
							# se le asigna a los adjacentes siguientes (si tiene) un posible tiempo de inicio
							self.propagate_times(graph, lst, end_time, current_op)
							# se prende booleana de fijación para la operación actual
							graph[current_op.get_id()][0].set_fixed(True)
						else:
							print('Operación no es primera.')
							# si la operación actual espera una asignación de tiempo por máquina que no ha ocurrido
							if current_op.waits_for_machine() and not current_op.has_machine_time_assigned():
							    print('Operación espera tiempo de máquina.')
							    # si esto depende de una operación adelante entonces seguimos al siguiente nodo
							    if self.depends_on_posterior_op(graph, lst):
							        print('Operación depende de nodos posteriores.')
							    else:
							    	print('Backtracking activado.')
							    	# si no depende de una operación posterior entonces activamos backtracking
							    	# para pasar a la sig. tarea. Si estamos en la última tarea
							    	# pasamos a la primera, de lo contrario a la siguiente en el orden.
							    	if not (int(lst[0].get_id()[0]) == (lst[0].get_job().get_op_count()-1)):
							    		backtracking = True
							else:
								# si la operación no es primera y no espera un tiempo por máquina o ya lo tiene
								# entonces establecemos tiempo de inicio, lo marcamos como asignado, reemplazamos el objeto
								# y agregamos su tiempo de inicio a la lista de tiempos
								print('Operación no espera tiempo de máquina.')
								current_op.set_start_time(max(current_op.get_start_times()))
								current_op.set_end_time(current_op.get_start_time() + current_op.get_duration())
								current_op.set_fixed(True)
								print('Se fija la operación ' + str(op_id) + '.')
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
					print('Se detiene el backtracking en la operación: ' + op_id)
					backtracking = False

		makespan = str(max(times))
		print("Makespan: " + makespan)
		return graph, makespan

	""" Método propagate_times que añade el tiempo de finalización de la operación actual a la lista
	de posibles tiempos de inicio de las operaciones adyacente. """
	def propagate_times(self, graph, lst, end_time, current_op):
		# si algún adyacente pertenece a otra tarea entonces se trata de un adyacente conectado
		# por máquina, así que se prende su booleana
		print("Propagando desde:", current_op.get_id())
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
			print('El grafo generado está ciclado. Generando un nuevo grafo...')
			return self.assign_machine_order(graph2)
		else:
			print('Grafo sin ciclos.')
			return graph
	

	def machine_order(self, graph, operations):
		machines = {}
		machine_ids = []
		spr = []
		firsts_lst = self.find_first_operations(graph, operations)
		for op in firsts_lst:
			print(op)
		graph_aux = dd(str)
		# Se voltea el diccionario actual de operaciones
		for _, lst in graph.items():
			if lst[0].get_id() in firsts_lst:
				graph_aux[lst[0].get_id()] = []
			elif len(lst) > 1:
				if graph_aux.get(lst[1].get_id()) is None:
					graph_aux[lst[1].get_id()] = []
					graph_aux[lst[1].get_id()].append(lst[0])
				else:
					graph_aux[lst[1].get_id()].append(lst[0])
		
		# Obtenemos las operaciones en orden de precedencias 
		counter = len(graph_aux) / len(firsts_lst)
		for i in range(int(counter)):
			for op, lst in graph_aux.items():
				if len(lst) <= 0 and not graph_aux[op].has_machine_order():
						spr.append(lst[0])
						lst[0].set_machine_order(True)
			shuffle(spr)
			if not spr[len(spr) - 1].get_machine_id() in machine_ids:
				machines[spr[len(spr) - 1].get_machine_id()] = [spr[len(spr) - 1]]
				machine_ids.append(spr[len(spr) - 1].get_machine_id())
			else:
				machines[spr[0].get_machine_id()].append(spr[len(spr) - 1])
				graph_aux[spr[0]] = []
			spr.pop()
		return machines

	def set_machines(self, graph, operations):
		graph_aux = self.machine_order(graph, operations)
		for m_id, lst in graph_aux:
			for i in range(len(lst)-1):
				graph[lst[i].get_id()].append(lst[i+1])

		return graph

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
				print('El grafo generado está ciclado. Generando un nuevo grafo...')
				contador += 1
				print('Iteracion no.', contador)
				graph = cp.deepcopy(graph2)
		print('Grafo sin ciclos.')
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


