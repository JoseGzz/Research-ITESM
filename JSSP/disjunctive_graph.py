# -*- coding: utf-8 -*
import collections
from random import shuffle

class DisjunctiveGraph:
	def __init__(self):
		pass

	def find_makespan(self, jobs, operations, machines, no_machines):
		# Using the job array index values
		# Create diccionary, each key for each operation and values are the next operation
		graph = collections.OrderedDict((operations[i].get_id(), [operations[i], operations[i + 1]])
			for i in range(len(operations) - 1) if operations[i].get_job_id() == operations[i+1].get_job_id())

		# crea nodos finales apuntando a vacío por el momento
		for op in operations:
			if op.get_self_id() == (no_machines-1):
				graph[op.get_id()] = [op]
	
		'''
		for k, v in graph.iteritems():
			print 'key: {}'.format(k)
			for val in v:
				print val.get_id()
			print '---'
		'''
		graph = self.assign_machine_order(graph, operations)
		first_op_ids = self.find_first_operations(graph, operations)

		# For each operation identify common operations in terms of machines
		
		for k, v in graph.iteritems():
			print('key: ' + str(k))
			for val in v:
				print(val.get_id())
			print('---')
		

		print first_op_ids

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
			for op_id, lst in graph.iteritems():
				print(op_id)
				print('Analizando operación...')
				current_op = lst[0]
				if not backtracking: 
					if not current_op.is_fixed():
						print('Operación sin asignacion.')
						if current_op.get_id() in first_op_ids:
							print('Operación es primera.')
							current_op.set_tart_time(0)
							current_op.set_end_time(current_op.get_start_time() + current_op.get_duration())
							end_time = current_op.get_end_time()
							graph[current_op.get_id()][0] = current_op
							for count, adjacent in enumarate(lst[:1]):
								graph[adjacent.get_id()][0].add_possible_start_time(end_time)
								if count > 0:
									graph[adjacent.get_id()][0].set_machine_time_assigned(True)
							graph[current_op.get_id()][0].set_fixed(True)
						else:
							print('Operación no es primera.')
							if current_op.waits_for_machine() and not current_op.has_machine_time_assigned():
							    print('Operación espera tiempo de máquina.')
							    if self.depends_on_posterior_op(graph, lst):
							        print('Operación depente de nodos posteriores.')
							    else:
							    	print('Activando backtracking.')
							    	backtracking = True
							    	current_job = int(current_op.get_id()[2])
							    	next_job = 0 if current_job == (len(jobs) - 1) else current_job + 1 
							else:
								print('Operación no espera tiempo de máquina.')
								current_op.set_start_time()
								current_op.set_fixed(True)
								graph[current_op.get_id()][0] = current_op
								times.append(current_op.get_start_time())
				elif int(lst[1].get_id()[2]) == next_job :
					backtracking = False



		print("makespan: " + str(max(times)))
		return graph

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
		for op_id, lst in graph.iteritems():
			if not lst[0].is_fixed():
				return False
		return True

	def assign_machine_order(self, graph, operations):
		for op_id, lst in graph.iteritems():
			if not lst[0].has_machine_order():
			    machine_id = lst[0].get_machine_id()
			    ops_with_common_machine = [lst2[0] for op_id2, lst2 in graph.iteritems()
			    if lst2[0].get_machine_id() == machine_id and not lst2[0].has_machine_order()]
			    ops_cm = ops_with_common_machine
			    vals = []
			    for val in ops_cm:
			    	val.set_machine_order(True)
			    	vals.append(val)
			    ops = vals
			    shuffle(ops)
			    ops[0].set_waits_for_machine(False)
			    # se agrergan las operaciones comunes (por máquinas) a la lista de adjacentes
			    for i in range(len(ops)-1):
			          graph[ops[i].get_id()].append(ops[i+1])
		return graph

	def find_first_operations(self, graph, operations):
		id_list = []
		for op in operations:
			for k, v in graph.iteritems():
				if op.get_id() in v:
					id_list.append(op.get_id())
		return id_list


