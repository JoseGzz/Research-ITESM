class Solver():
	def __init__(self):

	def get_total_time(self, facilities, locations, p):
		flow_list = 0
		for i in range(len(fac)):
			for j in range(len(fac)-i):
				current_flow = facilities[i].flow_with(facilities[j])
				if current_flow != 0 and current_flow != -1:
					flow_list.append(current_flow)
		return flow_list



