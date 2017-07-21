# -*- coding: utf-8 -*-
from solutions.solution import Solution
from .data_reader import DataReader
from solutions.qap_solution import Location, Facility, QapSolution
import sys
import numpy as np


def generate_locations(distance_mat):
    """generate_locations regresa la lista de objetos location con su id y distancias"""
    location_list = []
    for i in range((len(distance_mat))):
        location = Location(loc_id=i)
        location.set_distances(distance_mat)
        location_list.append(location)
    return location_list


def generate_facilities(flow_mat):
    """generate_facilities regresa la lista de objetos facility con su id y flujos"""
    facility_list = []
    for i in range((len(flow_mat))):
        facility = Facility(fac_id=i)
        facility.set_flows(flow_mat)
        facility_list.append(facility)
    return facility_list


def generate_lists(distance_mat, flow_mat):
    """generate_lists regresa las listas de objetos location y facility para usarse en el problema"""
    location_list = generate_locations(distance_mat)
    facility_list = generate_facilities(flow_mat)
    return location_list, facility_list


class QapDataReader(DataReader):
    def read(self, source_filename):
        """read_data lee del archivo de pruebas el número de facilities/loactions y las matrices
                de distancia y flujo.
                Instances recuperadas de: http://anjos.mgi.polymtl.ca/qaplib//inst.html#EW"""
        try:
            with open(source_filename, 'r') as f:
                flow_mat = []
                distance_mat = []
   
                # leemos la cantidad de facilities
                no_facilities = f.readline()
                # ignoramos un salto de línea
                f.readline()
                # por la cantidad de facilities
                for i in range(int(no_facilities)):
                    # usaremos una lista para guardar cada elemento de la matriz
                    line = []
                    # cada elemento en de la línea de la matriz
                    file_line = f.readline().split()
                
                    for num in file_line:
                        # lo agregamos a la lista
                        line.append(int(num.strip()))
                    # agregamos el contenido de la línea a la matriz
                    flow_mat.append(line)

                # ignoramos el salto de línea que existe entre ambas matrices en el archivo
                f.readline()
                # repetimos para la segunda matriz
                
                for i in range(int(no_facilities)):
                    line = []
                    for num in f.readline().split():
                        line.append(int(num))
                    distance_mat.append(line)
                    
                distance_mat = np.array(distance_mat)
                flow_mat = np.array(flow_mat)

                # generamos listas de objetos para manipular mejor sus propiedades
                locations, facilities = generate_lists(distance_mat, flow_mat)
                solution = QapSolution(locations, facilities)
                solution.calculate_cost()
                return solution
        except IOError as _:
            print("No se encontró el archivo.")
            sys.exit(0)
