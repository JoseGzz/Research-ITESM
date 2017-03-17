# -*- coding: utf-8 -*- 
"""Formatter
Clase que transforma matrices de tiempos y máquinas
a listas con máquinas, tareas y operaciones.
José González Ayerdi - A01036121
ITESM Campus Monterrey
02/2017
"""
from machine   import Machine
from job       import Job   
from schedule  import Schedule
from operation import Operation

class Formatter:
    """Constructor para la clase formatter."""
    def __init__(self):
        pass
    
    """Método que recibe las matrices de tiempos y máquinas y regresa las 3 listas."""
    def create_objects(self, no_machines, no_jobs, times_matrix, machines_matrix):
        operations = self.create_operation_list(times_matrix, machines_matrix)
        jobs       = self.create_job_list(times_matrix, operations)
        machines   = self.create_machine_list(no_machines, machines_matrix, operations)
        operations = self.assign_jobs_to_operations(jobs, operations)
        return operations, jobs, machines
    
    """Método assign_jobs_to_operations para que cada operación sepa a qué tarea pertenece."""
    def assign_jobs_to_operations(self, jobs, operations):
        count = 0
        for job in jobs:
            for i in range(job.get_op_count()):
                operations[count].set_job(job)
                count += 1
        return operations

    """Para crear la lista de máquinas se agregan los id y se les asignan
    sus correspondientes operaciones."""
    def create_machine_list(self, no_machines, machines_matrix, operations):
        machines = []
        machines = self.add_machine_ids(no_machines)
        machines = self.add_operations_to_machines(machines, machines_matrix, operations)
        return machines
    
    """Asigna id's a las máquinas (comenzando en 1)."""
    def add_machine_ids(self, no_machines):
        machines = [Machine() for i in range(0, no_machines)]
        machines_aux = []
        for i, machine in enumerate(machines):
            machine.set_id(i+1)
            machines_aux.append(machine)
        return machines_aux

    """Se agregan las operaciones correspondientes a cada máquina."""
    def add_operations_to_machines(self, machines, machines_matrix, operations):
        for i, machine in enumerate(machines):
            ops = [op for op in operations if op.get_machine_id() == machine.get_id()]
            machines[i].set_operations(ops)
        return machines
    
    """Para crear la lista de tareas primero se asignan ids a las tareas
    y luego sus operaciones."""    
    def create_job_list(self, times_matrix, operations):
        jobs = []
        jobs = self.add_job_ids(times_matrix, jobs)
        jobs = self.add_operations_to_jobs(operations, jobs)
        return jobs
    
    """Se crean tareas y se les asignan ids."""
    def add_job_ids(self, times_matrix, jobs):
        id = 0
        for job in times_matrix:
           j = Job()
           j.set_id(id)
           jobs.append(j)
           id += 1
        return jobs

    """Se asignan las operaciones a sus tareas correspondientes."""
    def add_operations_to_jobs(self, operations, jobs):
        index = 0
        for job in jobs:
            ops = [op for op in operations if op.get_job_id() == job.get_id()]
            jobs[index].set_operations(ops)
            index += 1
        return jobs
    
    """Para crear la lista de operaciones se les asigna un id, una duración y 
    se asocian con la máquina donde serán procesadas."""
    def create_operation_list(self, times_matrix, machines_matrix):
        operations = []
        operations = self.add_operation_ids(times_matrix, operations)
        operations = self.add_times_to_operations(times_matrix, operations)
        operations = self.add_machines_to_operations(machines_matrix, operations)
        return operations
    
    """Se asocian las operaciones con sus correspondientes máquinas."""
    def add_machines_to_operations(self, machines_matrix, operations):
        index = 0
        for job in machines_matrix:
            for machine_id in job:
                operations[index].set_machine_id(machine_id)
                index += 1
        return operations
    
    """Crea las operacoines y les asigna un id que consiste de el id propio
    dentro de la operación y el id de la tarea."""
    def add_operation_ids(self, times_matrix, operations):
        job_id = 0
        for job in times_matrix:
            own_id = 0
            for time in job:
                op = Operation()
                id_sub = str(own_id) + '_' + str(job_id)
                op.set_id(id_sub)
                op.set_job_id(job_id)
                own_id += 1
                operations.append(op)
            job_id += 1
        return operations
    
    """Agrega los tiempos de duración a las operaciones."""
    def add_times_to_operations(self, times_matrix, operations):
        index = 0
        for job in times_matrix:
            for time in job:
                operations[index].set_duration(time)
                index += 1
        return operations

