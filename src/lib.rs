use pyo3::exceptions as exc;
use pyo3::prelude::*;
use std::fs::OpenOptions;
use std::io;
use std::path::PathBuf;

/// from_file(path)
/// --
///
/// Get mimetype of file from file path
#[pyfunction]
fn from_file(path: PathBuf) -> PyResult<String> {
    // We receive a PathBuf as parameter to try to handle the variety of file path encoding in
    // different OS.
    let path = path.as_path();
    OpenOptions::new().read(true).open(path).map_err(|err| {
        // We can leave for PyO3 to convert io::Error to Python exception,
        // but PyO3 v0.14.2 doesn't have special case for PermissionDenied
        // (https://github.com/PyO3/pyo3/blob/0.14/src/err/impls.rs#L12),
        // so we do convert ourselves here. May be removed in future version.
        match err.kind() {
            io::ErrorKind::NotFound => exc::PyFileNotFoundError::new_err(err),
            io::ErrorKind::PermissionDenied => exc::PyPermissionError::new_err(err),
            _ => exc::PyOSError::new_err(err),
        }
    })?;
    let result = tree_magic_mini::from_filepath(path);
    Ok(result.unwrap().to_string())
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
fn is_file_of_type(path: PathBuf, mimetypes: Vec<&str>) -> PyResult<bool> {
    let path = path.as_path();
    let matched = mimetypes
        .iter()
        .any(|&t| tree_magic_mini::match_filepath(t, path));
    Ok(matched)
}

/// is_bytes_of_type(path, mimetypes)
/// --
///
/// Test if file content is of one of given mime types.
#[pyfunction]
fn is_bytes_of_type(bytes: &[u8], mimetypes: Vec<&str>) -> PyResult<bool> {
    let matched = mimetypes
        .iter()
        .any(|&t| tree_magic_mini::match_u8(t, bytes));
    Ok(matched)
}

#[pymodule]
fn defity(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add_function(wrap_pyfunction!(from_file, m)?)?;
    m.add_function(wrap_pyfunction!(from_bytes, m)?)?;
    m.add_function(wrap_pyfunction!(is_file_of_type, m)?)?;
    m.add_function(wrap_pyfunction!(is_bytes_of_type, m)?)?;
    Ok(())
}
