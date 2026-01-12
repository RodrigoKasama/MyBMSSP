from algoritmos import Dijkstras, MyBMSSP
import graph_generator as graph_gen
import random
import time
import os
import csv

TRAD_DIJK = "Trad_Dijkstra"
FIBBO_DIJK = "Fibbo_Dijkstra"
BMSSP = "BMSSP"

# Falta registrar o tempo de cada caso e plottar os graficos de acordo

def experiment(matrix_adj, sources, algorithm):
    
    min_path = {}
    start_time = 0
    time_execution = 0
    
    if algorithm == TRAD_DIJK:
        start_time = time.perf_counter()
        min_path = Dijkstras.dijkstra_trad(matrix_adj, sources[0])
        time_execution = time.perf_counter() - start_time
        
    elif algorithm == FIBBO_DIJK:
        start_time = time.perf_counter()
        min_path = Dijkstras.dijkstra_fibbo(matrix_adj, sources[0])
        time_execution = time.perf_counter() - start_time

    elif algorithm == BMSSP:
        # Ajustando a estrutura de dados para o formato esperado pelo BMSSP
        matrix_adj = {k: {a: b for a, b in v} for k, v in matrix_adj.items()}

        BMSSP_solver = MyBMSSP.BMSSP(matrix_adj)

        # Valor arbitrário para o bound
        bound = 30

        start_time = time.perf_counter()
        min_path = BMSSP_solver.solve(sources, bound)
        time_execution = time.perf_counter() - start_time
        
        # Os vértices que não estão no resultado são inalcançáveis
        {min_path.update({vert: float("inf")}) for vert in matrix_adj.keys() if vert not in min_path.keys()}
    else:
        raise ValueError("Algoritmo desconhecido")
    
    return min_path, time_execution


def save_results(results, filename="results/experiments.csv"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    fieldnames = results.keys()

    write_header = not os.path.exists(filename)
    mode = "a"
    
    with open(filename, mode, newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if write_header:
            writer.writeheader()

        writer.writerows([results])

graph_sizes = [50, 100, 200, 500, 1000]

graph_types = ["sparse", "dense"]

alg_types = [TRAD_DIJK, FIBBO_DIJK, BMSSP]

overwrite_results = True

if overwrite_results and os.path.exists("results/experiments.csv"):
    os.remove("results/experiments.csv")

for size in graph_sizes:
    for g_type in graph_types:
        
        random.seed(1234)
        G = graph_gen.generate_sparse_graph(size) if g_type == "sparse" else graph_gen.generate_dense_graph(size)
        adj = graph_gen.nx_to_adjlist(G)
        sources = [next(iter(adj))]
        
        for alg_type in alg_types:
            for repeat in range(50):

                min_path, time_execution = experiment(adj, sources, alg_type)
                            
                save_results({
                    "algorithm": alg_type,
                    "graph_type": g_type,
                    "graph_size": size,
                    "n_edges": G.number_of_edges(),
                    "time_elapsed": time_execution,
                    # "adj_matrix": adj,
                    # "result": min_path,
                })

