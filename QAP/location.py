class Location():

	def __init__(self, loc_id=0, facility=None, distances=[]):
		self.loc_id = loc_id
		self.facility = facility
		self.distances = []

	def set_distances(self, distance_mat):
		for loc in distance_mat[self.loc_id]:
			self.distances.append(loc)
		self.distances[self.loc_id] = -1

	def distance_to(self, location_id):
		return self.distances[location_id]

	def get_adyacents_ids(self):
		return [i for i, x in enumerate(self.distances) if x != 0 and x != -1]

