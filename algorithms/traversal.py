import networkx as nx
from collections import deque

# Colours
WHITE = 'white'
BLACK = 'black'


class BFS:
    """This class implements Breadth-First Search (BFS) Traversal algorithm, with
    edge coloring.
    The edge coloring technique is implemented to avoid cycles and self-loops
    in the navigation of the Graph.

    Examples
    --------
    >>> bfs = BFS(G)  # instantiate the BFS object
    >>> bfs_edges = iter(bfs(source='source-node'))
    >>> for edge in bfs_edges:
    ...    print(edge)
    """

    def __init__(self, G: nx.DiGraph):
        self._BfsG = G.copy()
        nx.set_node_attributes(self._BfsG, WHITE, 'color')
        self._source = None

    @property
    def source(self):
        if self._source is None:
            raise AttributeError('Please specify a source first!')
        return self._source

    @source.setter
    def source(self, node: str):
        if node not in self._BfsG:
            raise ValueError('Input node is not in the graph!')
        self._source = node

    def __call__(self, source: str):
        """Callable object to foster the traversal from given source node."""
        self._source = source
        return self.__iter__()

    def __iter__(self):
        if self._source is None:
            raise AttributeError('No Source is specified!')

        def neighbourhood(gnode):
            nhbs = filter(lambda n: self._BfsG.nodes[n]['color'] != BLACK, self._BfsG[gnode])
            return list(nhbs)

        def color(gnode):
            return self._BfsG.nodes[gnode]['color']

        Q = deque()
        Q.appendleft(self._source)
        while Q:
            node = Q.popleft()
            if color(node) == BLACK:
                continue
            neighbours = neighbourhood(node)
            if neighbours:
                edges = [(node, v) for v in neighbours]
                edges = sorted(edges, key=lambda e: len(neighbourhood(e[1])))
                for (u, v) in edges:
                    yield (u, v)
                    Q.append(v)
                self._BfsG.nodes[node]['color'] = BLACK
