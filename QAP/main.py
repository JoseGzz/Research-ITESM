import numpy as np
import sys

def main():
	flow_mat      = []
	distance_mat  = []
	no_facilities = 0
	file_name     = "chr15a.dat"
	distance_mat, flow_mat = read_data(flow_mat, distance_mat, no_facilities, file_name)
	#print(distance_mat)
	#print('----------------------------------------')
	#print(flow_mat)
	non_zero_val_coordinates = np.argwhere(flow_mat != 0)
	"""
	found_vals = []
	new_vals = []
	for val in non_zero_val_coordinates:
		new_0 = val[1]
		new_1 = val[0]
		lst = [new_0, new_1]
		found_vals.append(lst)
		if val in found_vals:
			new_vals.append(val)
	print(found_vals)
	"""
	#facilities, locations 

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