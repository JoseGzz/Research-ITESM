# -*- coding: utf-8 -*- 
"""Job
Clase con la información correspondiente a cada tarea
a listas con máquinas, tareas y operaciones.
José González Ayerdi - A01036121
ITESM Campus Monterrey
02/2017
"""

class Job:
    def __init__(self, job_id=0, start_time=0, end_time=0, operations=[]):
        self.__job_id     = job_id
        self.__start_time = start_time
        self.__end_time   = end_time
        self.__operations = operations

    """Sección para getters"""

    def get_operations(self):
        return self.__operations
    
    def get_id(self):
        return self.__job_id
    
    def get_start_time(self):
        return self.__start_time
    
    def get_end_time(self):
        return self.__end_time

    def get_op_count(self):
        return len(self.__operations)

    """Sección para setters"""

    def set_operations(self, operations):
        self.__operations = operations
    
    def set_id(self, job_id):
        self.__job_id = job_id
        
    def set_start_time(self, start_time):
        self.__start_time = start_time
        
    def set_end_time(self, end_time):
        self.__end_time = end_time
        
    """Se establecen la propiedades de la clase."""
    id_job     = property(get_id, set_id)
    start_time = property(get_start_time, set_start_time)
    end_time   = property(get_end_time, set_end_time)
    operations = property(get_operations, set_operations)
