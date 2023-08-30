#!/usr/bin/env python
# coding: utf-8

# In[204]:


class GraphNode:
  def __init__(self, type, hash, params, id, children=None):
    self.type = type
    self.hash = hash
    self.params = params
    self.id = id
    self.children = children

  def __str__(self):
    return self.type + "\n"+self.hash




# In[176]:


import json
with open('jsonTest.json', 'r') as json_file:
    loaded_data = json.load(json_file)


# In[222]:


import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout  # Import the graphviz_layout function



def convert_layout_to_graph(layout):
    def traverse_layout(node, graph, parent_node=None):
        treeNode = GraphNode(type=node.get("type"), hash=node.get("hash"), params= node.get("params"), id=node.get("id"), children=node.get("children"))

        # Add the node to the graph
        graph.add_node(treeNode)

        # Connect the node to its parent, if it exists
        if parent_node is not None:
            graph.add_edge(parent_node, treeNode)

        # Process children recursively
        if treeNode.children:
            for child in treeNode.children:
                traverse_layout(child, graph, parent_node=treeNode)

    # Create an empty directed graph
    graph = nx.DiGraph()

    # Traverse the layout JSON and build the graph
    traverse_layout(layout['schema'], graph)

    return graph





def visualize_graph(graph, blockName):
    nodes_list = list(graph.nodes())
    first_node = nodes_list[0] if nodes_list else None
    
    # Create a hierarchical layout using graphviz_layout
    
    def hierarchy_pos(G, root, levels=None, width=1.0, height=2.):
        
        TOTAL = "total"
        CURRENT = "current"
        def make_levels(levels, node=root, currentLevel=0, parent=None):
            """Compute the number of nodes for each level
            """
            if not currentLevel in levels:
                levels[currentLevel] = {TOTAL : 0, CURRENT : 0}
            levels[currentLevel][TOTAL] += 1
            neighbors = list(G.neighbors(node))
            for neighbor in neighbors:
                if not neighbor == parent:
                    levels =  make_levels(levels, neighbor, currentLevel + 1, node)
            return levels
    
        def make_pos(pos, node=root, currentLevel=0, parent=None, vert_loc=0):
            dx = 1/levels[currentLevel][TOTAL]
            left = dx/2
            pos[node] = ((left + dx*levels[currentLevel][CURRENT])*width, vert_loc)
            levels[currentLevel][CURRENT] += 1
            neighbors = list(G.neighbors(node))
            for neighbor in neighbors:
                if not neighbor == parent:
                    pos = make_pos(pos, neighbor, currentLevel + 1, node, vert_loc-vert_gap)
            return pos
        if levels is None:
            levels = make_levels({})
        else:
            levels = {l:{TOTAL: levels[l], CURRENT:0} for l in levels}
        vert_gap = height / (max([l for l in levels])+1)
        return make_pos({})
    
    
    # Create a hierarchical layout for the graph
    pos = hierarchy_pos(graph, root=first_node)
    
    
    # Visualize the graph using the hierarchical layout
    plt.figure(figsize=(200, 50))
    nx.draw(graph, pos, with_labels=True, node_size=5000,  font_size=26)
    #plt.title(blockName)
    plt.title("Hierarchical Graph Visualization")
    plt.show()
    
#graph = convert_layout_to_graph(loaded_data)
#visualize_graph(graph)

