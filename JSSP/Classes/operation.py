# -*- coding: utf-8 -*- 
"""Operation
Clase con la información correspondiente a cada operación
José González Ayerdi
ITESM Campus Monterrey
02/2017
"""

class Operation:
    
    def __init__(self, op_id='0_0', common_operations=[], start_times=[], waits_for_m = True, self_id = 0, duration=0, start_time=0, end_time=0, machine=0, job=0, job_id=0, machine_id=0, fixed=False, machine_time_assigned=False):
        """constructor de la clase operation"""
        self.__op_id                  = op_id
        self.__duration               = duration
        self.__start_time             = start_time
        self.__end_time               = end_time
        self.__machine                = machine
        self.__job                    = job
        self.__job_id                 = job_id
        self.__machine_id             = machine_id
        self.__assigned_machine_order = False
        self.__common_operations      = common_operations
        self.__start_times            = []
        self.__fixed                  = fixed
        self.__machine_time_assigned  = machine_time_assigned
        self.__self_id                = self_id
        self.__waits_for_m            = waits_for_m
        self.debug = False

    """Regresa verdadero si la operación está esperando que se le asigne un tiempo por máquina."""
    def waits_for_machine(self):
        return self.__waits_for_m

    """Se obtiene el id de la operación sin el id de la tarea."""
    def create_self_id(self, op_job):
        final = ''
        for char in op_job:
            if char != '_':
                final = final + char
            else:
                self.__self_id = int(final)

    """Se agrega un tiempo tentativo de inicio para la oepración."""

    def add_possible_start_time(self, time):
        #print("Soy", self.__op_id, " y recibí tiempo:", time)
        self.__start_times.append(time)

    """Pregunta si ya se le asignó un orden de ejecución en la máquina."""
    def has_machine_order(self):
        return self.__assigned_machine_order

    """Sección para getters"""

    def get_possible_times(self):
        return self.__start_times

    def get_self_id(self):
        return self.__self_id

    def has_machine_time_assigned(self):
        return self.__machine_time_assigned

    def is_fixed(self):
        return self.__fixed

    def get_common_operations(self):
        return self.__common_operations

    def get_id(self):
        return self.__op_id    
    
    def get_start_time(self):
        return self.__start_time

    def get_start_times(self):
        return self.__start_times
    
    def get_duration(self):
        return self.__duration
    
    def get_end_time(self):
        return self.__end_time
    
    def get_machine(self):
        return self.__machine
    
    def get_machine_id(self):
        return self.__machine_id
    
    def get_job(self):
        return self.__job
    
    def get_job_id(self):
        return self.__job_id
    
    def get_assigned_machine(self):
        return self.__assigned_machine

    def get_machine_order(self):
        return self.__assigned_machine_order

    def get_machine_time_assigned(self):
        return self.__machine_time_assigned

    def get_waits_for_machine(self):
        return self.__waits_for_m

    """Sección para setters""" 

    def set_waits_for_machine(self, waits_for_m):
        self.__waits_for_m = waits_for_m

    def set_machine_time_assigned(self, machine_time_assigned):
        self.__machine_time_assigned = machine_time_assigned

    def set_self_id(self, self_id):
        self.__self_id = self_id

    def set_fixed(self, fixed):
        self.__fixed = fixed

    def set_machine_order(self, assigned_machine_order):
        self.__assigned_machine_order = assigned_machine_order

    def set_job_id(self, job_id):
        self.__job_id = job_id
    
    def set_id(self, self_job):
        self.__op_id = self_job
        self.create_self_id(self.__op_id)
    
    def set_job(self, job):
        self.__job = job
    
    def set_start_time(self, time):
        self.__start_time = time
        if self.debug:
            for time in self.__start_times:
                print("tiempo::", time)
        
    def set_duration(self, duration):
        self.__duration = duration
        
    def set_end_time(self,end_time):
        self.__end_time = end_time
    
    def set_machine(self, machine):
        self.__machine = machine
    
    def set_machine_id(self, machine_id):
        self.__machine_id = machine_id

    def set_common_operations(self, common_operations):
        self.__common_operations = common_operations
    
    def set_assigned_machine(self, assigned_machine):
        self.__assigned_machine = assigned_machine

    """Se establecen la propiedades de la clase."""
    op_id             = property(get_id, set_id)
    self_id           = property(get_self_id, set_self_id)
    common_operations = property(get_common_operations, set_common_operations)
    duration          = property(get_duration, set_duration)
    start_time        = property(get_start_time, set_start_time, add_possible_start_time)
    end_time          = property(get_end_time, set_end_time)
    machine           = property(get_machine, set_machine)
    machine_id        = property(get_machine_id, set_machine_id)
    job               = property(get_job, set_job)
    job_is            = property(get_job_id, set_job_id)
    fixed             = property(is_fixed, set_fixed)
    waits_for_m       = property(get_waits_for_machine, set_waits_for_machine)
    assigned_machine  = property(get_assigned_machine, set_assigned_machine)
    machine_time_assigned  = property(set_machine_time_assigned, get_machine_time_assigned)
    assigned_machine_order = property(get_machine_order , set_machine_order)

