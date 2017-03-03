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
		for op_id, lst in graph.iteritems():
			duration = lst[0].get_duration()
			# si es un primer proceso
			if op_id[0] in first_op_ids:
				graph[op_id][0] = graph[op_id][0].set_start_time([0])

			iterops = iter(lst)
			next(iterops)
			   for next_op in iterops:
			   	next_op.add_start_time(duration)
			# iterate over all operations on lst and call set_tart_time() 


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
			#        if waiting a start time based on machine order
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


	    # for op_id, lst in graph.iteritems():
	    #	operation = lst[0]
		# Ask if no machine order has been assign for this operation
		# if no order then choose a random order and put the next processing operation in the values list and mark all of them as assigned
		# else if order assigned then ignore.
		# For each key, use previous finish times (of nodes pointing to this one) and choose the largest,
		# then sum the own duration time and pass it to the next nodes
		# search node with largest time (makespan)
		return graph

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
				if op.get_id() not in v:
					continue
				else:
					id_list.append(op.get_id())
		return id_list


