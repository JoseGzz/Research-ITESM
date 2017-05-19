
# -*- coding: utf-8 -*- 
"""
Sistema de clases para el problema JSSP
José González Ayerdi - A01036121
ITESM Campus Monterrey
02/2017  
"""
from machine   import Machine
from job       import Job   
from schedule  import Schedule
from operation import Operation
from formatter import Formatter
from disjunctive_graph import DisjunctiveGraph
import sys
import numpy as np

""" Función main para comenzar a ejecutar el programa """
def main():
    """Archivos con pocos datos de prueba"""
    #instance = 'datos/toy/3x3_demo.txt'
    #instance = 'datos/toy/4x4_demo.txt'
    #instance = 'datos/toy/5x5_demo.txt' 
    """Archivos con datos benchmark (tareas x maquinas)"""
    instance = 'datos/benckmark/15x15/Ta01.txt'
    #instance = 'datos/benckmark/20x15/Ta11.txt'
    #instance = 'datos/benckmark/20x20/Ta21.txt'
    #instance = 'datos/benckmark/30x15/Ta31.txt'
    #instance = 'datos/benckmark/30x20/Ta41.txt'
    #instance = 'datos/benckmark/50x15/Ta51.txt'
    #instance = 'datos/benckmark/50x20/Ta61.txt'
    #instance = 'datos/benckmark/100x20/Ta71.txt'
    #instance = 'datos/toy/4x4.txt'
    """IMPORTANTE: se asume que todas las tareas tienen la misma cantidad de operaciones"""
    # leemos los datos 
    with open(instance, 'r') as f:
        no_jobs = int(f.readline())
        mat = np.loadtxt(f, dtype=None)

    # asignamos los valores a las matrices correspondientes
    times_mat = mat[:no_jobs]
    machines_mat = mat[no_jobs:]

    # Establecemos cantidades necesarias
    no_jobs     = len(times_mat[:])
    no_machines = len(times_mat[0])


    # Se crea la lista de objetos
    f = Formatter()
    ops, jobs, machines = f.create_objects(no_machines, no_jobs, times_mat, machines_mat)

    # Se calcula el makespan solamente con el recorrido hacia adelante
    dg = DisjunctiveGraph()
    schedule = Schedule()
    g, ms, jg, mg, ops = dg.find_makespan(jobs, ops, machines, no_machines)

    #for i in range(10):
    #for i in range(40):
    #     g, ms, jg, mg, ops = dg.perturbate_solution(jg, mg, ops)
    schedule.plot_result(g, no_machines, machines, ops, ms, no_jobs)
    #schedule.print_result(g)
    
if __name__ == "__main__":
    main()


