use pyo3::prelude::*;
use numpy::{PyArray1, PyArrayMethods, PyReadonlyArray1};

// minimal impact, as expected
// though kinda impressive how we get basically identical or slightly better performance with no
// pointer magic at all
#[pyfunction]
pub fn mc_of_m1_m2<'py>(
    py: Python<'py>,
    m1_arr: PyReadonlyArray1<f64>,
    m2_arr: PyReadonlyArray1<f64>,
) -> Bound<'py, PyArray1<f64>> {

    assert!(!m1_arr.is_empty().unwrap());
    assert!(m2_arr.len().unwrap() == m1_arr.len().unwrap());

    let m1_slice = m1_arr.as_slice().unwrap();
    let m2_slice = m2_arr.as_slice().unwrap();

    let out_arr = unsafe{ PyArray1::new(py, m1_slice.len(), false)};
    let out_slice = unsafe {out_arr.as_slice_mut().unwrap()};

    for (i, (m1, m2)) in m1_slice.iter().zip(m2_slice).enumerate() {
        out_slice[i] = (m1 * m2).powf(0.6) * (m1 + m2).powf(-0.2);
    }
    out_arr
}

// also unlikely to see much difference
// actually, we do see significant difference, and growing
#[pyfunction]
pub fn eta_of_m1_m2<'py>(
    py: Python<'py>,
    m1_arr: PyReadonlyArray1<f64>,
    m2_arr: PyReadonlyArray1<f64>,
) -> Bound<'py, PyArray1<f64>> {

    assert!(!m1_arr.is_empty().unwrap());
    assert!(m2_arr.len().unwrap() == m1_arr.len().unwrap());

    let m1_slice = m1_arr.as_slice().unwrap();
    let m2_slice = m2_arr.as_slice().unwrap();

    let out_arr = unsafe{ PyArray1::new(py, m1_slice.len(), false)};
    let out_slice = unsafe {out_arr.as_slice_mut().unwrap()};

    for (i, (m1, m2)) in m1_slice.iter().zip(m2_slice).enumerate() {
        out_slice[i] = (m1*m2) / ((m1 + m2) * (m1 + m2));
    }
    out_arr
}

// some extra speedup compared to doing each one at a time, but since the mc calculation is so much
// heavier, it dominates and the gain, though real, is small
#[pyfunction]
pub fn mc_and_eta_of_m1_m2<'py>(
    py: Python<'py>,
    m1_arr: PyReadonlyArray1<f64>,
    m2_arr: PyReadonlyArray1<f64>,
) -> (Bound<'py, PyArray1<f64>>, Bound<'py, PyArray1<f64>>) {

    assert!(!m1_arr.is_empty().unwrap());
    assert!(m2_arr.len().unwrap() == m1_arr.len().unwrap());

    let m1_slice = m1_arr.as_slice().unwrap();
    let m2_slice = m2_arr.as_slice().unwrap();

    let out_mc_arr = unsafe{ PyArray1::new(py, m1_slice.len(), false)};
    let out_eta_arr = unsafe{ PyArray1::new(py, m1_slice.len(), false)};
    let out_mc_slice = unsafe {out_mc_arr.as_slice_mut().unwrap()};
    let out_eta_slice = unsafe {out_eta_arr.as_slice_mut().unwrap()};

    for (i, (m1, m2)) in m1_slice.iter().zip(m2_slice).enumerate() {
        out_mc_slice[i] = (m1 * m2).powf(0.6) * (m1 + m2).powf(-0.2);
        out_eta_slice[i] = (m1*m2) / ((m1 + m2) * (m1 + m2));
    }
    (out_mc_arr, out_eta_arr)
}

#[pyfunction]
pub fn m_of_mc_eta<'py>(
    py: Python<'py>,
    mc_arr: PyReadonlyArray1<f64>,
    eta_arr: PyReadonlyArray1<f64>,
) -> Bound<'py, PyArray1<f64>> {

    assert!(!mc_arr.is_empty().unwrap());
    assert!(eta_arr.len().unwrap() == mc_arr.len().unwrap());

    let mc_slice = mc_arr.as_slice().unwrap();
    let eta_slice = eta_arr.as_slice().unwrap();

    let out_arr = unsafe{ PyArray1::new(py, mc_slice.len(), false)};
    let out_slice = unsafe {out_arr.as_slice_mut().unwrap()};

    for (i, (mc, eta)) in mc_slice.iter().zip(eta_slice).enumerate() {
        out_slice[i] = mc * eta.powf(-0.6);
    }
    out_arr
}

// does not work: check why
// likely something to do with the C code
// not actually operating on contiguous arrays like
// the other functions, but on views
#[pyfunction]
pub fn m1_of_m_eta<'py>(
    py: Python<'py>,
    m_arr: PyReadonlyArray1<f64>,
    eta_arr: PyReadonlyArray1<f64>,
) -> Bound<'py, PyArray1<f64>> {

    assert!(!m_arr.is_empty().unwrap());
    assert!(eta_arr.len().unwrap() == m_arr.len().unwrap());

    let m_slice = m_arr.as_slice().unwrap();
    let eta_slice = eta_arr.as_slice().unwrap();

    let out_arr = unsafe{ PyArray1::new(py, m_slice.len(), false)};
    let out_slice = unsafe {out_arr.as_slice_mut().unwrap()};

    for (i, (m, eta)) in m_slice.iter().zip(eta_slice).enumerate() {
        out_slice[i] = (m/2.0) * (1.0 + (1.0 - 4.0 * eta).sqrt());

        // m1[i] = (tM/2.)*(1. + sqrt(1. - 4.*teta));
    }
    out_arr
}

// why not merge this and m1?? almost identical, operating on the same data
// the original C code did that, but now it's commented out


#[pyfunction]
pub fn m2_of_m_eta<'py>(
    py: Python<'py>,
    m_arr: PyReadonlyArray1<f64>,
    eta_arr: PyReadonlyArray1<f64>,
) -> Bound<'py, PyArray1<f64>> {

    assert!(!m_arr.is_empty().unwrap());
    assert!(eta_arr.len().unwrap() == m_arr.len().unwrap());

    let m_slice = m_arr.as_slice().unwrap();
    let eta_slice = eta_arr.as_slice().unwrap();

    let out_arr = unsafe{ PyArray1::new(py, m_slice.len(), false)};
    let out_slice = unsafe {out_arr.as_slice_mut().unwrap()};

    for (i, (m, eta)) in m_slice.iter().zip(eta_slice).enumerate() {
        out_slice[i] = (m/2.0) * (1.0 - (1.0 - 4.0 * eta).sqrt());
    }
    out_arr
}

#[pyfunction]
pub fn detector_of_source<'py>(
    py: Python<'py>,
    m_arr: PyReadonlyArray1<f64>,
    z_arr: PyReadonlyArray1<f64>,
) -> Bound<'py, PyArray1<f64>> {

    assert!(!m_arr.is_empty().unwrap());
    assert!(z_arr.len().unwrap() == m_arr.len().unwrap());

    let m_slice = m_arr.as_slice().unwrap();
    let z_slice = z_arr.as_slice().unwrap();

    let out_arr = unsafe{ PyArray1::new(py, m_slice.len(), false)};
    let out_slice = unsafe {out_arr.as_slice_mut().unwrap()};

    for (i, (m, z)) in m_slice.iter().zip(z_slice).enumerate() {
        out_slice[i] = m * (z + 1.0);
    }

    out_arr
}

#[pyfunction]
pub fn source_of_detector<'py>(
    py: Python<'py>,
    m_arr: PyReadonlyArray1<f64>,
    z_arr: PyReadonlyArray1<f64>,
) -> Bound<'py, PyArray1<f64>> {

    assert!(!m_arr.is_empty().unwrap());
    assert!(z_arr.len().unwrap() == m_arr.len().unwrap());

    let m_slice = m_arr.as_slice().unwrap();
    let z_slice = z_arr.as_slice().unwrap();

    let out_arr = unsafe{ PyArray1::new(py, m_slice.len(), false)};
    let out_slice = unsafe {out_arr.as_slice_mut().unwrap()};

    for (i, (m, z)) in m_slice.iter().zip(z_slice).enumerate() {
        out_slice[i] = m / (z + 1.0);
    }

    out_arr
}

// joint mc and eta of m1_m2. If we're running over the same data, why run multiple times?
