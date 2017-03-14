# -*- coding: utf-8 -*
from collections import OrderedDict
from random import shuffle

class DisjunctiveGraph:
	def __init__(self):
		pass

	def find_makespan(self, jobs, operations, machines, no_machines):
		# Using the job array index values
		# Create diccionary, each key for each operation and values are the next operation
		graph = OrderedDict((operations[i].get_id(), [operations[i], operations[i + 1]])
			for i in range(len(operations) - 1) if operations[i].get_job_id() == operations[i+1].get_job_id())

		# crea nodos finales apuntando a vacío por el momento
		graph_last = {}
		for op in operations:
			if op.get_self_id() == (no_machines-1):
				graph_last[op.get_id()] = [op]
	
		graph = self.merge_graphs(graph, graph_last, jobs)

		'''
		for k, v in graph.items():
			print('key: ' + k)
			for val in v:
				print(val.get_id())
			print('---')
		'''
		graph = self.assign_machine_order(graph)
		first_op_ids = self.find_first_operations(graph, operations)

		# imrpime diccionario después de asignación de máquinas
		'''
		for k, v in graph.items():
			print('key: ' + str(k))
			for val in v:
				print(val.get_id())
			print('---')
		'''
		#print('firsts: ', first_op_ids)

		# ALGORITHM 1 : Calculate Makespan
		#
		# do
		#  for each operation
		#    if not fixed then
		#      if its a FIRST (no predecesors at all)
		#        assign start-time 0 and end-time st + duration
		#        then for all of its succesors add the end time of this node to their list of start times. From succesors 2 on, set those as machine time assigned.
		#        Mark this node as 'fixed'.
		#        continue to the next node and repeat.
		#      else if not a FIRST node then 
		#        if needs and waiting a start time based on machine order
		#          if it depends on a posterior operation of the same job
		#            continue to the next node and repeat
		#          else 
		#            then backtrack to the next job and repeat.
		#        else if it has recived a start time based on machine order or it does not need one then
		#          substract 1 from the pending machine times variable
		#          calculate latest time from list of start times, add its duration and send to adyacents.
		#          set to fixed.
		#          continue to next node and repeat
		#   else if fixed then continue to next node
		# while not all operations are fixed

		backtracking = False
		next_job = 0
		times = []
		print('Asignando tiempos...')
		while not self.all_fixed(graph):
			for op_id, lst in graph.items():
				print('Operación actual: ', op_id)
				current_op = lst[0]
				# si no estamos buscando una tarea distinta
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
							current_op.set_start_time()
							# le asignamos tiempo de finalización en base a su duración
							current_op.set_end_time(current_op.get_start_time() + current_op.get_duration())
							# establecemos un tiempo de finalización
							end_time = current_op.get_end_time()
							# remplazamos el objeto ya con el tiempo asignado
							print('Se fija la operación ', op_id, '.')
							current_op.set_fixed(True)
							times.append(end_time)
							graph[current_op.get_id()][0] = current_op
							# se le asigna a los adjacentes siguientes (si tiene) un posible tiempo de inicio
							# si algún adyacente pertenece a otra tarea entonce se trata de un adyacente conectado
							# por máquina, así que se prende su booleana
							if len(lst) > 1:
								for adjacent in lst[1:]:
									graph[adjacent.get_id()][0].add_possible_start_time(end_time)
									if graph[adjacent.get_id()][0].get_job_id() != current_op.get_job_id():
										graph[adjacent.get_id()][0].set_machine_time_assigned(True)
							# se prende booleana de fijación para la operación actual
							graph[current_op.get_id()][0].set_fixed(True)
						else:
							print('Operación no es primera.')
							# si la operación actual espera una asignación de tiempo por máquina que no ha ocurrido
							# si esto depende de una operación adelante entonces seguimos al siguiente nodo
							if current_op.waits_for_machine() and not current_op.has_machine_time_assigned():
							    print('Operación espera tiempo de máquina.')
							    if self.depends_on_posterior_op(graph, lst):
							        print('Operación depente de nodos posteriores.')
							    else:
							    	print('Backtracking activado.')
							    	# si no depende de una operación posterior entonces activamos backtracking
							    	# para pasar a la sig. tarea. Si estamos en la última tarea
							    	# pasamos a la primera, de lo contrario a la siguiente.
							    	backtracking = True
							    	#current_job_id = current_op.get_self_id()
							    	#next_job = 0 if current_job_id == (len(jobs) - 1) else current_job_id + 1 
							else:
								# si la operación no es primera y no espera un tiempo por máquina o ya lo tiene
								# entonces establecemos tiempo de inicio, lo marcamos como asignado, reemplazamos el objeto
								# y agregamos su tiempo de inicio a la lista de tiempos
								print('Operación no espera tiempo de máquina.')
								current_op.set_start_time()
								current_op.set_end_time(current_op.get_start_time() + current_op.get_duration())
								current_op.set_fixed(True)
								print('Se fija la operación ', op_id, '.')
								end_time = current_op.get_end_time()
								graph[current_op.get_id()][0] = current_op
								times.append(current_op.get_end_time())
								# se le asigna a los adjacentes un posible tiempo de inicio
								# a partir del primer adyacente (si existe y la operación es final) se trata de un adyacente 
								# conectado por máquina, así que se prende su booleana
								# en otros casos a partir del tercer elemento tenemos adyacentes por máquinas
								if len(lst) > 1:
									for adjacent in lst[1:]:
										graph[adjacent.get_id()][0].add_possible_start_time(end_time)
										if graph[adjacent.get_id()][0].get_job_id() != current_op.get_job_id():
											graph[adjacent.get_id()][0].set_machine_time_assigned(True)
										# se prende booleana de asignación para la operación actual
								graph[current_op.get_id()][0].set_fixed(True)
				# si la siguiente operación corresponde a la tarea que se buscaba, detenemos la búsqueda 
				elif int(lst[0].get_id()[0]) == (lst[0].get_job().get_op_count()-1):#len(jobs)-1:# len(lst) > 1 and int(lst[1].get_id()[2]) == next_job:
					#print('op: ', int(lst[1].get_id()[0]))
					print('Se detiene el backtracking en operación: ' + op_id)
					backtracking = False

		print("Makespan: " + str(max(times)))
		
		return graph


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

	def depends_on_posterior_op(self, graph, op_lst):
		current_op = op_lst[0]
		iterops = iter(op_lst)
		next(iterops)
		for op in iterops:
			adjacents = graph.get(op.get_id())[1:]
			if current_op in adjacents:
				return True
		return False

	def all_fixed(self, graph):
		for op_id, lst in graph.items():
			if not lst[0].is_fixed():
				return False
		return True

	def assign_machine_order(self, graph):
		graph2 = graph.copy()
		for op_id, lst in graph.items():
			if not lst[0].has_machine_order():
			    machine_id = lst[0].get_machine_id()
			    ops_with_common_machine = [lst2[0] for op_id2, lst2 in graph.items()
			    if lst2[0].get_machine_id() == machine_id and not lst2[0].has_machine_order()]
			    ops_cm = ops_with_common_machine
			    vals = []
			    for val in ops_cm:
			    	val.set_machine_order(True)
			    	vals.append(val)
			    ops = vals
			    shuffle(ops)
			    ops[0].set_waits_for_machine(False)
			    # se agrergan las operaciones comunes (por máquina) a la lista de adjacentes
			    for i in range(len(ops)-1):
			          graph[ops[i].get_id()].append(ops[i+1])

		for k, v in graph.items():
			print('key: ' + k)
			for val in v:
				print(val.get_id())
			print('---')
		
		if self.cycle_exists(graph):
			print('El grafo generado está ciclado. Generando un nuevo grafo...')
			return self.assign_machine_order(graph2)
		else:
			print('Grafo sin ciclos.')
			return graph

#-----------
	def has_cycles(self, graph):
		return self.cycle_exists(graph)

	def cycle_exists(self, G):
	    color = { u : "white" for u in G  }
	    found_cycle = [False]
	    for u in G:
	    	if color[u] == "white":
	    		self.dfs_visit(G, u, color, found_cycle)
	    	if found_cycle[0]:
	    		break
	    return found_cycle[0]

	def dfs_visit(self, G, u, color, found_cycle):
		'''
		for k, v in G.items():
			print('key: ' + k)
			for val in v:
				print(val)
			print('------')
		'''
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
		
#-----------------

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


