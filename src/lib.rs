use std::fs::OpenOptions;
use std::path::Path;
use tree_magic_mini;
use pyo3::prelude::*;


/// from_file(path)
/// --
///
/// Get mimetype of file from file path
#[pyfunction]
fn from_file(path: &str) -> PyResult<String>{
    let path = Path::new(path);
    OpenOptions::new().read(true).open(path)?;
    let result = tree_magic_mini::from_filepath(path);
    Ok(result.unwrap().to_string())
}

#[pymodule]
fn defity(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add_function(wrap_pyfunction!(from_file, m)?)?;
    Ok(())
}
