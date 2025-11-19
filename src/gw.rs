use std::f64::consts::PI;
use pyo3::prelude::*;
use numpy::{PyArray1, PyArrayMethods, PyReadonlyArray1};

const C_LIGHT: f64 = 299_792_458.0; // using m/s
const G: f64 = 6.67430e-11; // using si
const PERIOD_FACTOR: f64 = 4.0 * (PI * PI) / G;

#[pyfunction]
pub fn beta<'py>(
    py: Python<'py>,
    m1_arr: PyReadonlyArray1<'py, f64>,
    m2_arr: PyReadonlyArray1<'py, f64>,
) -> Bound<'py, PyArray1<f64>> {

    assert!(!m1_arr.is_empty().unwrap());
    let npts = m1_arr.len().unwrap();
    assert!(m2_arr.len().unwrap() == npts);

    let m1_slice = m1_arr.as_slice().unwrap();
    let m2_slice = m2_arr.as_slice().unwrap();

    let out_arr = unsafe{ PyArray1::new(py, m1_slice.len(), false)};
    let out_slice = unsafe {out_arr.as_slice_mut().unwrap()};

    for (i, (m1, m2)) in m1_slice.iter().zip(m2_slice).enumerate() {
        out_slice[i] = (PERIOD_FACTOR * m1 * m2 * (m1 + m2)).sqrt();
    }

    out_arr
}


// same as orb_sep_evol_circ_arr in decay
#[pyfunction]
pub fn orbital_separation_evolve<'py>(
    py: Python<'py>,
    m1_arr: PyReadonlyArray1<'py, f64>,
    m2_arr: PyReadonlyArray1<'py, f64>,
    a0_arr: PyReadonlyArray1<'py, f64>,
    t_arr: PyReadonlyArray1<'py, f64>
) -> Bound<'py, PyArray1<f64>> {
    let beta_factor = 12.8 * G.powi(3) * C_LIGHT.powf(-5.0);

    assert!(!m1_arr.is_empty().unwrap());
    let npts = m1_arr.len().unwrap();
    assert!(m2_arr.len().unwrap() == npts);
    assert!(a0_arr.len().unwrap() == npts);
    assert!(t_arr.len().unwrap() == npts);
    
    let m1_slice = m1_arr.as_slice().unwrap();
    let m2_slice = m2_arr.as_slice().unwrap();
    let a_slice = a0_arr.as_slice().unwrap();
    let t_slice = t_arr.as_slice().unwrap();

    let out_arr = unsafe{ PyArray1::new(py, m1_slice.len(), false)};
    let out_slice = unsafe {out_arr.as_slice_mut().unwrap()};

    for (i, (((m1, m2), a0), t)) in m1_slice.iter().zip(m2_slice).zip(a_slice).zip(t_slice).enumerate() {
        let beta = beta_factor * m1 * m2 * (m1 + m2);
        out_slice[i] = (a0.powi(2).powi(2) - (4.0 * beta * t)).sqrt().sqrt()
    };

    out_arr
}

#[pyfunction]
pub fn time_of_orbital_shrinkage<'py>(
    py: Python<'py>,
    m1_arr: PyReadonlyArray1<'py, f64>,
    m2_arr: PyReadonlyArray1<'py, f64>,
    a0_arr: PyReadonlyArray1<'py, f64>,
    af_arr: PyReadonlyArray1<'py, f64>
) -> Bound<'py, PyArray1<f64>> {
    let beta_factor = 12.8 * G.powi(3) * C_LIGHT.powf(-5.0);

    assert!(!m1_arr.is_empty().unwrap());
    let npts = m1_arr.len().unwrap();
    assert!(m2_arr.len().unwrap() == npts);
    assert!(a0_arr.len().unwrap() == npts);
    assert!(af_arr.len().unwrap() == npts);
    
    let m1_slice = m1_arr.as_slice().unwrap();
    let m2_slice = m2_arr.as_slice().unwrap();
    let a0_slice = a0_arr.as_slice().unwrap();
    let af_slice = af_arr.as_slice().unwrap();

    let out_arr = unsafe{ PyArray1::new(py, m1_slice.len(), false)};
    let out_slice = unsafe {out_arr.as_slice_mut().unwrap()};

    for (i, (((m1, m2), a0), af)) in m1_slice.iter().zip(m2_slice).zip(a0_slice).zip(af_slice).enumerate() {
        let beta = beta_factor * m1 * m2 * (m1 + m2);

        out_slice[i] = ((a0.powi(4)) - (af.powi(4))) / (4.0 * beta)
    };

    out_arr
}


#[pyfunction]
pub fn time_to_merge_of_m1_m2_a0<'py>(
    py: Python<'py>,
    m1_arr: PyReadonlyArray1<'py, f64>,
    m2_arr: PyReadonlyArray1<'py, f64>,
    a0_arr: PyReadonlyArray1<'py, f64>,
) -> Bound<'py, PyArray1<f64>> {
    let beta_factor = 12.8 * G.powi(3) * C_LIGHT.powf(-5.0);

    assert!(!m1_arr.is_empty().unwrap());
    let npts = m1_arr.len().unwrap();
    assert!(m2_arr.len().unwrap() == npts);
    assert!(a0_arr.len().unwrap() == npts);
    
    let m1_slice = m1_arr.as_slice().unwrap();
    let m2_slice = m2_arr.as_slice().unwrap();
    let a_slice = a0_arr.as_slice().unwrap();

    let out_arr = unsafe{ PyArray1::new(py, m1_slice.len(), false)};
    let out_slice = unsafe {out_arr.as_slice_mut().unwrap()};

    for (i, ((m1, m2), a0)) in m1_slice.iter().zip(m2_slice).zip(a_slice).enumerate() {
        let beta = beta_factor * m1 * m2 * (m1 + m2);

        out_slice[i] = (a0.powi(4)) / (4.0 * beta)
    };

    out_arr
}


#[pyfunction]
pub fn orbital_period_evolved_gw<'py>(
    py: Python<'py>,
    m1_arr: PyReadonlyArray1<'py, f64>,
    m2_arr: PyReadonlyArray1<'py, f64>,
    a0_arr: PyReadonlyArray1<'py, f64>,
    t_arr: PyReadonlyArray1<'py, f64>,
) -> Bound<'py, PyArray1<f64>> {
    let beta_factor = 12.8 * G.powi(3) * C_LIGHT.powf(-5.0);

    assert!(!m1_arr.is_empty().unwrap());
    let npts = m1_arr.len().unwrap();
    assert!(m2_arr.len().unwrap() == npts);
    assert!(a0_arr.len().unwrap() == npts);
    assert!(t_arr.len().unwrap() == npts);
    
    let m1_slice = m1_arr.as_slice().unwrap();
    let m2_slice = m2_arr.as_slice().unwrap();
    let a0_slice = a0_arr.as_slice().unwrap();
    let t_slice = t_arr.as_slice().unwrap();

    let out_arr = unsafe{ PyArray1::new(py, m1_slice.len(), false)};
    let out_slice = unsafe {out_arr.as_slice_mut().unwrap()};

    for (i, (((m1, m2), a0), t)) in m1_slice.iter().zip(m2_slice).zip(a0_slice).zip(t_slice).enumerate() {
        let beta = beta_factor * m1 * m2 * (m1 + m2);

        let af = (a0.powi(4) - 4.0 * beta * t).sqrt().sqrt();
        // af = sqrt(sqrt(pow(pow(*a0_ptr, 2),2) - 4 * beta * (*t_ptr)));
        out_slice[i] = PERIOD_FACTOR * af.powi(3) / (m1 + m2);
    };

    out_arr
}



