//! Graph data structure.

use crate::core::io::read_edge_list_csv;

pub type Node = Vec<usize>;

/// A directed edge `(n1, n2)` from `n1` to `n2`.
pub type Edge = (usize, usize);

/// A directed graph.
///
/// A directed graph represented as an adjacency list.
/// Nodes are densely indexed, starting at 0,
/// meaning that a graph with N nodes will have the nodes:
/// 0, 1, ..., N-1.
///
/// # Examples:
/// Basic usage:
/// ```
/// # use networkg::core::graph::Graph;
/// # fn main() -> Result<(), String> {
/// let mut graph = Graph::new(10);
///
/// assert_eq!(10, graph.size());
/// assert!(graph.nodes[0].is_empty());
///
/// graph.add_edge(0, 9)?;
/// assert_eq!(vec![9], graph.nodes[0]);
/// # Ok(())
/// # }
/// ```
pub struct Graph {
    pub nodes: Vec<Node>,
}

impl Graph {
    /// Creates a new graph.
    pub fn new(size: usize) -> Self {
        Graph {
            nodes: vec![vec![]; size],
        }
    }

    /// Returns the number of nodes in the graph.
    pub fn size(&self) -> usize {
        self.nodes.len()
    }

    /// Creates a fully connected graph.
    ///
    /// A fully connected graph is a graph where there is an edge between every node
    /// pair.
    ///
    /// # Examples:
    /// ```
    /// # use networkg::core::graph::Graph;
    /// let mut graph = Graph::fully_connected(3);
    /// assert_eq!(vec![1, 2], graph.nodes[0]);
    /// ```
    pub fn fully_connected(size: usize) -> Self {
        Graph {
            nodes: (0..size)
                .map(|n| (0..size).filter(|i| *i != n).collect())
                .collect(),
        }
    }

    /// Load graph from a csv-file.
    ///
    /// The csv-file should contain one node-pair per row.
    /// The nodes in a pair should be separated by an non-numeric ASCII character.
    /// Example of a space-delimited file:
    /// ```txt
    /// 0 1
    /// 1 2
    /// ```
    ///
    /// # Errors
    /// * If the specified csv-file could not be opened.
    /// * If the csv-file is malformed.
    /// * If any node index in the csv is larger than or equal to `size`.
    ///
    ///
    /// # Examples
    /// ```no_run
    /// # use networkg::core::graph::Graph;
    /// # fn main() -> Result<(), String> {
    /// let graph = Graph::from_csv("graph.csv", 10, b' ')?;
    /// # Ok(())
    /// # }
    /// ```
    pub fn from_csv(path: &str, size: usize, delimiter: u8) -> Result<Self, String> {
        let mut graph = Graph::new(size);
        graph.add_falliable_edges(read_edge_list_csv(path, delimiter)?)?;
        Ok(graph)
    }

    /// Adds an edge from node `n1` to `n2`.
    ///
    /// # Errors
    /// If either `n1` or `n2` are too large to fit in the graph.
    ///
    /// # Examples
    /// ```
    /// # use networkg::core::graph::Graph;
    /// # fn main() -> Result<(), String> {
    /// let mut graph = Graph::new(2);
    /// graph.add_edge(0, 1)?;
    /// assert_eq!(vec![1], graph.nodes[0]);
    /// # Ok(())
    /// # }
    /// ```
    ///
    /// # TODO
    /// Possibly panic instead of returning an error.
    /// I believe this would make the Rust code more ideomatic, since calling with
    /// an argument which is too large is a contract breach on the caller side.
    /// It has the advantage of simplifying any code that uses `add_edge`.
    /// However, this would require the bindings module to handle Panics, and convert
    /// them to appropriate Python exceptions.
    pub fn add_edge(&mut self, n1: usize, n2: usize) -> Result<(), String> {
        if n1.max(n2) >= self.size() {
            Err(format!(
                "Node with id {} does not fit in Graph of size {}.",
                n1.max(n2),
                self.size(),
            ))
        } else {
            self.nodes[n1].push(n2);
            Ok(())
        }
    }
    /// Adds multiple edges to the graph from an iterator of [`Edge`] tuples.
    ///
    /// # Errors
    /// If any of the `Edge` tuples contains a node with an index that is too large to
    /// fit in the graph.
    ///
    /// # Examples
    /// ```
    /// # use networkg::core::graph::Graph;
    /// # fn main() -> Result<(), String> {
    /// let mut graph = Graph::new(3);
    /// let edges = vec![(0, 1), (1, 2)];
    /// graph.add_edges(edges.into_iter())?;
    /// assert_eq!(vec![vec![1], vec![2], vec![]], graph.nodes);
    /// # Ok(())
    /// # }
    /// ```
    pub fn add_edges(&mut self, mut edges: impl Iterator<Item = Edge>) -> Result<(), String> {
        edges.try_for_each(|(n1, n2)| self.add_edge(n1, n2))
    }

    /// Adds multiple edges to the graph from an iterator of `Result<Edge>`,
    /// stopping at the first encountered error an returning an error.
    ///
    /// # Errors
    /// * If any of the items in the iterator is an `Err`.
    /// * If any of the `Edge` tuples contains a node with an index that is too large to
    ///   fit in the graph.
    ///
    /// # Examples
    /// ```
    /// # use networkg::core::graph::Graph;
    /// # fn main() -> Result<(), String> {
    /// let mut graph = Graph::new(3);
    /// let edges = vec![Ok((0, 1)), Err("Something went wrong!")];
    /// let result = graph.add_falliable_edges(edges.into_iter());
    /// assert!(result.is_err());
    /// # Ok(())
    /// # }
    /// ```
    pub fn add_falliable_edges(
        &mut self,
        mut edges: impl Iterator<Item = Result<Edge, impl std::string::ToString>>,
    ) -> Result<(), String> {
        edges.try_for_each(|x| match x {
            Ok((n1, n2)) => self.add_edge(n1, n2),
            Err(error) => Err(error.to_string()),
        })
    }
}
