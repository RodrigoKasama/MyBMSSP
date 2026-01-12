import math

class FibNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.degree = 0
        self.mark = False

        self.parent = None
        self.child = None

        self.left = self
        self.right = self


class FibonacciHeap:
    def __init__(self):
        self.min = None
        self.n = 0

    def is_empty(self):
        return self.min is None

    def insert(self, key, value):
        node = FibNode(key, value)

        if self.min is None:
            self.min = node
        else:
            self._add_to_root_list(node)
            if node.key < self.min.key:
                self.min = node

        self.n += 1
        return node

    def _add_to_root_list(self, node):
        node.left = self.min
        node.right = self.min.right
        self.min.right.left = node
        self.min.right = node

    def extract_min(self):
        z = self.min
        if z is not None:

            if z.child is not None:
                children = []
                x = z.child
                while True:
                    children.append(x)
                    x = x.right
                    if x == z.child:
                        break

                for x in children:
                    self._add_to_root_list(x)
                    x.parent = None

            self._remove_from_root_list(z)

            if z == z.right:
                self.min = None
            else:
                self.min = z.right
                self._consolidate()

            self.n -= 1

        return z

    def _consolidate(self):
        A = [None] * (int(math.log2(self.n)) + 2)

        roots = []
        x = self.min
        while True:
            roots.append(x)
            x = x.right
            if x == self.min:
                break

        for w in roots:
            x = w
            d = x.degree
            while A[d] is not None:
                y = A[d]
                if x.key > y.key:
                    x, y = y, x
                self._link(y, x)
                A[d] = None
                d += 1
            A[d] = x

        self.min = None
        for node in A:
            if node is not None:
                if self.min is None or node.key < self.min.key:
                    self.min = node

    def _link(self, y, x):
        self._remove_from_root_list(y)
        y.left = y.right = y
        y.parent = x

        if x.child is None:
            x.child = y
        else:
            y.right = x.child.right
            y.left = x.child
            x.child.right.left = y
            x.child.right = y

        x.degree += 1
        y.mark = False

    def _remove_from_root_list(self, node):
        node.left.right = node.right
        node.right.left = node.left

    def decrease_key(self, x, k):
        if k > x.key:
            raise ValueError("Nova chave é maior que a atual")

        x.key = k
        y = x.parent

        if y is not None and x.key < y.key:
            self._cut(x, y)
            self._cascading_cut(y)

        if x.key < self.min.key:
            self.min = x

    def _cut(self, x, y):
        if y.child == x:
            if x.right != x:
                y.child = x.right
            else:
                y.child = None

        x.left.right = x.right
        x.right.left = x.left

        y.degree -= 1

        self._add_to_root_list(x)
        x.parent = None
        x.mark = False

    def _cascading_cut(self, y):
        z = y.parent
        if z is not None:
            if not y.mark:
                y.mark = True
            else:
                self._cut(y, z)
                self._cascading_cut(z)


def dijkstra_fibbo(adj, source):
    heap = FibonacciHeap()

    dist = {u: float("inf") for u in adj}
    nodes = {}

    dist[source] = 0

    for u in adj:
        nodes[u] = heap.insert(dist[u], u)

    while not heap.is_empty():
        min_node = heap.extract_min()
        u = min_node.value

        for v, w in adj[u]:
            if dist[v] > dist[u] + w:
                dist[v] = dist[u] + w
                heap.decrease_key(nodes[v], dist[v])

    return dist

# ##############################################################################

def dijkstra_trad(graph, source):
    # Inicializa as distâncias
    dist = {v: float('inf') for v in graph}
    dist[source] = 0

    # Vertices não visitados
    unvisited = set(graph.keys())

    while unvisited:
        # Vertice não visitado com menor distância
        current = min(unvisited, key=lambda v: dist[v])

        # Se a menor distância for infinita, cabou
        if dist[current] == float('inf'):
            break

        unvisited.remove(current)

		# Relaxation...
        for neighbor, weight in graph[current]:
            if neighbor in unvisited:
                alt = dist[current] + weight
                if alt < dist[neighbor]:
                    dist[neighbor] = alt

    return dist
