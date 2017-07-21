# -*- coding: utf-8 -*-
from .solution import Solution
import random
import numpy as np
import copy as cp
import settings.qap_settings as settings


class QapSolution(Solution):
    @property
    def facilities(self):
        return self._facilities
    
    @facilities.setter
    def facilities(self, new_value):
        self._facilities = new_value
    
    @property
    def locations(self):
        return self._locations
    
    @locations.setter
    def locations(self, new_value):
        self._locations = new_value
    
    @property
    def p(self):
        return self._p
    
    @p.setter
    def p(self, new_p):
        self._p = new_p
    
    def __init__(self, locations, facilities, p=None):
        super(QapSolution, self).__init__()
        self._facilities = facilities
        self._locations = locations
        self._p = p if p is not None else random.sample(range(len(self.locations)), len(self.locations))
        self._travel_cost = 0
        self.calculate_cost()
    
    def does_violate_constraint(self):
        """For this instance of QAP, there are no constraints that could be violated."""
        return False
    
    def permute(self, heuristic):
        ###################### START DATA COLLECTION ########################
        if settings.options.collect_data:
            settings.collector.add_data("num_jobs", len(self.facilities))
            settings.collector.add_data("num_machines", len(self.locations))
        ###################### END DATA COLLECTION ##########################
        return heuristic.permute(cp.deepcopy(self))
    
    def cost(self):
        return self._travel_cost
    
    def calculate_cost(self):
        """ calculate_cost hace el producto punto entre los vectores de flujos
            y distancias y regresa el resultado. """
        flows, fac_ids = self.calculate_flows()
        distances = self.calculate_distances(fac_ids)
        flows = np.array(flows)
        distances = np.array(distances)
        
        self._travel_cost = distances.dot(flows)
    
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
            fac1_loc = self.p[ids[0]]
            fac2_loc = self.p[ids[1]]
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
    
    def __str__(self):
        """ For this instance, each element e at position i represents such a location e
            at location i. """
        result = []
        for value in self.p:
            result.append(value + 1)
        
        return str(result)


"""
Clase para el objeto facility del problema QAP.
José González Ayerdi
ITESM Campus Monterrey
03/2017
"""


class Facility:
    def __init__(self, fac_id=0, flows=[], location=None):
        """Inicialización de clase y valores"""
        self.fac_id = fac_id
        self.flows = []
        self.location = location
    
    def set_flows(self, flow_mat):
        """set_flows asigna a la facility actual los flujos con todas las demás facilities"""
        for fac in flow_mat[self.fac_id]:
            self.flows.append(fac)
        self.flows[self.fac_id] = 0
    
    def flow_with(self, fac_id):
        """flow_with regresa el flujo entre la facility actual y la facility con id fac_id"""
        return self.flows[fac_id]


"""
Clase para el objeto de ubicación del problema QAP.
José González Ayerdi
ITESM Campus Monterrey
03/2017
"""


class Location:
    def __init__(self, loc_id=0, facility=None, distances=[]):
        """inicialización de clase y valores"""
        self.loc_id = loc_id
        self.facility = facility
        self.distances = []
    
    def set_distances(self, distance_mat):
        """set_distances establece las distancias entre la ubicación actual y todas las demás"""
        for loc in distance_mat[self.loc_id]:
            self.distances.append(loc)
        self.distances[self.loc_id] = 0
    
    def distance_to(self, location_id):
        """distance_to obtiene la distancia entre la ubicación actual y la ubicación con id location_id"""
        return self.distances[location_id]
    
    def get_adyacents_ids(self):
        """get_adyacents_ids regresa una lista de ids correspondiente a las ubicaciones adyacentes a la actual"""
        return [i for i, x in enumerate(self.distances) if x != 0 and x != -1]
