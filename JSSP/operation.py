# -*- coding: utf-8 -*- 
'''Operation
Clase con la información correspondiente a cada operación
'''

class Operation:
    def __init__(self, id='0_0', duration=0, start_time=0, end_time=0, machine=0, job=0, job_id=0, machine_id=0, fixed=False, machine_time_assigned=False):
        self.id         = id
        self.duration   = duration
        self.start_time = start_time
        self.end_time   = end_time
        self.machine    = machine
        self.job        = job
        self.job_id     = job_id
        self.machine_id = machine_id
        self.assigned_machine_order = False
        self.common_operations = []
        self.start_times = []
        self.fixed = fixed
        self.machine_time_assigned = machine_time_assigned


    def add_possible_start_time(self, time):
        start_time.append(time)

    def has_machine_order(self):
        return self.assigned_machine_order

    '''Sección para getters'''

    def has_machine_time_assigned(self):
        return self.machine_time_assigned

    def is_fiexd(self):
        return self.fixed

    def get_common_operations(self):
        return common_operations

    def get_id(self):
        return self.id    
    
    def get_start_time(self):
        return self.start_time
    
    def get_duration(self):
        return self.duration
    
    def get_end_time(self):
        return self.start_time + duration
    
    def get_machine(self):
        return self.machine
    
    def get_machine_id(self):
        return self.machine_id
    
    def get_job(self):
        return self.job
    
    def get_job_id(self):
        return self.job_id
    
    '''Sección para setters'''
    def set_machine_time_assigned(self, machine_time_assigned):
        self.machine_time_assigned = machine_time_assigned

    def set_fixed(sefl, fixed):
        self.fixed = fixed

    def set_machine_order(self, assigned_machine):
        self.assigned_machine = assigned_machine

    def set_job_id(self, job_id):
        self.job_id = job_id
    
    def set_id(self, id):
        self.id = id
    
    def set_job(self, job):
        self.job = job
    
    def set_start_time(self):
        self.start_time = max(start_times)
    
    def set_duration(self, duration):
        self.duration = duration
        
    def set_end_time(self,end_time):
        self.end_time = end_time
    
    def set_machine(self, machine):
        self.machine = machine
    
    def set_machine_id(self, machine_id):
        self.machine_id = machine_id

    def set_common_operations(self, common_operations):
        self.common_operations = common_operations
    
    id         = property(get_id, set_id)
    duration   = property(get_duration, set_duration)
    start_time = property(get_start_time, set_start_time)
    end_time   = property(get_end_time, set_end_time)
    machine    = property(get_machine, set_machine)
    machine_id = property(get_machine_id, set_machine_id)
    job        = property(get_job, set_job)
    job_is     = property(get_job_id, set_job_id)
    fixed      = property(is_fixed, set_fixed)
    assigned_machine = property(get_assigned_machine, set_assigned_machine)

