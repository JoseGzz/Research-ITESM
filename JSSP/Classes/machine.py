# -*- coding: utf-8 -*- 
"""Machine
Clase con la información correspondiente a cada máquina 
José González Ayerdi - A01036121
ITESM Campus Monterrey
02/2017
"""
class Machine:

    """Constructor con valoes opcionales"""
    def __init__(self, m_id=0, operations=[]):
        self.__m_id             = m_id
        self.__operations       = operations
        self.__total_operations = len(operations)
    
    """Se agrega una operacion para ser ejecutada por esa máquina"""
    def add_operation(self, operation):
        self.__operations.append(operation)

    """Elimina la operación especificada"""
    def remove_operation(self, operation):
        self.__operations.remove(operation)
    
    """Sección para setters""" 

    def set_id(self, m_id):
        self.__m_id = m_id
    
    def set_operations(self, operations):
        self.__operations = operations
    
    def set_total_operations(self, total_operations):
        self.__total_operations = total_operations
    
    """Sección para getters"""
    def get_id(self):
        return self.__m_id
    
    def get_operations(self):
        return self.__operations
    
    def get_total_operations(self):
        return self.__total_operations
    
    """Se establecen la propiedades de la clase"""
    m_id             = property(set_id, get_id)
    operations       = property(set_operations, get_operations)
    total_operations = property(set_total_operations, get_total_operations)