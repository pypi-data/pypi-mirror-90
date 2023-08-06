"""Graph data structure."""
from typing import Dict, Iterable, List, Optional, Tuple

from networkg.networkg import _graph


class Graph:
    """Graph data structure."""

    def __init__(self, size: int = 0) -> None:
        """Initializes an empty graph with `size` nodes.

        Args:
            size: The number of nodes the graph should have.
        """
        self._graph = _graph.Graph(size)

    @classmethod
    def fully_connected(cls, size: int) -> "Graph":
        """Creates a fully connected graph with `size` nodes.

        Args:
            size: The number of nodes the graph should have.

        Returns:
            A fully connected graph with `size` nodes.
        """
        graph = cls()
        graph._graph = _graph.Graph.fully_connected(size)
        return graph

    @classmethod
    def from_csv(cls, path: str, size: int, delimiter: str) -> "Graph":
        """Creates a graph from a csv-file.

        Each row of the csv-file should contain exactly one node pair,
        represented by their indices.

        Indices should be positive integers in the range [0, size).

        Args:
            path: Path to the csv.
            size: The number of nodes the graph should have.
            delimiter: The character used as delimiter in the csv-file.

        Returns:
            A graph with edges read from `path`.
        """
        graph = cls()
        graph._graph = _graph.Graph.from_csv(path, size, delimiter)
        return graph

    @property
    def size(self) -> int:
        """The number of nodes in the graph."""
        return self._graph.size

    @property
    def nodes(self) -> List[List[int]]:
        """A list of all nodes in the graph, represented as an adjacency list."""
        return self._graph.nodes

    def add_edge(self, n1: int, n2: int) -> None:
        """Adds an edge between the nodes `n1` and `n2`.

        Both of the nodes need to exist in the graph.

        Args:
            n1: A node index
            n2: A node index

        Examples:
            >>> g = Graph(2)
            >>> g.nodes[0]
            []
            >>> g.add_edge(0, 1)
            >>> g.nodes[0]
            [1]
        """
        self._graph.add_edge(n1, n2)

    def add_edges(self, edges: Iterable[Tuple[int, int]]) -> None:
        """Adds multiple edges.

        Adds an edge between each pair of nodes in `edges`.

        Args:
            edges: An iterable of node pairs

        Examples:
            >>> g = Graph(4)
            >>> g.add_edges([(0, 1), (0, 2), (1, 3)])
        """
        self._graph.add_edges(edges)

    def single_source_shortest_path_length(
        self, source: int, cutoff: Optional[int] = None
    ) -> Dict[int, int]:
        """Calculates the shortest path lengths from `source` to all reachable nodes.

        Args:
            source: Node index from which to calculate shortest path lengths.
            cutoff:
                Stop search at this path length.
                No paths longer than `cutoff` are returned.

        Returns:
            A dictionary mapping each node reachable from `source` to the shortest
            path length between them.

        Examples:
            Basic usage:
            >>> g = Graph(4)
            >>> g.add_edges([(0, 1), (1, 2)])
            >>> g.single_source_shortest_path_length(0) == {0: 0, 1: 1, 2: 2}
            True

            With cutoff:
            >>> g = Graph(4)
            >>> g.add_edges([(0, 1), (1, 2)])
            >>> g.single_source_shortest_path_length(0, cutoff=1) == {0: 0, 1: 1}
            True

        """
        if source >= self._graph.size:
            raise AttributeError(
                f"Specified `source` ({source})"
                f"does not exist in graph of size ({self.size})."
            )
        return self._graph.single_source_shortest_path_length(source, cutoff)
