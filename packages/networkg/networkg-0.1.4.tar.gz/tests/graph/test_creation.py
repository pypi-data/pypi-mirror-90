"""Test cases for the creation of Graph objects."""

import contextlib
import os
from tempfile import NamedTemporaryFile
from typing import ContextManager

import hypothesis as hyp
import pytest

from networkg.graph import Graph


class TestConstructor:
    """Test cases for the constructor of Graph."""

    def test_empty(self):
        """It creates a Graph with no nodes."""
        g = Graph()

        assert g.size == 0

    def test_disconnected(self):
        """It creates a disconnected Graph."""
        g = Graph(2)

        assert g.nodes == [[], []]


class TestFullyConnected:
    """Test cases for the `Graph.fully_connected` constructor."""

    def test_empty(self):
        """It creates a Graph with no nodes."""
        g = Graph.fully_connected(size=0)

        assert g.size == 0

    def test_right_number_of_nodes(self):
        """It creates a Graph with the right number of nodes."""
        g = Graph.fully_connected(3)

        assert g.size == 3

    def test_right_number_of_edges(self):
        """It creates a Graph with the right number of edges."""
        g = Graph.fully_connected(3)

        assert sum([len(edges) for edges in g.nodes]) == 6


class TestFromCSV:
    """Test cases for the `Graph.from_csv` constructor."""

    @pytest.fixture
    def empty_graph_csv(self, rootdir: str) -> str:
        """The path to an empty graph in csv-format."""
        return os.path.join(rootdir, "test_files/graphs/empty.csv")

    @pytest.fixture
    def small_space_delimited_graph_csv(self, rootdir: str) -> str:
        """The path to a graph with 4 nodes in space-delimited csv-format."""
        return os.path.join(rootdir, "test_files/graphs/small_spaces.csv")

    @pytest.fixture
    def small_comma_delimited_graph_csv(self, rootdir: str) -> str:
        """The path to a graph with 4 nodes in comma-delimited csv-format."""
        return os.path.join(rootdir, "test_files/graphs/small_spaces.csv")

    @pytest.fixture
    def broken_graph_csv(self, rootdir: str) -> str:
        """The path to a broken graph-csv."""
        return os.path.join(rootdir, "test_files/graphs/broken.csv")

    @contextlib.contextmanager
    def temp_graph_csv(self, delimiter: str) -> ContextManager[str]:
        """Creates a temporary graph-csv with specified delimiter.

        The created graph has two nodes, and a single edge from 0 to 1.

        Args:
            delimiter: String to use as delimiter in the csv.

        Yields:
            The path to the csv.
        """
        with NamedTemporaryFile("w", encoding="utf-8") as f:
            f.write(f"0{delimiter}1\n")
            f.flush()
            yield f.name

    def test_empty(self, empty_graph_csv):
        """It creates a Graph with no nodes."""
        g = Graph.from_csv(empty_graph_csv, 0, " ")

        assert g.size == 0

    def test_space_delimited(self, small_space_delimited_graph_csv):
        """It reads a space-delimited graph correctly."""
        g = Graph.from_csv(small_space_delimited_graph_csv, 4, " ")

        assert g.nodes == [[1], [2], [3], []]

    def test_comma_delimited(self, small_comma_delimited_graph_csv):
        """It reads a comma-delimited graph correctly."""
        g = Graph.from_csv(small_comma_delimited_graph_csv, 4, " ")

        assert g.nodes == [[1], [2], [3], []]

    def test_raises_on_broken_csv(self, broken_graph_csv):
        """It raises an error when the csv contains an error."""
        # TODO: Make exception more specific.
        with pytest.raises(ValueError):
            Graph.from_csv(broken_graph_csv, 10, " ")

    @hyp.given(
        hyp.strategies.characters(min_codepoint=128, blacklist_categories=["Cs"])
    )
    def test_raises_on_non_ascii_delimiter(self, delimiter):
        """It raises an error when the specified delimiter is a non-ASCII-char."""
        with self.temp_graph_csv(delimiter) as path:
            with pytest.raises(AttributeError):
                Graph.from_csv(path, 2, delimiter)

    @hyp.given(hyp.strategies.text(min_size=2))
    def test_raises_on_multiple_character_delimiter(self, delimiter):
        """It raises an error when the specified delimiter is more than one char."""
        with self.temp_graph_csv(delimiter) as path:
            with pytest.raises(AttributeError):
                Graph.from_csv(path, 2, delimiter)

    @hyp.given(
        hyp.strategies.characters(
            max_codepoint=127,
            blacklist_categories=["Nd"],  # Exclude numbers
            blacklist_characters=["\n"],
        )
    )
    @hyp.example("\t")
    @hyp.example(" ")
    @hyp.example(",")
    def test_reads_ascii_delimited_csv(self, delimiter):
        """It successfully reads an ASCII-delimited csv."""
        with self.temp_graph_csv(delimiter) as path:
            g = Graph.from_csv(path, 2, delimiter)
        assert g.nodes == [[1], []]
