
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

    times    = 'datos/times_sample_mat.txt' 
    machines = 'datos/machines_sample_mat.txt'
    #times    = 'datos/times_sample_mat2.txt' 
    #machines = 'datos/machines_sample_mat2.txt'
    #times    = 'datos/times_sample_mat3.txt' 
    #machines = 'datos/machines_sample_mat3.txt'
    #times    = "datos/times_mat4.txt"
    #machines = "datos/machines_mat4.txt"
    # archivos con datos benchmark.
    # para estos archivos el programa no encuentra un grafo sin ciclos
    #times    = 'datos/times_mat.txt' 
    #machines = 'datos/machines_mat.txt'
    #times    = "datos/times_mat5.txt"
    #machines = "datos/machines_mat5.txt"
    # verifica que los archivos existan
    """IMPORTANTE: se asume que todas las tareas tienen la misma cantidad de operaciones"""
    try:
        times_mat, machines_mat = np.genfromtxt(times), np.genfromtxt(machines, dtype=None)
    except IOError as e:
        print("No se encontró alguno de los archivos.")
        print(e)
        sys.exit(0)

    # Establecemos cantidades necesarias
    no_jobs     = len(times_mat[:])
    no_machines = len(times_mat[0])

    # Se crea la lista de objetos
    f = Formatter()
    ops, jobs, machines = f.create_objects(no_machines, no_jobs, times_mat, machines_mat)

    # Se calcula el makespan solamente con el recorrido hacia adelante
    dg = DisjunctiveGraph()
    g, ms, jg, mg = dg.find_makespan(jobs, ops, machines, no_machines)
    dg.perturbate_solution(jg, mg)

    schedule = Schedule()
    schedule.plot_result(g, no_machines, machines, ops, ms, no_jobs)
    schedule.print_result(g)

if __name__ == "__main__":
    main()


