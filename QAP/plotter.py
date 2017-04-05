import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
import matplotlib.colors as colors

class Plotter:
	def __init__(self, locations=[], facilities=[], permutation=[], cost=0):
		self.locations = locations
		self.facilities = facilities
		self.permutation = permutation
		self.cost = cost

	def plot_results(self):
		max_value = 16581375 
		interval  = int(max_value / len(self.locations))
		node_colors    = [hex(I)[2:].zfill(6) for I in range(0, max_value, interval)]

		adjacency_list = [(str(a.loc_id+1), str(b+1)) for a in self.locations for b in a.get_adyacents_ids()]
		node_colors.pop()

		G = nx.Graph()
		G.add_edges_from(adjacency_list)

		val_map = {str(i+1): int(val, 16) for i, val in enumerate(node_colors)}

		values = [val_map.get(node, 0.25) for node in G.nodes()]
		
		for con in adjacency_list:
			dist = self.locations[(int(con[0])-1)].distance_to(int(con[1])-1)
			flow = self.locations[(int(con[0])-1)].facility.flow_with(self.locations[(int(con[1])-1)].facility.fac_id)
			G[con[0]][con[1]]["dist / flujo"] = str(dist) + " / " + str(flow)

		plt.show()

		pos = nx.spring_layout(G)
		for i, p in enumerate(self.permutation):
			x, y = pos[str(i+1)]
			plt.text(x,y+0.08,s="fac "+str(p+1), bbox=dict(facecolor='red', alpha=0.5), size = 15, horizontalalignment='center')

		axes = plt.gca()
		axes.set_xlim([-0.1,1.2])
		axes.set_ylim([-0.2,1.2])
		plt.sca(axes)

		plt.text((-0.1 + 1.2)/2, -0.1 , s="Costo total "+str(self.cost), bbox=dict(facecolor='white', alpha=0.5), size=20, verticalalignment = 'center',
		 horizontalalignment='center')

		nx.draw(G, pos, cmap=plt.get_cmap('jet'), with_labels=True)
		nx.draw_networkx_edge_labels(G,pos)
		
		





