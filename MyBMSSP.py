import heapq

class BMSSP:
    def __init__(self, graph):
        self.max_depth = 0
        self.global_distances = {}
        self.n_recursoes = 0
        
        self.graph = graph
        
        self.vertices = set(graph.keys())
        self.vertices.update(v for u in graph for v in graph[u])
                
    def bounded_dijkstra(self, sources, bound):
        """
        Dijkstra limitado pelo bound.
        Retorna os vertices encontrados e os além do bound
        """
        heap = []
        distancias = {}
        visited = set()
        fronteira = []

        for s in sources:
            start_dist = self.global_distances.get(s, 0)
            distancias[s] = start_dist
            heapq.heappush(heap, (start_dist, s))

        while heap:
            # Pega o vertice de menor distância
            dist, next_vertice = heapq.heappop(heap)
            
            if dist >= bound:
                continue
            
            if next_vertice in visited:
                continue
            
            visited.add(next_vertice)
            
            # Atualiza a distância global
            if next_vertice not in self.global_distances or dist < self.global_distances[next_vertice]:
                self.global_distances[next_vertice] = dist
                
            
            for v, w in self.graph.get(next_vertice).items():
                new_dist = dist + w
                # Se está dentro fo limite (fronteira), considera para exploração
                if new_dist < bound:
                    if v not in visited:
                        if v not in distancias or new_dist < distancias[v]:
                            distancias[v] = new_dist
                            heapq.heappush(heap, (new_dist, v))
                else:
                    # Do contrário, adiciona na fronteira
                    fronteira.append((v, new_dist))

        return visited, fronteira
    
    def bmssp(self, sources, bound, max_depth=20, depth=0):
        """
        Core do BMSSP
        """
        self.n_recursoes += 1
        self.max_depth = max(self.max_depth, depth)

        if bound <= 0 or depth >= max_depth:
            return set()

        
        vertices_explorados, fronteira = self.bounded_dijkstra(sources, bound)

        for v, d in fronteira:
            remaining_bound = bound - (d - self.global_distances.get(v, float("inf")))
            if remaining_bound > 0:
                old_dist = self.global_distances.get(v, float("inf"))
                if d < old_dist:
                    self.global_distances[v] = d
                self.bmssp([v], bound - d, max_depth, depth + 1)


        return vertices_explorados
    
    def solve(self, sources, bound):
        """
        Ponto de partida do BMSSP.
        """
        self.global_distances = {s: 0 for s in sources}
        self.n_recursoes = 0
        self.max_depth = 0

        self.bmssp(sources, bound)

        return {v: d for v, d in self.global_distances.items() if d < bound}
