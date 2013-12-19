import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

## Control Graphs, Edit for better graphs as you need
LABEL_FLAG = True  # Whether shows labels.NOTE: configure your matplotlibrc for Chinese characters.
REMOVE_ISOLATED = True  # Whether remove isolated nodes(less than iso_level connects)
DIFFERENT_SIZE = True  # Nodes for different size, bigger means more shared friends
ISO_LEVEL = 10
NODE_SIZE = 40  # Default node size


class DrawPic():
    
    def __init__(self, filename):
        self.dict = defaultdict(list)
        self.filename = filename
        self.generate_dict()
    
    
    def generate_dict(self):
        email = open(self.filename)
        for line in email:
            fromNode, toNode = line.split()
            self.dict[int(fromNode)].append(int(toNode))
        email.close()
    
    
    def get_toNodes(self, fromNode_id):
        return self.dict[fromNode_id]
        
    
    def getrelations(self, id1, id2):
        """receive two user id, If they are friends, return 1, otherwise 0."""
        toNodes_id1 = self.get_toNodes(id1)
        toNodes_id2 = self.get_toNodes(id2)
        if (id2 in toNodes_id1) or (id1 in toNodes_id2):
            return 1
        else:
            return 0
    
    
    def getgraph(self, nodeids):
        'Get the Graph Object and return it.'
        
        G = nx.Graph()  # Create a Graph object
        
        for nodeid in nodeids:
            dict_root = self.get_toNodes(nodeid)  # Get root tree
            if nodeid not in dict_root:
                dict_root.append(nodeid)
            for toNodeid1 in dict_root:
                G.add_node(toNodeid1)
                for toNodeid2 in dict_root:
                    if toNodeid2 == toNodeid1:
                        continue
                    if self.getrelations(toNodeid1, toNodeid2):
                        G.add_edge(toNodeid1, toNodeid2)
    
        return G
    
    
    def draw_graph(self, nodeids, filename='graph.p', label_flag=True, remove_isolated=True, different_size=True, iso_level=10, node_size=40):
        """Reading data from file and draw the graph.If not exists, create the file and re-scratch data from net"""
        
        print("Generating graph...")
        '''
        try:
            with open(filename, 'rb') as f:
                G = p.load(f)
        except:
            G = self.getgraph(nodeid)
            with open(filename, 'wb') as f:
                p.dump(G, f)
        '''
        G = self.getgraph(nodeids)
        
        #nx.draw(G)
        # Judge whether remove the isolated point from graph
        if remove_isolated is True:
            H = nx.empty_graph()
            for SG in nx.connected_component_subgraphs(G):
                if SG.number_of_nodes() > iso_level:
                    H = nx.union(SG, H)
            G = H
        # Ajust graph for better presentation
        if different_size is True:
            L = nx.degree(G)
            G.dot_size = {}
            for k, v in L.items():
                G.dot_size[k] = v
            node_size = [G.dot_size[v] for v in G]
        pos = nx.spring_layout(G, iterations=50)
        nx.draw_networkx_edges(G, pos, alpha=0.2)
        nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color='r', alpha=0.3)
        # Judge whether shows label
        if label_flag is True:
            nx.draw_networkx_labels(G, pos, font_size=6, alpha=0.5)
        #nx.draw_graphviz(G)
        plt.show()
    
        return G
    
if __name__ == '__main__':
    recv_most = [179170,422,30,72,298,485,83,366,70524,994]
    send_most = [83,868,192,2371,10,1417,104,818,240,147]
    nodes = set(recv_most + send_most)
    
    drawpic = DrawPic('cleaned_email.txt')
    G = drawpic.draw_graph(nodes, filename='graph.p', label_flag=LABEL_FLAG, remove_isolated=REMOVE_ISOLATED, different_size=DIFFERENT_SIZE, iso_level=ISO_LEVEL, node_size=NODE_SIZE)