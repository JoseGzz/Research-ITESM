# -*- coding: utf-8 -*- 
'''Machine
Clase con la información correspondiente a cada máquina 
'''
class Machine:

    '''Constructor con valoes opcionales'''
    def __init__(self, id=0, operations=[]):
        self.id               = id
        self.operations       = operations
        self.total_operations = len(operations)
    
    '''Se agrega una operacion para ser ejecutada por esa máquina'''
    def add_operation(operation):
        operations.append(operation)
    '''Elimina la operación especificada'''
    def remove_operation(self, operation):
        self.operations.remove(operation)
    
    '''Sección para setters''' 

    def set_id(self, id):
        self.id = id
    
    def set_operations(self, operations):
        self.operations = operations
    
    def set_total_operations(self, total_operations):
        self.total_operations = total_operations
    
    '''Sección para getters'''
    def get_id(self):
        return self.id
    
    def get_operations(self):
        return self.operations
    
    def get_total_operations(self):
        return self.total_operations
    
    '''Se establecen la propiedades de la clase'''
    id               = property(set_id, get_id)
    operations       = property(set_operations, get_operations)
    total_operations = property(set_total_operations, get_total_operations)