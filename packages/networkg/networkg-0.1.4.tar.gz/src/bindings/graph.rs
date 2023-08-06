//! Python bindings for the graph module
use crate::core::graph::{Graph, Node};

use std::{collections::HashMap, convert::TryFrom};

use pyo3::exceptions::{PyAttributeError, PyValueError};
use pyo3::prelude::*;
use pyo3::types::{PyIterator, PyType};

/// Submodule containing Python bindings for the Graph datastructure
pub fn module(py: Python) -> PyResult<&PyModule> {
    let module = PyModule::new(py, "_graph")?;
    module.add_class::<PyGraph>()?;
    Ok(module)
}

/// Python bindings for the networkg Graph
#[pyclass(name=Graph)]
struct PyGraph {
    graph: Graph,
}

#[pymethods]
impl PyGraph {
    #[new]
    #[args(size = "0")]
    fn new(size: usize) -> PyResult<Self> {
        Ok(PyGraph {
            graph: Graph::new(size),
        })
    }

    #[classmethod]
    #[text_signature = "(size)"]
    fn fully_connected(_cls: &PyType, size: usize) -> PyResult<Self> {
        Ok(PyGraph {
            graph: Graph::fully_connected(size),
        })
    }

    #[classmethod]
    #[text_signature = "(path, delimiter)"]
    fn from_csv(_cls: &PyType, path: &str, size: usize, delimiter: &str) -> PyResult<Self> {
        match str_as_char_u8(delimiter) {
            Ok(delimiter) => match Graph::from_csv(path, size, delimiter) {
                Ok(graph) => Ok(PyGraph { graph }),
                Err(error) => Err(PyValueError::new_err(error)),
            },
            Err(_) => Err(PyAttributeError::new_err(format!(
                "Invalid delimiter: {}. Delimiter must be a single ASCII-character.",
                delimiter
            ))),
        }
    }

    #[getter]
    fn size(&self) -> PyResult<usize> {
        Ok(self.graph.size())
    }

    #[getter]
    fn nodes(&self) -> PyResult<Vec<Node>> {
        Ok(self.graph.nodes.clone())
    }

    #[text_signature = "(n1, n2)"]
    fn add_edge(&mut self, n1: usize, n2: usize) -> PyResult<()> {
        match self.graph.add_edge(n1, n2) {
            Ok(()) => Ok(()),
            Err(error) => Err(PyAttributeError::new_err(error)),
        }
    }

    #[text_signature = "(edges)"]
    fn add_edges<'p>(&mut self, py: Python<'p>, edges: &PyAny) -> PyResult<()> {
        let edges_py_iterator = PyIterator::from_object(py, edges)?;
        let edges_iter = edges_py_iterator.map(|x| x.and_then(PyAny::extract::<(usize, usize)>));
        match self.graph.add_falliable_edges(edges_iter) {
            Ok(()) => Ok(()),
            Err(error) => Err(PyAttributeError::new_err(error)),
        }
    }

    #[text_signature = "(source, cutoff)"]
    #[args(cutoff = "None")]
    fn single_source_shortest_path_length(
        &self,
        source: usize,
        cutoff: Option<u32>,
    ) -> PyResult<HashMap<usize, u32>> {
        Ok(self
            .graph
            .single_source_shortest_path_length(source, cutoff))
    }
}

fn str_as_char_u8(s: &str) -> Result<u8, ()> {
    if s.len() == 1 {
        if let Some(c) = s.chars().next() {
            if let Ok(char_u32) = u32::try_from(c) {
                if let Ok(char_u8) = u8::try_from(char_u32) {
                    return Ok(char_u8);
                };
            };
        };
    };
    Err(())
}
