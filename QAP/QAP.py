# -*- coding: utf-8 -*- 
"""
Sistema de clases para el problema QAP
José González Ayerdi - A01036121
ITESM Campus Monterrey
03/2017  
"""
import numpy as np
import sys
from facility import Facility
from location import Location
from formatter import Formatter
from solution import Solution

class QAP():
	def __init__(self):
		self.locations = []
		self.facilities = []
		self.flow_mat = []
		self.distance_mat = []
		self.no_facilities = 0
		self.solution = None

	def random_solution(self):
		"""generamos una solución aleatoria para comenzar"""
		self.solution = Solution(self.locations, self.facilities)
		self.solution.generate_permutation(len(self.locations))
		self.solution.calculate_cost()
		
		return self.solution

	"""read_data lee del archivo de pruebas el número de facilities/loactions y las matrices
	de distancia y flujo. """
	def read_data(self, filename=""):
		filename = "test_data/had12.dat"
		try:
			with open(filename, 'r') as f:
				# leemos la cantidad de facilities
				self.no_facilities = f.readline() 
				# ignoramos un salto de línea
				f.readline()
				# por la cantidad de facilities                          
				for i in range(int(self.no_facilities)):
					# usaremos una lista para guardar cada elemento de la matriz   
					line = []
					# cada elemento en de la línea de la matriz                         
					for num in f.readline().split():
						# lo agregamos a la lista  
						line.append(int(num))
					# agregamos el contenido de la línea a la matriz         
					self.flow_mat.append(line)
				# ignoramos un salto de línea             
				f.readline()
				# repetimos para la segunda matriz                          
				for i in range(int(self.no_facilities)):   
					line = []
					for num in f.readline().split():
						line.append(int(num))
					self.distance_mat.append(line)
				self.distance_mat = np.array(self.distance_mat)
				self.flow_mat = np.array(self.flow_mat)
		except IOError as e:
			print("No se encontró el archivo.")
			sys.exit(0)
		# generamos listas de objetos para manipular mejor sus propiedades
		self.locations, self.facilities = Formatter().generate_lists(self.distance_mat, self.flow_mat)
