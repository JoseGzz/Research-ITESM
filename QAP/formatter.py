
# -*- coding: utf-8 -*- 
"""
Sistema de clases para el problema QAP
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
		locations_list = self.generate_locations(distance_mat)
		facility_list  = self.generate_facilities(flow_mat)

	def generate_locations(self, distance_mat):
		pass

	def generate_facilities(self, flow_mat):
		pass


