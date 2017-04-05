# -*- coding: utf-8 -*- 
'''Schedule
Clase cresponsable de generar el calendario
José González - A01036121
ITESM Campus Monterrey
29/03/2017
'''
import matplotlib.pyplot  as plt
import matplotlib.patches as patches
import matplotlib.ticker  as plticker

class Schedule:
    """Método de inicialización"""
    def __init__(self):
        pass

    """Método para imprimir los resultados en forma de texto."""
    def print_result(self, g):
        # desplegamos los tiempos de cada operación.
        for op, lst in g.items():
            print("operacion:", op)
            print("empieza en:", g.get(op)[0].get_start_time())
            print("termina en:", g.get(op)[0].get_end_time())


    """Método draw que dibuja en pantalla la gráfica representando la secuencia de ejecución de las operaciones en cada máquina"""
    def plot_result(self, graph, no_machines, machines, operations, ms, no_jobs):
        # generación de colores para las operaciones
        max_value = 16581375 
        interval  = int(max_value / no_jobs)
        colors    = [hex(I)[2:].zfill(6) for I in range(0, max_value, interval)]

        # recorremos el grafo disyuntivo obteniendo tiempos de inicio, duración y finalización para mostrar las operaciones como rectángulos
        # los tiempos se guardan como coordenadas en los patches de Matplotlib para después graficar las figuras
        # también llena una lista de colores para colorear del mismo color las operaciones de la misma tarea
        patch_list = []
        job_colors = [None]*no_jobs
        for k, v in graph.items():
            y = v[0].get_machine_id()
            x = v[0].get_start_time()
            coordinates = (x,y)
            color = colors[v[0].get_job_id()]
            job_colors[v[0].get_job_id()] = color
            patch_list.append(patches.Rectangle(coordinates, v[0].get_duration(), 1, facecolor='#'+str(color)))

        # creamos las etiquetas que se colocarán en la esquina superior derecha indicando el color de cada tarea
        color_patches = []
        labels = []
        for i, j_color in enumerate(job_colors):
            labels.append('Tarea ' + str(i))
            color_patch = patches.Patch(color="#"+str(j_color))
            color_patches.append(color_patch)

        # creamos el espacio de la gráfica como figura y establecemos características
        fig = plt.figure()
        fig.legend(labels=labels, handles=color_patches)
        ax = fig.add_subplot(111, aspect='equal', xlabel='Tiempo')
        ax.set_xlim(xmin=0,xmax=int(float(ms))+1)
        ax.set_ylim(ymin=0,ymax=int(float(no_machines+1)))
        loc = plticker.MultipleLocator(base=1.0)
        ax.xaxis.set_major_locator(loc)
        ax.get_yaxis().set_visible(False)

        # desplegamos el Makespan como parte del plot
        ax.annotate("Makespan: " + str(int(float(ms))), xy=(0.5, 0.2), xycoords=('axes fraction', 'figure fraction'),
        xytext=(0, 10), textcoords='offset points', size=18, ha='center', va='bottom')

        # generamos las anotaciones correspondientes a los identificadores de las máquinas y las posicionamos
        m_indexes = list(reversed(list(range(1, no_machines+1))))
        for i in range(no_machines*2):
            if i%2 != 0:
             ax.annotate('Maquina ' + str(m_indexes.pop()), xy=(0, i/2), xytext=(-1*int(float(ms))/10, i/2), size = 15)

        # se agregan los patches rectángulos a la figura
        for p in patch_list:
            ax.add_patch(p)        

         # mostramos la gráfica con la figura y los patches
        plt.show()









