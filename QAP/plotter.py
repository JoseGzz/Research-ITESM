import networkx as nx
import matplotlib.pyplot as plt

class Plotter:
	def __init__(self, locations=[], facilities=[]):
		self.locations = locations
		self.facilities = facilities


	def plot_results(self):
		max_value = 16581375 
        interval  = int(max_value / len(self.locations))
		colors    = [hex(I)[2:].zfill(6) for I in range(0, max_value, interval)]
		G = nx.Graph()
		G.add_edges_from(
		    [('1', '2'), ('1', '3'), ('4', '2'), ('5', '3'), ('5', '6'),
		     ('2', '8'), ('2', '7'), ('2', '6'), ('3', '7')])

		val_map = {'A': 1.0,
		           'D': 0.5714285714285714,
		           'H': 0.0}

		values = [val_map.get(node, 0.25) for node in G.nodes()]
		plt.show()
		nx.draw(G, cmap=plt.get_cmap('jet'), with_labels=True, node_color=values)
		





