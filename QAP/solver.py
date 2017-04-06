# -*- coding: utf-8 -*- 
"""
Función de costo para el problema QAP.
José González Ayerdi - A01036121
ITESM Campus Monterrey
03/2017  
"""
import numpy as np
import random

class Solver():
	"""Inicialización de objeto y valores."""
	def __init__(self, locations=[], facilities=[], p=[]):
		self.facilities = facilities
		self.locations	= locations
		self.p          = p

	"""generate_permutation genera una permutación acomodando facilities (valores de la lista p)
	en ciertas ubicaciones (índices de la lista p). Mientras hace el recorrido asigna las correspondientes
	ubicaciones y facilities a los objetos."""
	def generate_permutation(self, no_locations):
		self.p = random.sample(range(no_locations), no_locations)
		#self.p = [1,0,3,2]
		locations = []
		facilities = []
		for i, fac in enumerate(self.p):
			loc = self.search_location(i)
			facility = self.search_facility(fac)
			loc.facility = facility
			facility.location = loc
			locations.append(loc)
			facilities.append(facility)
		return locations, facilities, self.p

	"""calculate_cost multiplica los vectores de flujos y distancias y regresa el resultado."""
	def calculate_cost(self):
		flows, fac_ids 	  = self.calculate_flows()
		distances         = self.calculate_distances(fac_ids)
		flows             = np.array(flows)
		distances         = np.array(distances)
		return flows.dot(distances)

	"""calculate_flows calcula el flujo entre dos facilities para cada una en la lista."""
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

	"""calculate_distances calcula la distancia entre dos ubicaciones para cada una en la lista."""
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

	"""search_location regresa un objeto location dado su id."""
	def search_location(self, loc_id):
		for location in self.locations:
			if location.loc_id == loc_id:
				return location

	"""search_facility regresa un objeto facility dado su id."""
	def search_facility(self, fac_id):
		for facility in self.facilities:
			if facility.fac_id == fac_id:
				return facility






