# -*- coding: utf-8 -*- 
"""
Función de costo para el problema QAP.
José González Ayerdi - A01036121
ITESM Campus Monterrey
03/2017  
"""
import numpy as np
import random
from plotter import Plotter

class Solution():
	def __init__(self, locations=[], facilities=[], p=[]):
		"""Inicialización de objeto y valores."""
		self.facilities  = facilities
		self.locations	 = locations
		self.p           = p
		self.travel_cost = 0

	def generate_permutation(self, no_locations):
		"""generate_permutation genera una permutación acomodando facilities (valores de la lista p)
		en ciertas ubicaciones (índices de la lista p). Mientras hace el recorrido asigna las correspondientes
		ubicaciones y facilities a los objetos."""
		self.p = random.sample(range(no_locations), no_locations)
		#self.p = [1,0,3,2]
		#self.p = [1,2,3,0]
		#self.p = [0,1,2,3] #inicial para test2.dat
		#self.p = [2,3,0,1] #optima para test2.dat
		#self.p = [0,1,2,3]
		#self.p = [5,10,8,13,12,11,14,2,4,6,7,15,3,1,9]
		#self.p = [8,1,6,2,11,10,3,5,9,7,12,4]
		"""
		for i, _ in enumerate(self.p):
			self.p[i] = self.p[i] - 1
		"""
		
		self.generate_lists_for_plot()

	def generate_lists_for_plot(self):
		locations = []
		facilities = []
		for i, fac in enumerate(self.p):
			loc = self.search_location(i)
			facility = self.search_facility(fac)
			loc.facility = facility
			facility.location = loc
			locations.append(loc)
			facilities.append(facility)
		

	def create_neighbor(self):
		fac1, fac2 = random.sample(self.p, 2)
		fac1_index, fac2_index = self.p.index(fac1), self.p.index(fac2)
		self.p[fac2_index], self.p[fac1_index] = self.p[fac1_index], self.p[fac2_index]
		self.generate_lists_for_plot()
		self.calculate_cost()
		print(self.p)
		return self


	def calculate_cost(self):
		"""calculate_cost multiplica los vectores de flujos y distancias y regresa el resultado."""
		flows, fac_ids = self.calculate_flows()
		distances      = self.calculate_distances(fac_ids)
		flows          = np.array(flows)
		distances      = np.array(distances)
		self.travel_cost = flows.dot(distances)

	def calculate_flows(self):
		"""calculate_flows calcula el flujo entre dos facilities para cada una en la lista."""
		flow_list = []
		fac_ids   = []
		for i in range(len(self.facilities)):
			for j in range(i, len(self.facilities)):
				current_flow = self.facilities[i].flow_with(self.facilities[j].fac_id)
				if current_flow != -1:
					flow_list.append(current_flow)
					fac_ids.append((i, j))
		return flow_list, fac_ids

	def calculate_distances(self, fac_ids):
		"""calculate_distances calcula la distancia entre dos ubicaciones para cada una en la lista."""
		distances = []
		for ids in fac_ids:
			fac1_loc = self.p.index(ids[0])
			fac2_loc = self.p.index(ids[1])
			loc1 = self.search_location(fac1_loc)
			loc2 = self.search_location(fac2_loc)
			distance = loc1.distance_to(loc2.loc_id)
			distances.append(distance)
		return distances

	def search_location(self, loc_id):
		"""search_location regresa un objeto location dado su id."""
		for location in self.locations:
			if location.loc_id == loc_id:
				return location

	def search_facility(self, fac_id):
		"""search_facility regresa un objeto facility dado su id."""
		for facility in self.facilities:
			if facility.fac_id == fac_id:
				return facility

	def plot(self, fig, flag=True):
		"""plot grafica la solución actual."""
		if flag:
			pt = Plotter(self.locations, self.facilities, self.p, self.travel_cost)
			pt.plot_results(fig)

	def cost(self):
		return self.travel_cost


