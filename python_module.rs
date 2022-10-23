use pyo3::prelude::*;
use serde_json::{Value};
use std::collections::HashSet;

use crate::import::import::import as import;

#[pyfunction]
fn import_thick_triples(path: &str) -> HashSet<String> { 
    import(path) 
}


/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn ldtab_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(import_thick_triples, m)?)?;

    Ok(())
}
