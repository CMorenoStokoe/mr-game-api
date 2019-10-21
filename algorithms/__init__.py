"""
Python package containing all the algorithms
for Graph analysis and exploration.

So far, the package provides:
- `BFS`: Breadth-First Search traversal with edge colouring (to avoid cycles and self-loops)
- `propagate`: Propagation function
"""

from .traversal import BFS
from .propagation import propagate