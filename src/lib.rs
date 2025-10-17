use std::fs::OpenOptions;
use std::path::{Path, PathBuf};

use pyo3::prelude::*;
use pyo3::pybacked::PyBackedStr;

const DEFAULT_UNKNOWN: &str = "application/octet-stream";

/// from_file(path)
/// --
///
/// Get mimetype of file from file path
#[pyfunction]
fn from_file(path: PathBuf) -> PyResult<String> {
    // We receive a PathBuf as parameter to try to handle the variety of file path encoding in
    // different OS.
    // The operations below only involve Rust pure data types, we don't need to hold
    // Python's GIL, so we release the lock to let other Python threads to run.
    let path = path.as_path();
    // tree_magic_mini::from_filepath returns `None` for both case:
    // File not openable and MIME not found. We resolve that ambiguity
    // by checking file first.
    check_file_readable(path)?;
    let result = tree_magic_mini::from_filepath(path);
    let mime = result.map(String::from);
    Ok(mime.unwrap_or_else(|| String::from(DEFAULT_UNKNOWN)))
}

/// from_bytes(content)
/// --
///
/// Get mimetype of file from file content
#[pyfunction]
fn from_bytes(bytes: &[u8]) -> PyResult<String> {
    Ok(tree_magic_mini::from_u8(bytes).to_owned())
}

/// is_file_of_type(path, mimetypes)
/// --
///
/// Test if file at given path is of one of given mime types.
#[pyfunction]
fn is_file_of_type(path: PathBuf, mimetypes: Vec<PyBackedStr>) -> PyResult<bool> {
    let path = path.as_path();
    check_file_readable(path)?;
    let matched = mimetypes
        .iter()
        .any(|t| tree_magic_mini::match_filepath(t, path));
    Ok(matched)
}

/// is_bytes_of_type(path, mimetypes)
/// --
///
/// Test if file content is of one of given mime types.
#[pyfunction]
fn is_bytes_of_type(bytes: &[u8], mimetypes: Vec<PyBackedStr>) -> PyResult<bool> {
    let matched = mimetypes
        .iter()
        .any(|t| tree_magic_mini::match_u8(t, bytes));
    Ok(matched)
}

// Because tree_magic_mini doesn't throw error when file is not accessible,
// we use OpenOptions to check those error cases, in order to return meaningful
// error to Python application.
fn check_file_readable(path: &Path) -> PyResult<()> {
    OpenOptions::new().read(true).open(path)?;
    Ok(())
}

#[pymodule(gil_used = false)]
fn defity(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add_function(wrap_pyfunction!(from_file, m)?)?;
    m.add_function(wrap_pyfunction!(from_bytes, m)?)?;
    m.add_function(wrap_pyfunction!(is_file_of_type, m)?)?;
    m.add_function(wrap_pyfunction!(is_bytes_of_type, m)?)?;
    Ok(())
}
