use pyo3::prelude::*;
use numpy::{PyArray1, PyArrayMethods, PyReadonlyArray1};
use std::f64::consts::PI;

const MSUN: f64 = 1.988409870698051e+30;
const RSUN: f64 = 6.957e8;
const R_NS: f64 = 1.4e-5;
const CHANDRASEKHAR_MASS: f64 = 1.4 * MSUN;
const G: f64 = 6.67430e-11; // using si
const PERIOD_FACTOR: f64 = 4.0 * (PI * PI) / G;

#[pyfunction]
pub fn dwd_r_of_m<'py>(
    py: Python<'py>,
    m_arr: PyReadonlyArray1<'py, f64>,
) -> Bound<'py, PyArray1<f64>> {
    assert!(!m_arr.is_empty().unwrap());

    let m_slice = m_arr.as_slice().unwrap();

    let out_arr = unsafe{ PyArray1::new(py, m_slice.len(), false)};
    let out_slice = unsafe {out_arr.as_slice_mut().unwrap()};

    for (i, m) in m_slice.iter().enumerate() {

        let m_ratio: f64 = CHANDRASEKHAR_MASS / m;
        // could optimize further by simplifying this to a powf?
        let m_ch_m_2_3 = m_ratio.cbrt().powi(2);
        let m_m_ch_2_3 = (1.0/m_ratio).cbrt().powi(2);
        let a = 0.0115 * (m_ch_m_2_3 - m_m_ch_2_3).sqrt();

        let co = if R_NS > a {R_NS} else {a};
        out_slice[i] = RSUN * co;
    }
    out_arr
}

#[pyfunction]
pub fn dwd_rlof_a_of_m1_m2_r1_r2<'py>(
    py: Python<'py>,
    m1_arr: PyReadonlyArray1<'py, f64>,
    m2_arr: PyReadonlyArray1<'py, f64>,
    r1_arr: PyReadonlyArray1<'py, f64>,
    r2_arr: PyReadonlyArray1<'py, f64>,
) -> Bound<'py, PyArray1<f64>> {
    assert!(!m1_arr.is_empty().unwrap());
    let npts = m1_arr.len().unwrap();
    assert!(m2_arr.len().unwrap() == npts);
    assert!(r1_arr.len().unwrap() == npts);
    assert!(r2_arr.len().unwrap() == npts);

    let m1_slice = m1_arr.as_slice().unwrap();
    let m2_slice = m2_arr.as_slice().unwrap();
    let r1_slice = r1_arr.as_slice().unwrap();
    let r2_slice = r2_arr.as_slice().unwrap();

    let out_arr = unsafe{ PyArray1::new(py, m1_slice.len(), false)};
    let out_slice = unsafe {out_arr.as_slice_mut().unwrap()};

    for (i, (((m1, m2), r1), r2)) in m1_slice.iter().zip(m2_slice).zip(r1_slice).zip(r2_slice).enumerate() {
        let c1 = if m1 > m2 { m2 } else { m1 };
        let c2 = if m1 > m2 { m1 } else { m2 };
        let q = c1 / c2;

        let q_1_3 = q.cbrt();
        let q_2_3 = q_1_3.powi(2);

        // assuming C log is a natural log
        let numerator = 0.6 * q_2_3 + (1.0 + q_1_3).ln();
        let denominator = 0.49 * q_2_3;

        let c3 = if m1 > m2 {r2} else {r1};
        out_slice[i] = c3 * numerator / denominator;
    }
    out_arr
}

#[pyfunction]
pub fn dwd_rlof_p_of_m1_m2_r1_r2<'py>(
    py: Python<'py>,
    m1_arr: PyReadonlyArray1<'py, f64>,
    m2_arr: PyReadonlyArray1<'py, f64>,
    r1_arr: PyReadonlyArray1<'py, f64>,
    r2_arr: PyReadonlyArray1<'py, f64>,
) -> Bound<'py, PyArray1<f64>> {
    assert!(!m1_arr.is_empty().unwrap());
    let npts = m1_arr.len().unwrap();
    assert!(m2_arr.len().unwrap() == npts);
    assert!(r1_arr.len().unwrap() == npts);
    assert!(r2_arr.len().unwrap() == npts);

    let m1_slice = m1_arr.as_slice().unwrap();
    let m2_slice = m2_arr.as_slice().unwrap();
    let r1_slice = r1_arr.as_slice().unwrap();
    let r2_slice = r2_arr.as_slice().unwrap();

    let out_arr = unsafe{ PyArray1::new(py, m1_slice.len(), false)};
    let out_slice = unsafe {out_arr.as_slice_mut().unwrap()};

    for (i, (((m1, m2), r1), r2)) in m1_slice.iter().zip(m2_slice).zip(r1_slice).zip(r2_slice).enumerate() {

        let c1 = if m1 > m2 { m2 } else { m1 };
        let c2 = if m1 > m2 { m1 } else { m2 };
        let q = c1 / c2;

        let q_1_3 = q.cbrt();
        let q_2_3 = q_1_3.powi(2);

        // assuming C log is a natural log
        let numerator = 0.6 * q_2_3 + (1.0 + q_1_3).ln();
        let denominator = 0.49 * q_2_3;

        let c3 = if m1 > m2 {r2} else {r1};
        let a = c3 * numerator / denominator;

        out_slice[i] = (PERIOD_FACTOR * a.powi(3) / (m1 + m2)).sqrt();
    }
    out_arr
}
