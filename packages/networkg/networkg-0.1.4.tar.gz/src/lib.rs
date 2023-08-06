pub mod core;

// Don't create bindings when running with test feature.
// Workaround for https://github.com/PyO3/pyo3/issues/340 which allows for doctests.
// Source of workaround: https://github.com/rust-lang/rust/issues/45599
#[cfg(not(feature = "test"))]
pub mod bindings;
