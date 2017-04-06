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
from solver import Solver
from plotter import Plotter

def main():
	flow_mat      = []
	distance_mat  = []
	no_facilities = 0
	
	#file_name     = "test_data/chr15a.dat"
	file_name     = "test_data/test.dat"
	# lectura de archivos de prueba
	distance_mat, flow_mat = read_data(flow_mat, distance_mat, no_facilities, file_name)
	# generamos listas de objetos para manipular mejor sus propiedades
	locations, facilities  = Formatter().generate_lists(distance_mat, flow_mat)

	"""
	# imprime las distancias entre ubicaciones para probar
	for loc in locations:
		print("location #", loc.loc_id)
		for dis in loc.distances:
			print(dis)

	# imprime los flujos entre facilities para probar
	for fac in facilities:
		print("facility #", fac.fac_id)
		for flow in fac.flows:
			print(flow)
	"""

	# incializamos la clase solver para generar una permutacion
	# y obtener las listas de objetos con sus ubicaciones y facilities asignados.
	# calculamos el costo total y graficamos los resultados.
	s = Solver(locations, facilities)
	locations, facilities, permutation = s.generate_permutation(len(locations))
	cost = s.calculate_cost()
	print("Costo total:", cost)
	pt = Plotter(locations, facilities, permutation, cost)
	pt.plot_results()

	"""
	# imprime las distancias entre ubicaciones para probar
	for loc in locations:
		print("location #", loc.loc_id)
		print("has fac #", loc.facility.fac_id)
		for dis in loc.distances:
			print(dis)

	# imprime los flujos entre facilities para probar
	for fac in facilities:
		print("facility #", fac.fac_id)
		print("has location #", fac.location.loc_id)
		for flow in fac.flows:
			print(flow)
	"""

"""read_data lee del archivo de pruebas el número de facilities/loactions y las matrices
de distancia y flujo. """
def read_data(flow_mat, distance_mat, no_facilities, file_name):
	try:
		with open(file_name, "r+") as f:
			# leemos la cantidad de facilities
			no_facilities = f.readline() 
			# ignoramos un salto de línea
			f.readline()
			# por la cantidad de facilities                          
			for i in range(int(no_facilities)):
				# usaremos una lista para guardar cada elemento de la matriz   
				line = []
				# cada elemento en de la línea de la matriz                         
				for num in f.readline().split():
					# lo agregamos a la lista  
					line.append(int(num))
				# agregamos el contenido de la línea a la matriz         
				flow_mat.append(line)
			# ignoramos un salto de línea             
			f.readline()
			# repetimos para la segunda matriz                          
			for i in range(int(no_facilities)):   
				line = []
				for num in f.readline().split():
					line.append(int(num))
				distance_mat.append(line)
			distance_mat = np.array(distance_mat)
			flow_mat = np.array(flow_mat)
			return distance_mat, flow_mat
	except IOError as e:
		print("No se encontró el archivo.")
		sys.exit(0)
    
if __name__ == "__main__":
    main()