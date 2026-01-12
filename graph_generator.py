import random
import networkx as nx

def generate_sparse_graph(n:int, edges_per_node=3, max_weight=10):
    G = nx.DiGraph()
    G.add_nodes_from(range(n))

    for u in range(n):
        for _ in range(edges_per_node):
            v = random.randint(0, n - 1)
            if u != v:
                G.add_edge(u, v, weight=random.randint(1, max_weight))
    return G

def generate_dense_graph(n:int, density=0.3, max_weight=10):
    G = nx.DiGraph()
    G.add_nodes_from(range(n))

    for u in range(n):
        for v in range(n):
            if u != v and random.random() < density:
                G.add_edge(u, v, weight=random.randint(1, max_weight))
    return G

def nx_to_adjlist(G):
    adj = {u: [] for u in G.nodes()}
    for u, v, data in G.edges(data=True):
        adj[u].append((v, data["weight"]))
    return adj