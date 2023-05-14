from models.Graph import Graph
import time
import sys

class UnionFind:
    def __init__(self, nodes):
        self.parent = {node: node for node in nodes}
        self.rank = {node: 0 for node in nodes}

    def find(self, node):
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self, node1, node2):
        root1 = self.find(node1)
        root2 = self.find(node2)

        if root1 != root2:
            if self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            elif self.rank[root1] < self.rank[root2]:
                self.parent[root1] = root2
            else:
                self.parent[root2] = root1
                self.rank[root1] += 1

def kruskal(grafo: Graph):
    # Sort the edges in ascending order based on distance
    sorted_edges = sorted(grafo.edge_list, key=lambda edge: edge.distance)

    # Create an instance of UnionFind
    uf = UnionFind(grafo.get_nodes())

    mst = []  # Minimum Spanning Tree

    for edge in sorted_edges:
        if uf.find(edge.start_node) != uf.find(edge.end_node):
            mst.append(edge)
            uf.union(edge.start_node, edge.end_node)

    return mst

def prim(grafo: Graph):
    mst = []  # Create a list to store the MST edges
    if not grafo.adj_list:  # Check if the graph is empty
        return mst

    start_node = next(iter(grafo.adj_list.keys()))  # Select any starting node
    visited = {start_node}  # Set of visited nodes
    num_nodes = len(grafo.adj_list)

    while len(visited) < num_nodes:
        min_edge = None
        min_distance = sys.maxsize

        for edge in grafo.edge_list:
            if (edge.start_node in visited and edge.end_node not in visited) or \
                    (edge.start_node not in visited and edge.end_node in visited):
                # Consider edges where one node is visited and the other is not
                if edge.distance < min_distance:
                    min_distance = edge.distance
                    min_edge = edge

        if min_edge:
            mst.append(min_edge)  # Add the edge to the MST
            visited.add(min_edge.start_node)
            visited.add(min_edge.end_node)

    return mst