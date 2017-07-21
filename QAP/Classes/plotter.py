# -*- coding: utf-8 -*- 
"""
Grafica resultados del problema QAP.
José González Ayerdi
ITESM Campus Monterrey
03/2017  
"""
import networkx as nx
import matplotlib.pyplot as plt


class Plotter:
    def __init__(self, locations=[], facilities=[], permutation=[], cost=0):
        """Inicialización de objeto."""
        self.locations = locations
        self.facilities = facilities
        self.permutation = permutation
        self.cost = cost
    
    def plot_results(self, fig):
        """plot_results grafica nodos numerados con etiquetas numeradas representando las ubicaciones
        y las facilities respectivamente"""
        
        fig.clf()
        # generamos una lista de tuplas que representan las conexiones entre la ubicación a y b
        # (+1 para presentar resultados desde índice 1).
        adjacency_list = [(str(a.loc_id + 1), str(b + 1)) for a in self.locations for b in a.get_adyacents_ids()]
        G = nx.Graph()
        G.add_edges_from(adjacency_list)
        
        # para cada conexión cualculamos la distancia y el flujo entre ellos
        # y agregamos esos valores al diccionario de conexiones de nodos.
        for con in adjacency_list:
            dist = self.locations[(int(con[0]) - 1)].distance_to(int(con[1]) - 1)
            flow = self.locations[(int(con[0]) - 1)].facility.flow_with(
                self.locations[(int(con[1]) - 1)].facility.fac_id)
            G[con[0]][con[1]]["dist / flujo"] = str(dist) + " / " + str(flow)
        
        # generamos las etiquetas de asignación de facilities
        pos = nx.spring_layout(G)
        for i, p in enumerate(self.permutation):
            x, y = pos[str(i + 1)]
            plt.text(x, y + 0.08, s="fac " + str(p + 1), bbox=dict(facecolor='red', alpha=0.5), size=15,
                     horizontalalignment='center')
        
        # establecemos las características del espacio de graficación.
        axes = plt.gca()
        axes.set_xlim([-0.1, 1.2])
        axes.set_ylim([-0.2, 1.2])
        plt.sca(axes)
        
        # agregamos una etiqueta a la gráfica para mostrar el costo total encontrado.
        plt.text((-0.1 + 1.2) / 2, -0.1, s="Costo total " + str(self.cost), bbox=dict(facecolor='white', alpha=0.5),
                 size=20, verticalalignment='center',
                 horizontalalignment='center')
        
        # se grafican los resultados
        nx.draw(G, pos, cmap=plt.get_cmap('jet'), with_labels=True)
        nx.draw_networkx_edge_labels(G, pos)
        plt.show()
