# -*- coding: utf-8 -*- 
"""
Clase de representación problema QAP
José González Ayerdi
ITESM Campus Monterrey
03/2017  
"""
import numpy as np
import sys
from solution import Solution

from TT.Classes.data_readers.qap_data_reader import generate_lists


class QAP:
    def __init__(self):
        """inicialización de propiedades"""
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
    
    def read_data(self, filename=""):
        """read_data lee del archivo de pruebas el número de facilities/loactions y las matrices
        de distancia y flujo.
        Instances recuperadas de: http://anjos.mgi.polymtl.ca/qaplib//inst.html#EW"""
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
                    file_line = f.readline().split()
                    
                    print(len(file_line))
                    
                    for num in file_line:
                        # lo agregamos a la lista
                        line.append(int(num.strip()))
                    # agregamos el contenido de la línea a la matriz
                    self.flow_mat.append(line)
                # ignoramos un salto de línea
                # comentar cuando se lean archivos descargados de la pagina .
                last_pos = f.tell()
                nlines_skip = 1
                # ignoramos el salto de línea que existe entre ambas matrices en el archivo
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
        self.locations, self.facilities = generate_lists(self.distance_mat, self.flow_mat)
