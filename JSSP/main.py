
# -*- coding: utf-8 -*- 
'''
    José González Ayerdi
    ITESM Campus Monterrey
    23/02/2017

    Sistema de clases para el problema JSSP
'''

from machine   import Machine
from job       import Job   
from schedule  import Schedule
from operation import Operation
from formatter import Formatter
from disjunctive_graph import DisjunctiveGraph
import sys
import numpy as np

'''Función main para comenzar a ejecutar el programa '''
def main():

    times    = 'datos/times_sample_mat.txt' 
    machines = 'datos/machines_sample_mat.txt'
    # verifica que los archivos existan
    # IMPORTANTE: se asume que todas las tareas tienen la misma cantidad de operaciones
    try:
        times_mat, machines_mat = np.genfromtxt(times), np.genfromtxt(machines, dtype=None)
    except IOError as e:
        print("No se encontró uno de los archivos.")
        print(e)
        sys.exit(0)

    # Estableecmos cantidades necesarias
    no_jobs     = len(times_mat[:])
    no_machines = len(times_mat[0])

    # Se crea la lista de objetos
    f = Formatter()
    ops, jobs, machines = f.create_objects(no_machines, no_jobs, times_mat, machines_mat)
    '''
    # Se imprimen casos de prueba
    print '----Operaciones----'
    print 'operacion 17 (empieza Índice en 0)'
    print 'id: {} (operación_tarea)'.format(ops[17].get_id())
    print 'Le pertenece a la tarea: {}.'.format(ops[17].get_job_id())
    print 'Dura {} unidades de tiempo.'.format(ops[17].get_duration())
    print 'Se ejecutará en la máquina: {}.'.format(ops[17].get_machine_id())
    print

    ops_1j = jobs[1].get_operations()
    print '----Tareas----'
    print 'tarea 1 (empieza Índice en 0)'
    print 'Contiene las operaciones (operación_tarea):'
    for op in ops_1j:
        print op.get_id(),
    else:
        print
    print

    ops_2m = machines[2].get_operations()
    print '----Máquinas----'
    print 'máquina 3 (empieza índice en 1)'
    print 'Ejecutará las operaciones (operación_tarea): '
    for op in ops_2m:
        print op.get_id(),
    else:
        print 

    

    #for op in ops:
    #    print op.id
    '''
    dg = DisjunctiveGraph()
    g = dg.find_makespan(jobs, ops, machines, no_machines)
    # print g
    
if __name__ == "__main__":
    main()

'''
TODO:

ops, precedence, groups = generate_matrixes(ops, jobs, machines)

g = DisjunctiveGraph(ops, precedence, groups)

schedule = solver(g)

schedule.print_result()
'''
