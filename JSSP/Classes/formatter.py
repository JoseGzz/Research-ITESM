# -*- coding: utf-8 -*- 
"""Formatter
Clase que transforma matrices de tiempos y máquinas
a listas con máquinas, tareas y operaciones.
José González Ayerdi
ITESM Campus Monterrey
02/2017
"""
from machine   import Machine
from job       import Job   
from solution  import Solution
from operation import Operation

class Formatter:
    """constructor para la clase formatter"""
    def __init__(self):
        pass
    
    def create_objects(self, no_machines, no_jobs, times_matrix, machines_matrix):
        """genera y regresa las listas de maquinas, tareas y operaciones"""
        operations = self.create_operation_list(times_matrix, machines_matrix)
        jobs       = self.create_job_list(times_matrix, operations)
        machines   = self.create_machine_list(no_machines, machines_matrix, operations)
        operations = self.assign_jobs_to_operations(jobs, operations)
        return operations, jobs, machines
    
    def assign_jobs_to_operations(self, jobs, operations):
        """le decimos a cada operación a qué tarea pertenece"""
        count = 0
        for job in jobs:
            for i in range(job.get_op_count()):
                operations[count].set_job(job)
                count += 1
        return operations

    def create_machine_list(self, no_machines, machines_matrix, operations):
        """para crear la lista de máquinas se agregan los id y se les asignan
        sus correspondientes operaciones"""
        machines = []
        machines = self.add_machine_ids(no_machines)
        machines = self.add_operations_to_machines(machines, machines_matrix, operations)
        return machines
    
    def add_machine_ids(self, no_machines):
        """asigna id's a las máquinas (comenzando en 1)"""
        machines = [Machine() for i in range(0, no_machines)]
        machines_aux = []
        for i, machine in enumerate(machines):
            machine.set_id(i+1)
            machines_aux.append(machine)
        return machines_aux

    def add_operations_to_machines(self, machines, machines_matrix, operations):
        """se agregan las operaciones correspondientes a cada máquina"""
        for i, machine in enumerate(machines):
            ops = [op for op in operations if op.get_machine_id() == machine.get_id()]
            machines[i].set_operations(ops)
        return machines
       
    def create_job_list(self, times_matrix, operations):
        """para crear la lista de tareas primero se asignan ids a las tareas
        y luego sus operaciones""" 
        jobs = []
        jobs = self.add_job_ids(times_matrix, jobs)
        jobs = self.add_operations_to_jobs(operations, jobs)
        return jobs
    
    def add_job_ids(self, times_matrix, jobs):
        """crea tareas y se les asignan ids"""
        id = 0
        for job in times_matrix:
           j = Job()
           j.set_id(id)
           jobs.append(j)
           id += 1
        return jobs

    def add_operations_to_jobs(self, operations, jobs):
        """se asignan las operaciones a sus tareas correspondientes"""
        index = 0
        for job in jobs:
            ops = [op for op in operations if op.get_job_id() == job.get_id()]
            jobs[index].set_operations(ops)
            index += 1
        return jobs
    
    def create_operation_list(self, times_matrix, machines_matrix):
        """para crear la lista de operaciones se les asigna un id, una duración y 
        se asocian con la máquina donde serán procesadas"""
        operations = []
        operations = self.add_operation_ids(times_matrix, operations)
        operations = self.add_times_to_operations(times_matrix, operations)
        operations = self.add_machines_to_operations(machines_matrix, operations)
        return operations
    
    def add_machines_to_operations(self, machines_matrix, operations):
        """se asocian las operaciones con sus correspondientes máquinas"""
        index = 0
        for job in machines_matrix:
            for machine_id in job:
                operations[index].set_machine_id(machine_id)
                index += 1
        return operations
    
    def add_operation_ids(self, times_matrix, operations):
        """crea las operacoines y les asigna un id que consiste de el id propio
        dentro de la operación y el id de la tarea"""
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
    
    def add_times_to_operations(self, times_matrix, operations):
        """agrega los tiempos de duración a las operaciones"""
        index = 0
        for job in times_matrix:
            for time in job:
                operations[index].set_duration(time)
                index += 1
        return operations

