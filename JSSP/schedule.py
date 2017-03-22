# -*- coding: utf-8 -*- 
'''Schedule
Clase con la información correspondiente al calendario
'''
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import copy as cp

class Schedule:
    machines_operations = {}
    def __init__(self):
        pass

    def fit(self, graph, no_machines, machines, operations, ms, no_jobs):
        #machines_location = list(range(no_machines))
        #print(machines_location)	

        '''
		machines_lst = [None]*no_machines

        # agrupación por máquina
        for i, m in enumerate(machines):
            machines_tmp = []
            for op in operations:
                if op.get_machine_id() == m.get_id():
                    machines_tmp.append(op)
            machines_lst[i] = machines_tmp
	
		
        '''
        # pr = [patches.rectangle,...]
        max_value = 16581375 #255**3
        interval = int(max_value / no_jobs)
        colors = [hex(I)[2:].zfill(6) for I in range(0, max_value, interval)]

        patch_list = []
        for k, v in graph.items():
            y = v[0].get_machine_id()
            x = v[0].get_start_time()
            coordinates = (x,y)
            color = colors[v[0].get_job_id()]
            patch_list.append(patches.Rectangle(coordinates, v[0].get_duration(), 1, facecolor='#'+str(color)))

        fig = plt.figure()
        ax = fig.add_subplot(111, aspect='equal', label='?')
        ax.set_xlim(xmin=0,xmax=int(float(ms))+5)
        ax.set_ylim(ymin=0,ymax=int(float(no_machines+3)))
        for p in patch_list:
            ax.add_patch(p)        
        plt.show()









