import networkx as nx
from typing import Dict, Callable, List, Set, Sequence, Tuple
from collections import defaultdict
from .traversal import BFS


def agg_mean(l: List[float]) -> float:
    """Simple implementation of arithmetic Mean.
    So far, I am using this function so to **not**
    include NumPy just for this as (huge) dependency
    in the requirements.
    In future, it would be better to replace this with NumPy.
    """
    return sum(l) / len(l)


# Typing for Documentation
WeightMap = Dict[str, Dict[str, float]]
AggregationFn = Callable[[List[float]], float]
Edge = Tuple[str, str]
Path = Sequence[Edge]
CycleEdges = Set[Edge]


def propagate(G: nx.DiGraph, n: str, activation: int,
              agg_fn: AggregationFn = agg_mean,
              node_activation_key: str = 'activation',
              edge_beta_key: str = 'value') -> WeightMap:
    """
    Function to calculate the propagation effect
    on the Graph `G` from node `n`.

    Parameters
    ----------
    G: networkx.DiGraph object
        NetworkX Directed Graph object on which to apply the propagation.

    n: str
        The node in the graph `G` from which initiate the propagation

    activation: int
        The activation of the target node `n`

    agg_fn: function object
        The aggregation function to use when more than one
        change is applied to nodes. (default: the arithmetic Mean)

    node_activation_key: str (default "activation")
        The key attribute in the input graph `G`
        referencing nodes' activations.

    edge_beta_key: str (default: "value")
        The key attribute in the input graph `G`
        denoting weights on the edges.

    Returns
    -------
    WeightMap:  dictionary containing the new "activation"
    attribute for each node.
    The structure of this map will be as a dict of dict
    to be compliant with the `networkx.set_nodes_attribute` function.
    """

    node_activations = nx.get_node_attributes(G, node_activation_key)
    node_activations[n] = activation

    propagation_path = defaultdict(list)

    # BFS on all edges induced by target source node `n`
    # The BFS w. edge colouring algorithm will
    # (1) avoid getting stuck in cycles and self-loops,
    # i.e. arcs leading to loops will be simply skipped;
    # (2) arcs will be returned so that nodes with
    # the smaller neighbourhood of un-visited nodes will be
    # processed first.
    bfs = BFS(G)  # leverage on BFS w. edge colouring
    source_node = n
    for edge in bfs(n):
        u, v = edge
        if source_node is not u:
            source_node = u  # update the reference source_node
            # Before proceeding, we need to collect and update
            # the activation of the source node, to be used later on
            # during the updates of next edges.

            # Note: to avoid inconsistencies with the final round of
            # updates, we remove the new source_node from the propagation map
            # once updated!
            activations = propagation_path.pop(u)
            node_activations[u] = agg_fn(activations)

        beta = G.edges[edge][edge_beta_key]
        if beta < 0:
            # divide if the beta is negative.
            beta = 1 / abs(beta)
        weight = node_activations[u]
        v_activation = G[v][node_activation_key]
        propagation_factor = 1 / (weight * beta)
        updated_activation = v_activation * propagation_factor
        propagation_path[v].append(updated_activation)

    # Finalise the weights for the remaining nodes
    for node, activations in propagation_path.items():
        node_activations[node] = agg_fn(activations)

    return {node: {node_activation_key: activation} for node, activation in node_activations.items()}
