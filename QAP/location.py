# -*- coding: utf-8 -*- 
"""
Clase para el objeto de ubicación del problema QAP.
José González Ayerdi - A01036121
ITESM Campus Monterrey
03/2017  
"""
class Location():

	"""Inicialización de clase y valores"""
	def __init__(self, loc_id=0, facility=None, distances=[]):
		self.loc_id    = loc_id
		self.facility  = facility
		self.distances = []

	"""set_distances establece las distancias entre la ubicación actual y todas las demás"""
	def set_distances(self, distance_mat):
		for loc in distance_mat[self.loc_id]:
			self.distances.append(loc)
		self.distances[self.loc_id] = -1

	"""distance_to obtiene la distancia entre la ubicación actual y la ubicación con id location_id"""
	def distance_to(self, location_id):
		return self.distances[location_id]

	"""get_adyacents_ids regresa una lista de ids correspondiente a las ubicaciones adyacentes a la actual"""
	def get_adyacents_ids(self):
		return [i for i, x in enumerate(self.distances) if x != 0 and x != -1]

