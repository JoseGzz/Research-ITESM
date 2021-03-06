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
import settings


class Solution:
    def __init__(self, locations=[], facilities=[], p=[]):
        """Inicialización de objeto y valores."""
        self.facilities = facilities
        self.locations = locations
        self.p = p
        self.travel_cost = 0
        self.debug = False
        self.benchmark = True
    
    def generate_permutation(self, no_locations):
        """generate_permutation genera una permutación acomodando facilities (valores de la lista p)
        en ciertas ubicaciones (índices de la lista p). Mientras hace el recorrido asigna las correspondientes
        ubicaciones y facilities a los objetos."""
        """IMPORTANTE: para problemas benchmark en http://anjos.mgi.polymtl.ca/qaplib//inst.html#EW
        los indices de la lista representan los id de los facilities, y los valores las locations."""
        
        # generación de permutación aleatoria
        self.p = random.sample(range(no_locations), no_locations)
        
        # se puede ejecutar una permutación especificada manualmente
        # self.set_test_permutation()
        # generamos objetos para graficación
        self.generate_lists_for_plot()
    
    def set_test_permutation(self):
        # se pude especificar una permutación específica para verificar resultados
        # es necesario también especificar la permutación en la función de perturbación.
        # Se necesita también prender la bandera de debug para cambiar a índice 0.
        # por ejemplo: self.p = [12,7,9,3,4,8,11,1,5,6,10,2]
        self.p = []
        for i, _ in enumerate(self.p):
            self.p[i] = self.p[i] - 1
    
    def generate_lists_for_plot(self):
        """llena listas que se usarán para graficar"""
        locations = []
        facilities = []
        for i, fac in enumerate(self.p):
            loc = self.search_location_obj(i)
            facility = self.search_facility(fac)
            loc.facility = facility
            facility.location = loc
            locations.append(loc)
            facilities.append(facility)
    
    def create_neighbor(self):
        """perturbamos la solución actual"""
        # escogemos dos facilities al azar
        fac1, fac2 = random.sample(self.p, 2)
        # las intercambiamos
        fac1_index, fac2_index = self.p.index(fac1), self.p.index(fac2)

        ###################### START DATA COLLECTION ########################
        if settings.options.collect_data:
            if fac1_index == 0:
                settings.collector.add_data("first_fac_moved", True)
            else:
                settings.collector.add_data("first_fac_moved", False)
    
            if fac2_index == len(self.p) - 1:
                settings.collector.add_data("last_fac_moved", True)
            else:
                settings.collector.add_data("last_fac_moved", False)

            settings.collector.add_data("moves", abs(fac1_index - fac2_index))
        ###################### END DATA COLLECTION ##########################
        
        self.p[fac2_index], self.p[fac1_index] = self.p[fac1_index], self.p[fac2_index]
        
        # se puede especificar una permutación particular para verificar resultados
        # set test permutation
        # generamos las nuevas listas de objetos para graficar
        self.generate_lists_for_plot()
        # calculamos el nuevo costo
        self.calculate_cost()
        return self
    
    def calculate_cost(self):
        """calculate_cost hace el producto punto entre los vectores de flujos y distancias y regresa el resultado."""
        flows, fac_ids = self.calculate_flows()
        distances = self.calculate_distances(fac_ids)
        flows = np.array(flows)
        distances = np.array(distances)
        self.travel_cost = distances.dot(flows)
    
    def calculate_flows(self):
        """calculate_flows calcula el flujo entre dos facilities para cada una en la lista."""
        flow_list = []
        fac_ids = []
        for i in range(len(self.facilities)):
            for j in range(i, len(self.facilities)):
                flow_list.append(self.facilities[i].flow_with(self.facilities[j].fac_id))
                fac_ids.append((i, j))
        return flow_list, fac_ids
    
    def calculate_distances(self, fac_ids):
        """calculate_distances calcula la distancia entre dos ubicaciones para cada una en la lista."""
        distances = []
        for ids in fac_ids:
            fac1_loc = self.p[ids[0]] if self.benchmark else self.p.index(ids[0])
            fac2_loc = self.p[ids[1]] if self.benchmark else self.p.index(ids[1])
            loc1 = self.search_location_obj(fac1_loc)
            loc2 = self.search_location_obj(fac2_loc)
            # hay que sumar las distancias de ida y de vuelta
            distance = loc1.distance_to(loc2.loc_id) + loc2.distance_to(loc1.loc_id)
            distances.append(distance)
        return distances
    
    def search_location_obj(self, loc_id):
        """search_location_obj regresa un objeto location dado su id."""
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
        """regresa el costo de la solución actual"""
        return self.travel_cost
    
    def permutation(self):
        """muestra la permutación final con inice 1"""
        for i, _ in enumerate(self.p):
            self.p[i] = self.p[i] + 1
        return self.p
