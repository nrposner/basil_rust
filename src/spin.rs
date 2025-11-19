use pyo3::prelude::*;
use numpy::{PyArray1, PyArrayMethods, PyReadonlyArray1};

#[pyfunction]
pub fn chieff_of_m1_m2_chi1z_chi2z<'py>(
    py: Python<'py>,
    m1_arr: PyReadonlyArray1<'py, f64>,
    m2_arr: PyReadonlyArray1<'py, f64>,
    chi1z_arr: PyReadonlyArray1<'py, f64>,
    chi2z_arr: PyReadonlyArray1<'py, f64>,
) -> Bound<'py, PyArray1<f64>> {

    assert!(!m1_arr.is_empty().unwrap());
    assert!(m1_arr.len().unwrap() == m1_arr.len().unwrap());
    assert!(chi1z_arr.len().unwrap() == m1_arr.len().unwrap());
    assert!(chi2z_arr.len().unwrap() == m1_arr.len().unwrap());

    let m1_slice = m1_arr.as_slice().unwrap();
    let m2_slice = m2_arr.as_slice().unwrap();
    let chi1z_slice = chi1z_arr.as_slice().unwrap();
    let chi2z_slice = chi2z_arr.as_slice().unwrap();

    let out_arr = unsafe{ PyArray1::new(py, m1_slice.len(), false)};
    let out_slice = unsafe {out_arr.as_slice_mut().unwrap()};

    for (i, (((m1, m2), chi1z), chi2z)) in m1_slice.iter().zip(m2_slice).zip(chi1z_slice).zip(chi2z_slice).enumerate() {
        out_slice[i] = ((m1 * chi1z) + (m2 * chi2z)) / (m1 + m2);
    }
    out_arr
}


#[pyfunction]
pub fn chiminus_of_m1_m2_chi1z_chi2z<'py>(
    py: Python<'py>,
    m1_arr: PyReadonlyArray1<'py, f64>,
    m2_arr: PyReadonlyArray1<'py, f64>,
    chi1z_arr: PyReadonlyArray1<'py, f64>,
    chi2z_arr: PyReadonlyArray1<'py, f64>,
) -> Bound<'py, PyArray1<f64>> {

    assert!(!m1_arr.is_empty().unwrap());
    assert!(m1_arr.len().unwrap() == m1_arr.len().unwrap());
    assert!(chi1z_arr.len().unwrap() == m1_arr.len().unwrap());
    assert!(chi2z_arr.len().unwrap() == m1_arr.len().unwrap());

    let m1_slice = m1_arr.as_slice().unwrap();
    let m2_slice = m2_arr.as_slice().unwrap();
    let chi1z_slice = chi1z_arr.as_slice().unwrap();
    let chi2z_slice = chi2z_arr.as_slice().unwrap();

    let out_arr = unsafe{ PyArray1::new(py, m1_slice.len(), false)};
    let out_slice = unsafe {out_arr.as_slice_mut().unwrap()};

    for (i, (((m1, m2), chi1z), chi2z)) in m1_slice.iter().zip(m2_slice).zip(chi1z_slice).zip(chi2z_slice).enumerate() {
        out_slice[i] = ((m1 * chi1z) - (m2 * chi2z)) / (m1 + m2);
    }
    out_arr
}



#[pyfunction]
pub fn chi1z_of_m1_m2_chieff_chiminus<'py>(
    py: Python<'py>,
    m1_arr: PyReadonlyArray1<'py, f64>,
    m2_arr: PyReadonlyArray1<'py, f64>,
    chieff_arr: PyReadonlyArray1<'py, f64>,
    chiminus_arr: PyReadonlyArray1<'py, f64>,
) -> Bound<'py, PyArray1<f64>> {

    assert!(!m1_arr.is_empty().unwrap());
    assert!(m1_arr.len().unwrap() == m1_arr.len().unwrap());
    assert!(chieff_arr.len().unwrap() == m1_arr.len().unwrap());
    assert!(chiminus_arr.len().unwrap() == m1_arr.len().unwrap());

    let m1_slice = m1_arr.as_slice().unwrap();
    let m2_slice = m2_arr.as_slice().unwrap();
    let chieff_slice = chieff_arr.as_slice().unwrap();
    let chiminus_slice = chiminus_arr.as_slice().unwrap();

    let out_arr = unsafe{ PyArray1::new(py, m1_slice.len(), false)};
    let out_slice = unsafe {out_arr.as_slice_mut().unwrap()};

    for (i, (((m1, m2), chieff), chiminus)) in m1_slice.iter().zip(m2_slice).zip(chieff_slice).zip(chiminus_slice).enumerate() {
            out_slice[i] = (m1 + m2) * (chieff + chiminus) / (2.0*m1);
    }
    out_arr
}


#[pyfunction]
pub fn chi2z_of_m1_m2_chieff_chiminus<'py>(
    py: Python<'py>,
    m1_arr: PyReadonlyArray1<'py, f64>,
    m2_arr: PyReadonlyArray1<'py, f64>,
    chieff_arr: PyReadonlyArray1<'py, f64>,
    chiminus_arr: PyReadonlyArray1<'py, f64>,
) -> Bound<'py, PyArray1<f64>> {

    assert!(!m1_arr.is_empty().unwrap());
    assert!(m1_arr.len().unwrap() == m1_arr.len().unwrap());
    assert!(chieff_arr.len().unwrap() == m1_arr.len().unwrap());
    assert!(chiminus_arr.len().unwrap() == m1_arr.len().unwrap());

    let m1_slice = m1_arr.as_slice().unwrap();
    let m2_slice = m2_arr.as_slice().unwrap();
    let chieff_slice = chieff_arr.as_slice().unwrap();
    let chiminus_slice = chiminus_arr.as_slice().unwrap();

    let out_arr = unsafe{ PyArray1::new(py, m1_slice.len(), false)};
    let out_slice = unsafe {out_arr.as_slice_mut().unwrap()};

    for (i, (((m1, m2), chieff), chiminus)) in m1_slice.iter().zip(m2_slice).zip(chieff_slice).zip(chiminus_slice).enumerate() {
            out_slice[i] = (m1 + m2) * (chieff - chiminus) / (2.0*m2);

            // result[i] = (tm1 + tm2) * (tchieff - tchiMinus) / (2*tm2);
    }
    out_arr
}
