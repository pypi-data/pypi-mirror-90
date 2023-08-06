//! Python bindings for networkg.

mod graph;

use pyo3::prelude::*;

/// Python bindings for networkg.
#[pymodule]
fn networkg(py: Python, m: &PyModule) -> PyResult<()> {
    let graph_module = graph::module(py)?;
    m.add_submodule(graph_module)?;

    Ok(())
}
