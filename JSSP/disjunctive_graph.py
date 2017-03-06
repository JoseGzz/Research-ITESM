import collections
from random import shuffle

class DisjunctiveGraph:
	def __init__(self):
		pass

	def find_makespan(self, jobs, operations, machines):
		# Using the job array index values
		# Create diccionary, each key for each operation and values are the next operation
		#graph = dict([((operations[i], operations[i].get_id()), [operations[i+1].get_id()]) for i in range(len(operations) - 1)])
		graph = collections.OrderedDict((operations[i].get_id(), [operations[i], operations[i + 1]]) for i in range(len(operations) - 1))
		# For each operation identify common operations in terms of machines		
		
		graph = self.assign_machine_order(graph, operations)

		first_op_ids = find_first_operations(graph, operations)

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
		nect_job = 0
		times = []
		while not all_fixed(graph):
			for op_id, lst in graph.iteritems():
				current_op = lst[0]
				if not backtracking: 
					if not current_op.is_fixed():
						if current_op.get_id() in first_op_ids:
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
							if waits_for_machine(lst[0], graph) and not current_op.has_machine_time_assigned():
							    if depends_on_posterior_op(graph, lst):
							    	continue
							    else:
							    	backtracking = True
							    	next_job = int(current_op.get_job_id()[2]) 
							else:
								current_op.set_start_time()
								current_op.set_fixed(True)
								graph[current_op.get_id()][0] = current_op
								times.append(current_op.get_start_time())
						else:
							continue
				elif int(lst[0].get_job_id()[2]) == next_job :
					backtracking = False
				else:
					continue

		print "makespan: {}".format(max(times))

		return graph

	def waits_for_machine(op, graph):
		appearances = 0
		for op_id, lst in graph.iteritems():
			for next_op in ls[:1]:
				if op.get_id() ==  next_op.get_id():
					appearances += 1
				else:
					continue
		return appearances > 1



	def depends_on_posterior_op(self, graph, op_lst):
		current_op = op_lst[0]
		iterops = iter(op_lst)
		next(iterops)
		for op in iterops:
			adjacents = graph.get(op.get_id())[1:]
			if current_op in adjacents
				return True
			else:
				continue
		return False


	def all_fixed(self, graph):
		for op_id, lst in graph.iteritems():
			if not lst[0].is_fixed():
				return False
			else:
				continue
		return True

	def assign_machine_order(self, graph, operations):
		for op_id, lst in graph.iteritems():
			if not lst[0].has_machine_order():
			    machine_id = lst[0].get_machine_id()
			    ops_with_common_machines = [op for op in operations if op.get_machine_id() == machine_id]
			    ops_with_common_machines.append(lst[0])
			    ops = shuffle(ops_with_common_machines)
			    # se agrergan las operaciones comunes (por máquinas) a la lista de adjacentes
			    for i in range(len(ops) - 1):
			    	graph[ops[i].get_id()] = graph.get(ops[i].get_id()) + list([ops[i+1]])
			    # para las operaciones a las que ya se les asignaron máquinas, se prende su booleana
			    for op in ops:
			    	op.set_machine_order(True)
			    	vals = graph.get(op.get_id())
			    	vals[0] = op
			    	graph[op.get_id()] = vals
		return graph

	def find_first_operations(self, graph, operations):
		id_list = []
		for op in operations:
			for k, v in graph:
				if op.get_id() in v:
					id_list.append(op.get_id())
				else:
					continue
		return id_list


