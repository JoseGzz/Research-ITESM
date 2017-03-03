# -*- coding: utf-8 -*- 
'''Job
Clase con la información correspondiente a cada tarea
'''

class Job:
    def __init__(self, id=0, start_time=0, end_time=0, operations=[]):
        self.id         = id
        self.start_time = start_time
        self.end_time   = end_time
        self.operations = operations

    '''Sección para getters'''

    def get_operations(self):
        return self.operations
    
    def get_id(self):
        return self.id
    
    def get_start_time(self):
        return self.start_time
    
    def get_end_time(self):
        return self.end_time

    '''Sección para setters'''

    def set_operations(self, operations):
        self.operations = operations
    
    def set_id(self, id):
        self.id = id
        
    def set_start_time(sef, start_time):
        self.start_time = start_time
        
    def set_end_time(self, end_time):
        end_time = end_time
        
    '''Se establecen la propiedades de la clase'''
    id         = property(get_id, set_id)
    start_time = property(get_start_time, set_start_time)
    end_time   = property(get_end_time, set_end_time)
    operations = property(get_operations, set_operations)
