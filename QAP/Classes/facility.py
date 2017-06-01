# -*- coding: utf-8 -*- 
"""
Clase para el objeto facility del problema QAP.
José González Ayerdi
ITESM Campus Monterrey
03/2017
"""
class Facility():

	def __init__(self, fac_id=0, flows=[], location=None):
		"""Inicialización de clase y valores"""
		self.fac_id   = fac_id
		self.flows    = []
		self.location = location

	def set_flows(self, flow_mat):
		"""set_flows asigna a la facility actual los flujos con todas las demás facilities"""
		for fac in flow_mat[self.fac_id]:
			self.flows.append(fac)
		self.flows[self.fac_id] = 0

	def flow_with(self, fac_id):
		"""flow_with regresa el flujo entre la facility actual y la facility con id fac_id"""
		return self.flows[fac_id]


