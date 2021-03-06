# -*- coding: utf-8 -*- 
'''Schedule
Clase responsable de generar el calendario
José González - A01036121
ITESM Campus Monterrey
29/03/2017
'''
import matplotlib.pyplot  as plt
import matplotlib.patches as patches
import matplotlib.ticker  as plticker
# import simulated_annealing as sa
import numpy as np


class Plotter:
    def __init__(self):
        """Método de inicialización"""
        pass
    
    def print_solution(self, g):
        """Método para imprimir los resultados en forma de texto."""
        for op, lst in g.items():
            print("operacion:", op)
            print("empieza en:", g.get(op)[0].get_start_time())
            print("termina en:", g.get(op)[0].get_end_time())
    
    def plot_solution(self, fig, graph, no_machines, machines, operations, ms, no_jobs):
        """Método draw que dibuja en pantalla la gráfica representando la secuencia de ejecución de las operaciones en cada máquina"""
        max_value = 16581375
        interval = int(max_value / no_jobs)
        colors = [hex(I)[2:].zfill(6) for I in range(0, max_value, interval)]
        
        shortener = 1.0
        separation = 1.0
        formatter = ""
        if int(float(ms)) > 1000:
            shortener = 100.0
            separation = 10.0 if int(float(ms)) > 2500 else 5.0
            formatter = "00"
        elif int(float(ms)) > 100:
            shortener = 10.0
            separation = 1.0
            formatter = "0"
        
        # recorremos el grafo disyuntivo obteniendo tiempos de inicio, duración y finalización para mostrar las
        # operaciones como rectángulos
        # los tiempos se guardan como coordenadas en los patches de Matplotlib para después graficar las figuras
        # también llena una lista de colores para graficar del mismo color las operaciones de la misma tarea
        patch_list = []
        job_colors = [None] * no_jobs
        for k, v in graph.items():
            y = v[0].get_machine_id()
            x = v[0].get_start_time() / shortener
            coordinates = (x, y)
            color = colors[v[0].get_job_id()]
            job_colors[v[0].get_job_id()] = color
            patch_list.append(patches.Rectangle(
                coordinates, v[0].get_duration() / shortener, 1, facecolor='#' + str(color)))
        
        # creamos las etiquetas que se colocarán en la esquina superior derecha indicando el color de cada tarea
        color_patches = []
        labels = []
        for i, j_color in enumerate(job_colors):
            labels.append('Tarea ' + str(i))
            color_patch = patches.Patch(color="#" + str(j_color))
            color_patches.append(color_patch)
        
        # creamos el espacio de la gráfica como figura y establecemos características
        fs = 10 if no_jobs > 20 else 15
        plt.clf()
        fig.legend(labels=labels, fontsize=fs, handles=color_patches)
        ax = fig.add_subplot(111, aspect='equal', xlabel='Tiempo')
        ax.set_xlim(xmin=0, xmax=int(float(ms) / shortener) + 1)
        ax.set_ylim(ymin=0, ymax=int(float(no_machines + 1)))
        
        loc = plticker.MultipleLocator(base=separation)
        majorFormatter = plticker.FormatStrFormatter('%d' + formatter)
        minorLocator = plticker.MultipleLocator(5)
        ax.xaxis.set_major_locator(loc)
        ax.xaxis.set_major_formatter(majorFormatter)
        ax.xaxis.set_minor_locator(minorLocator)
        ax.get_yaxis().set_visible(False)
        
        # desplegamos el Makespan como parte del plot
        ax.annotate("Makespan: " + str(int(float(ms))), xy=(0.5, 0.95), xycoords=('axes fraction', 'figure fraction'),
                    xytext=(-0.1, 0.2), textcoords='offset points', size=18, ha='center', va='top')
        
        # generamos las anotaciones correspondientes a los identificadores de las máquinas y las posicionamos
        m_indexes = list(reversed(list(range(1, no_machines + 1))))
        for i in range(no_machines * 2):
            if i % 2 != 0:
                ax.annotate('M ' + str(m_indexes.pop()), xy=(0, i / 2),
                            xytext=(-1 * int(float(ms)) / (10 * shortener), i / 2 + 0.9), size=15)
        
        # se agregan los patches rectángulos a la figura
        for p in patch_list:
            ax.add_patch(p)
        
        # mostramos la gráfica con la figura y los patches
        plt.show()
        return graph
    
    def generate_solution_file(self, graph):
        """genera el archivo de salida con la solución en el formato
        especificado en http://optimizizer.com/TA.php para subirlo en la misma página. 
        El formato es: cada renglón representa una máquina y cada elemento del renglón
        representa la tarea a la que pertenece la operación en esa posición.
        El diccionario que se recibe como parámetro es tal que las llaves son los id
        de las máquinas mientras que los valores son listas con las operaciones en el oden
        que se ejecutarán."""
        
        solution_matrix = np.array([[op.get_job_id() for op in lst] for _, lst in graph.items()])
        np.savetxt('test.out', solution_matrix.astype(int), fmt='%i', delimiter=' ')
