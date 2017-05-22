
# -*- coding: utf-8 -*- 
"""
Sistema de clases para el problema JSSP
José González Ayerdi
ITESM Campus Monterrey
02/2017  
"""
from machine   import Machine
from job       import Job   
from solution  import Solution
from operation import Operation
from formatter import Formatter
from plotter   import Plotter
import sys
import numpy as np

class JSSP():
    def __init__(self):
        """ Función para inicializar propiedades del problema"""
        self.solution = Solution()
        self.formatter = Formatter()
        self.operations = []
        self.jobs = []
        self.machines = []
        self.no_machines = 0
        self.no_jobs = 0

    def read_data(self, filename=""):
        """Funcion para leer datos del archivo de entrada."""
        """IMPORTANTE: se asume que todas las tareas tienen la misma cantidad de operaciones"""
        # leemos los datos 
        with open(filename, 'r') as f:
            no_jobs = int(f.readline())
            mat = np.loadtxt(f, dtype=None)
        # asignamos los valores a las matrices correspondientes
        times_mat = mat[:no_jobs]
        machines_mat = mat[no_jobs:]
        self.format_data(times_mat, machines_mat)

    def format_data(self, times_mat, machines_mat):
        """Funcion para generar representacion interna de objetos"""
        # Establecemos cantidades necesarias
        no_jobs = len(times_mat[:])
        no_machines = len(times_mat[0])
        self.no_machines = no_machines
        self.no_jobs = no_jobs
        # Se crean las listas de objetos
        self.operations, self.jobs, self.machines = self.formatter.create_objects(no_machines, no_jobs, times_mat, machines_mat)

    def random_solution(self):
        # Se calcula un makespan inicial solamente con el recorrido hacia adelante
        self.solution.find_makespan(self.jobs, self.operations, self.machines, self.no_machines)
        return self.solution
        #self.g, self.ms, self.jg, self.mg, self.operations = self.solution.find_makespan(self.jobs, self.operations, self.machines, self.no_machines)

    def create_neighbor(self):
        self.g, self.ms, self.jg, self.mg, self.operations = self.solution.perturbate_solution(self.jg, self.mg, self.operations)

    """
    def random_solution(problem):
        problem.random_solution_helper()
       # problem.random_solution_helper(self.jobs, self.operations, self.machines, self.no_machines)
    """

    """Archivos con pocos datos de prueba"""
    #self.instance = '../Instances/toy/3x3_demo.txt'
    #self.instance = '../Instances/toy/4x4_demo.txt'
    #self.instance = '../Instances/toy/5x5_demo.txt' 
    """Archivos con datos benchmark (tareas x maquinas)"""
    #self.instance = '../Instances/taillard instances/15x15/Ta01.txt'
    #self.instance = '../Instances/taillard instances/20x15/Ta11.txt'
    #self.instance = '../Instances/taillard instances/20x20/Ta21.txt'
    #self.instance = '../Instances/taillard instances/30x15/Ta31.txt'
    #self.instance = '../Instances/taillard instances/30x20/Ta41.txt'
    #self.instance = '../Instances/taillard instances/50x15/Ta51.txt'
    #self.instance = '../Instances/taillard instances/50x20/Ta61.txt'
    #self.instance = '../Instances/taillard instances/100x20/Ta71.txt'