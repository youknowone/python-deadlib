use std::ffi::CStr;
use pyo3::{prelude::*, ffi::{PyExc_OSError, PyErr_SetFromErrno}, types::PyString, exceptions::PyValueError};

// Future Rust versions will support `unsafe extern`
// unsafe
extern "C" {
    #[link_name = "crypt"]
    fn extern_crypt(key: *const u8, salt: *const u8) -> *const u8;
}

/// Hashes the concatenation of a word and a salt using SHA-256.
#[pyfunction]
fn crypt(word: &Bound<PyString>, salt: &Bound<PyString>) -> PyResult<String> {
    let word = word.encode_utf8()?;
    let salt = salt.encode_utf8()?;
    if word.as_bytes().contains(&b'\0') || salt.as_bytes().contains(&b'\0') {
        return Err(PyValueError::new_err("embedded null character"));
    }
    let crypt_result = unsafe {
        let word = word.as_bytes();
        let salt = salt.as_bytes();
        let result = extern_crypt(word.as_ptr(), salt.as_ptr());
        if result.is_null() {
            let err_ptr = PyErr_SetFromErrno(PyExc_OSError);
            let py = Python::assume_gil_acquired();
            return Err(PyErr::from_value_bound(Bound::from_owned_ptr_or_err(py, err_ptr)?));
        }
        CStr::from_ptr(result as *const _).to_str().expect("OS crypt returns weird values")
    };
    Ok(crypt_result.to_string())
}

/// A Python module implemented in Rust.
#[pymodule]
fn _crypt(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(crypt, m)?)?;
    Ok(())
}

#[test]
fn test_extern_crypt() {
    let key = c"";
    let salt = c"$6$V.wBvD6qcC/2U9B/";
    let r = unsafe { extern_crypt(key.as_ptr() as *const u8, salt.as_ptr() as *const u8) };
    assert_ne!(r, std::ptr::null());
}