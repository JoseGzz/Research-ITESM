
# -*- coding: utf-8 -*- 
"""
Clase para generar lista de objetos a manipular según QAP.
José González Ayerdi - A01036121
ITESM Campus Monterrey
03/2017  
"""
from facility import Facility
from location import Location

class Formatter():
	def __init__(self):
		pass

	def generate_lists(self, distance_mat, flow_mat):
		location_list = self.generate_locations(distance_mat)
		facility_list  = self.generate_facilities(flow_mat)
		return location_list, facility_list

	def generate_locations(self, distance_mat):
		location_list = []
		for i in range((len(distance_mat))):
			location = Location(loc_id=i)
			location.set_distances(distance_mat)
			location_list.append(location)
		return location_list

	def generate_facilities(self, flow_mat):
		facility_list = []
		for i in range((len(flow_mat))):
			facility = Facility(fac_id=i)
			facility.set_flows(flow_mat)
			facility_list.append(facility)
		return facility_list
		


