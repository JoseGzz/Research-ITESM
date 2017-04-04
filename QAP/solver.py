import numpy as np

class Solver():
	def __init__(self, locations=[], facilities=[], p=[]):
		self.facilities = facilities
		self.locations	= locations
		self.p = p

	def generate_permutation(self, no_locations):
		print(np.random.randint(no_locations, size=no_locations))
		self.p = np.random.randint(no_locations, size=no_locations)
		#self.p = [1,0,3,2]


	def get_total_time(self):
		flows, fac_ids 	  = self.calculate_flows()
		distances         = self.calculate_distances(fac_ids)
		flows = np.array(flows)
		distances = np.array(distances)

		return flows.dot(distances)


	def calculate_flows(self):
		flow_list = []
		fac_ids   = []
		for i in range(len(self.facilities)):
			for j in range(i, len(self.facilities)):
				current_flow = self.facilities[i].flow_with(self.facilities[j].fac_id)
				if current_flow != 0 and current_flow != -1:
					flow_list.append(current_flow)
					fac_ids.append((i, j))
		return flow_list, fac_ids


	def calculate_distances(self, fac_ids):
		distances = []
		for ids in fac_ids:
			fac1_loc = self.p[ids[0]]
			fac2_loc = self.p[ids[1]]
			loc1 = self.search_location(fac1_loc)
			loc2 = self.search_location(fac2_loc)
			distance = loc1.distance_to(loc2.loc_id)
			distances.append(distance)
		return distances

	def search_location(self, loc_id):

		for location in self.locations:
			if location.loc_id == loc_id:
				return location







