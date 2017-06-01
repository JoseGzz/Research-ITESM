# -*- coding: utf-8 -*- 
"""
Clase para el objeto de ubicación del problema QAP.
José González Ayerdi
ITESM Campus Monterrey
03/2017  
"""
class Location():

	def __init__(self, loc_id=0, facility=None, distances=[]):
		"""inicialización de clase y valores"""
		self.loc_id    = loc_id
		self.facility  = facility
		self.distances = []

	def set_distances(self, distance_mat):
		"""set_distances establece las distancias entre la ubicación actual y todas las demás"""
		for loc in distance_mat[self.loc_id]:
			self.distances.append(loc)
		self.distances[self.loc_id] = 0

	def distance_to(self, location_id):
		"""distance_to obtiene la distancia entre la ubicación actual y la ubicación con id location_id"""
		return self.distances[location_id]

	def get_adyacents_ids(self):
		"""get_adyacents_ids regresa una lista de ids correspondiente a las ubicaciones adyacentes a la actual"""
		return [i for i, x in enumerate(self.distances) if x != 0 and x != -1]

