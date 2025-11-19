use std::f64::consts::PI;

use pyo3::prelude::*;
use numpy::{PyArray1, PyArrayMethods, PyReadonlyArray1};

const G: f64 = 6.67430e-11; // using si
// const C_LIGHT: f64 = 299_792_458.0; // using m/s

const PERIOD_FACTOR: f64 = 4.0 * (PI * PI) / G;

#[pyfunction]
pub fn orbital_period_of_m1_m2_a_arr<'py>(
    py: Python<'py>,
    m1_arr: PyReadonlyArray1<'py, f64>,
    m2_arr: PyReadonlyArray1<'py, f64>,
    a0_arr: PyReadonlyArray1<'py, f64>,
) -> Bound<'py, PyArray1<f64>> {

    assert!(!m1_arr.is_empty().unwrap());
    let npts = m1_arr.len().unwrap();
    assert!(m2_arr.len().unwrap() == npts);
    assert!(a0_arr.len().unwrap() == npts);

    let m1_slice = m1_arr.as_slice().unwrap();
    let m2_slice = m2_arr.as_slice().unwrap();
    let a0_slice = a0_arr.as_slice().unwrap();

    let out_arr = unsafe{ PyArray1::new(py, m1_slice.len(), false)};
    let out_slice = unsafe {out_arr.as_slice_mut().unwrap()};

    for (i, ((m1, m2), a0)) in m1_slice.iter().zip(m2_slice).zip(a0_slice).enumerate() {

        // wait, is the a0 part not just a cube??
        out_slice[i] = (PERIOD_FACTOR * (a0.powi(3)) / (m1 + m2)).sqrt();
        // *out_ptr = sqrt(period_factor * (*a0_ptr * pow(*a0_ptr, 2)) / (*m1_ptr + *m2_ptr));

    }

    out_arr
}

