# -*- coding: utf-8 -*- 
'''Operation
Clase con la información correspondiente a cada operación
'''

class Operation:
    
    def __str__(self):
        return str(self.__op_id)

    def __init__(self, op_id='0_0', waits_for_m = True, self_id = 0, duration=0, start_time=0, end_time=0, machine=0, job=0, job_id=0, machine_id=0, fixed=False, machine_time_assigned=False):
        self.__op_id      = op_id
        self.__duration   = duration
        self.__start_time = start_time
        self.__end_time   = end_time
        self.__machine    = machine
        self.__job        = job
        self.__job_id     = job_id
        self.__machine_id = machine_id
        self.__assigned_machine_order = False
        self.__common_operations = []
        self.__start_times = []
        self.__fixed = fixed
        self.__machine_time_assigned = machine_time_assigned
        self.__self_id = self_id
        self.__waits_for_m = waits_for_m

    def waits_for_machine(self):
        return self.__waits_for_m

    def create_self_id(self, op_job):
        final = ''
        for char in op_job:
            if char != '_':
                final = final + char
            else:
                self.__self_id = int(final)

    def add_possible_start_time(self, time):
        self.__start_times.append(time)

    def has_machine_order(self):
        return self.__assigned_machine_order

    '''Sección para getters'''

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

    '''Sección para setters'''  
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
    
    def set_start_time(self):
        self.__start_time = max(self.__start_times)
    
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

    id_op      = property(get_id, set_id)
    duration   = property(get_duration, set_duration)
    start_time = property(get_start_time, set_start_time)
    end_time   = property(get_end_time, set_end_time)
    machine    = property(get_machine, set_machine)
    machine_id = property(get_machine_id, set_machine_id)
    job        = property(get_job, set_job)
    job_is     = property(get_job_id, set_job_id)
    fixed      = property(is_fixed, set_fixed)
    assigned_machine = property(get_assigned_machine, set_assigned_machine)

