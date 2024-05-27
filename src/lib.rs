use std::fs::OpenOptions;
use std::io;
use std::path::{Path, PathBuf};

use pyo3::exceptions as exc;
use pyo3::prelude::*;
use pyo3::pybacked::PyBackedStr;

/// from_file(path)
/// --
///
/// Get mimetype of file from file path
#[pyfunction]
fn from_file(py: Python, path: PathBuf) -> PyResult<String> {
    // We receive a PathBuf as parameter to try to handle the variety of file path encoding in
    // different OS.
    // The operations below only involve Rust pure data types, we don't need to hold
    // Python's GIL, so we release the lock to let other Python threads to run.
    py.allow_threads(|| {
        let path = path.as_path();
        check_file_readable(path)?;
        let result = tree_magic_mini::from_filepath(path);
        Ok(result.unwrap().to_string())
    })
}

/// from_bytes(content)
/// --
///
/// Get mimetype of file from file content
#[pyfunction]
fn from_bytes(py: Python, bytes: &[u8]) -> PyResult<String> {
    py.allow_threads(|| Ok(tree_magic_mini::from_u8(bytes).to_owned()))
}

/// is_file_of_type(path, mimetypes)
/// --
///
/// Test if file at given path is of one of given mime types.
#[pyfunction]
fn is_file_of_type(py: Python, path: PathBuf, mimetypes: Vec<PyBackedStr>) -> PyResult<bool> {
    py.allow_threads(|| {
        let path = path.as_path();
        check_file_readable(path)?;
        let matched = mimetypes
            .iter()
            .any(|t| tree_magic_mini::match_filepath(t, path));
        Ok(matched)
    })
}

/// is_bytes_of_type(path, mimetypes)
/// --
///
/// Test if file content is of one of given mime types.
#[pyfunction]
fn is_bytes_of_type(py: Python, bytes: &[u8], mimetypes: Vec<PyBackedStr>) -> PyResult<bool> {
    py.allow_threads(|| {
        let matched = mimetypes
            .iter()
            .any(|t| tree_magic_mini::match_u8(t, bytes));
        Ok(matched)
    })
}

// Because tree_magic_mini doesn't throw error when file is not accessible,
// we use OpenOptions to check those error cases, in order to return meaningful
// error to Python application.
fn check_file_readable(path: &Path) -> PyResult<()> {
    match OpenOptions::new().read(true).open(path) {
        // We can leave for PyO3 to convert io::Error to Python exception,
        // but PyO3 v0.14.2 doesn't have special case for PermissionDenied
        // (https://github.com/PyO3/pyo3/blob/0.14/src/err/impls.rs#L12),
        // so we do convert ourselves here. May be removed in future version.
        Ok(_) => Ok(()),
        Err(err) => match err.kind() {
            io::ErrorKind::NotFound => Err(exc::PyFileNotFoundError::new_err(err)),
            io::ErrorKind::PermissionDenied => Err(exc::PyPermissionError::new_err(err)),
            _ => Err(exc::PyOSError::new_err(err)),
        },
    }
}

#[pymodule]
fn defity(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add_function(wrap_pyfunction!(from_file, m)?)?;
    m.add_function(wrap_pyfunction!(from_bytes, m)?)?;
    m.add_function(wrap_pyfunction!(is_file_of_type, m)?)?;
    m.add_function(wrap_pyfunction!(is_bytes_of_type, m)?)?;
    Ok(())
}
