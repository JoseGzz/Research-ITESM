# -*- coding: utf-8 -*- 
"""
Sistema de clases para el problema QAP
José González Ayerdi - A01036121
ITESM Campus Monterrey
03/2017
"""
class Facility():
	def __init__(self, fac_id=0, flows=[], location=None):
		self.fac_id   = fac_id
		self.flows    = []
		self.location = location

	def set_flows(self, flow_mat):
		for fac in flow_mat[self.fac_id]:
			self.flows.append(fac)
		self.flows[self.fac_id] = -1

	def flow_with(self, fac_id):
		return self.flows[fac_id]


