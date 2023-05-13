from models.Graph import Graph, Edge
import pathlib
import re
from models.Note import Note
import random
import json

def criar_grafo(path, node_color):
    # Cria um grafo vazio
    grafo = Graph()

    with open(path, 'r') as json_file:
        data = json.load(json_file)

    nodes={}
    for node_data in data['nodes']:
        nodes[node_data['filename']]= Note(node_data['x'], node_data['y'], node_data['filename'], color=node_color)

    for node in nodes.values():
        grafo.add_node(node)
    
    edges=[]
    for edge_data in data['edges']:
        edges.append(Edge(nodes[edge_data['start_node']], nodes[edge_data['end_node']], edge_data['distance']))

    for aresta in edges:
        grafo.add_edge(aresta)

    return grafo

from models.MST import prim

if __name__ == '__main__':
    grafo = criar_grafo('graphs_examples/example1.json')

    print(prim(grafo))