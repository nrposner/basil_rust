use pyo3::prelude::*;
use numpy::{PyReadonlyArray1, PyArray1, PyArrayMethods};

const G: f64 = 6.67430e-11; // using si
const C_LIGHT: f64 = 299_792_458.0; // using m/s

#[pyfunction]
fn beta_arr<'py>(
    py: Python<'py>,
    obj1: PyReadonlyArray1<'py, f64>,
    obj2: PyReadonlyArray1<'py, f64>,
) -> Bound<'py, PyArray1<f64>> {

    assert!(!obj1.is_empty().unwrap());
    assert!(obj1.len().unwrap() == obj2.len().unwrap());

    let factor = 12.8 * G.powi(3) * C_LIGHT.powf(-5.0);

    let obj1_slice = obj1.as_slice().unwrap();
    let obj2_slice = obj2.as_slice().unwrap();

    let out_arr = unsafe{ PyArray1::new(py, obj1_slice.len(), false)};
    let out_slice = unsafe {out_arr.as_slice_mut().unwrap()};

    for (i, (&o1, &o2)) in obj1_slice.iter().zip(obj2_slice).enumerate() {
        out_slice[i] = factor * o1 * o2 * (o1 + o2);
    };

    out_arr
}

#[pyfunction]
fn beta_sgl(d1: f64, d2: f64) -> f64 {
    let factor = 12.8 * G.powi(3) * C_LIGHT.powf(-5.0);
    factor * d1 * d2 * (d1 + d2)
}

#[pyfunction]
fn peters_ecc_const_sgl(ecc: f64) -> f64 {
    (1.0 - ecc.powi(2)) / 
    (
        ecc.powf(12.0/19.0) * (1.0 + (121.0 / 304.0) * ecc.powi(2)).powf(870.0/2299.0)
    )
}

#[pyfunction]
fn peters_ecc_const_arr<'py>(
    py: Python<'py>,
    eccs: PyReadonlyArray1<'py, f64>,
) -> Bound<'py, PyArray1<f64>>  {
    assert!(!eccs.is_empty().unwrap());

    let ecc_slice = eccs.as_slice().unwrap();

    let out_arr = unsafe{ PyArray1::new(py, ecc_slice.len(), false)};
    let out_slice = unsafe {out_arr.as_slice_mut().unwrap()};

    for (i, &ecc) in ecc_slice.iter().enumerate() {
        out_slice[i] = (1.0 - ecc.powi(2)) / ( ecc.powf(12.0/19.0) * (1.0 + (121.0 / 304.0) * ecc.powi(2)).powf(870.0/2299.0));
    };
    
    out_arr
}

#[pyfunction]
fn peters_ecc_integrand_sgl(ecc: f64) -> f64 {
    ecc.powf(29.0/19.0) * (1.0 + (121.0/304.0) * ecc.powi(2)).powf(1181.0/2299.0) * (1.0 - ecc.powi(2)).powf(-3.0/2.0)
    //  pow(ecc,29./19.) * pow(1 + (121./304.) * pow(ecc,2),1181./2299.) * pow(1 - pow(ecc,2), -3./2.)
}

#[pyfunction]
fn peters_ecc_integrand_arr(eccs: Vec<f64>) -> Vec<f64> {
    assert!(!eccs.is_empty());

    eccs.iter().map(|ecc| {
        ecc.powf(29.0/19.0) * (1.0 + (121.0/304.0) * ecc.powi(2)).powf(1181.0/2299.0) * (1.0 - ecc.powi(2)).powf(-3.0/2.0)
        // *out_ptr = pow(*ecc_ptr,29./19.) * pow(1 + (121./304.) * pow(*ecc_ptr,2),1181./2299.) * pow(1 - pow(*ecc_ptr,2), -3./2.);
    }).collect()
}

#[pyfunction]
fn merge_time_circ_arr(m1_arr: Vec<f64>, m2_arr: Vec<f64>, a_arr: Vec<f64>) -> Vec<f64> {
    let beta_factor = 12.8 * G.powi(3) * C_LIGHT.powf(-5.0);

    assert!(!m1_arr.is_empty());
    let npts = m1_arr.len();
    assert!(m2_arr.len() == npts);
    assert!(a_arr.len() == npts);

    m1_arr.iter().zip(m2_arr).zip(a_arr).map(|((m1, m2), a)| {
        let beta = beta_factor * m1 * m2 * (m1 + m2);
        
        (a.powi(2)).powi(2) / (4.0 * beta)
        // *out_ptr = pow(pow(*a0_ptr, 2),2) / (4 * beta);
    }).collect()
}

#[pyfunction]
fn merge_time_circ_sgl(m1: f64, m2: f64, a: f64) -> f64 {
    let beta_factor = 12.8 * G.powi(3) * C_LIGHT.powf(-5.0);
    let beta = beta_factor * m1 * m2 * (m1 + m2);
    (a.powi(2)).powi(2) / (4.0 * beta)
}

#[pyfunction]
fn orb_sep_evol_circ_arr(
    m1_arr: Vec<f64>, 
    m2_arr: Vec<f64>, 
    a0_arr: Vec<f64>,
    t_arr: Vec<f64>
) -> Vec<f64> {
    let beta_factor = 12.8 * G.powi(3) * C_LIGHT.powf(-5.0);

    assert!(!m1_arr.is_empty());
    let npts = m1_arr.len();
    assert!(m2_arr.len() == npts);
    assert!(a0_arr.len() == npts);
    assert!(t_arr.len() == npts);
    
    m1_arr.iter().zip(m2_arr).zip(a0_arr).zip(t_arr)
        .map(|(((m1, m2), a0), t)| { 
            let beta = beta_factor * m1 * m2 * (m1 + m2);
            (a0.powi(2).powi(2) - (4.0 * beta * t)).sqrt().sqrt()
        }).collect()
}

#[pyfunction]
fn orb_sep_evol_circ_sgl(m1: f64, m2: f64, a0: f64, t: f64) -> f64 {
    let beta_factor = 12.8 * G.powi(3) * C_LIGHT.powf(-5.0);

    let beta = beta_factor * m1 * m2 * (m1 + m2);
    (a0.powi(2).powi(2) - (4.0 * beta * t)).sqrt().sqrt()
}

#[pyfunction]
fn orb_sep_evol_ecc_integrand_arr<'py>(
    py: Python<'py>,
    preamble: f64,
    c0: f64,
    ecc_arr: PyReadonlyArray1<'py, f64>,
) -> Bound<'py, PyArray1<f64>> {
    
    assert!(!ecc_arr.is_empty().unwrap());

    // get a read-only slice to iterate over
    let ecc_slice = ecc_arr.as_slice().unwrap();

    // pre-allocate the new numpy array
    let out_arr = unsafe{ PyArray1::new(py, ecc_slice.len(), false)};
    let out_slice = unsafe {out_arr.as_slice_mut().unwrap()};

    // Now loop over the slices (no allocation)
    for (i, &ecc) in ecc_slice.iter().enumerate() {
        let sep = c0 / peters_ecc_const_sgl(ecc);
        out_slice[i] = preamble * (ecc/sep.powi(4)) * (1.0 + (121.0/304.0) * ecc.powi(2)) / (1.0 - ecc.powi(2)).powf(2.5);
    }
    
    out_arr
}

#[pyfunction]
fn orb_sep_evol_ecc_integrand_sgl(
    preamble: f64, 
    c0: f64,
    ecc: f64, 
) -> f64 {
    let sep = c0 / peters_ecc_const_sgl(ecc);
    preamble * (ecc/sep.powi(4)) * (1.0 + (121.0/304.0) * ecc.powi(2)) / (1.0 - (ecc).powi(2)).powf(2.5)
}

#[pymodule]
fn basil(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(beta_arr, m)?)?;
    m.add_function(wrap_pyfunction!(beta_sgl, m)?)?;
    m.add_function(wrap_pyfunction!(peters_ecc_const_arr, m)?)?;
    m.add_function(wrap_pyfunction!(peters_ecc_const_sgl, m)?)?;
    m.add_function(wrap_pyfunction!(peters_ecc_integrand_sgl, m)?)?;
    m.add_function(wrap_pyfunction!(peters_ecc_integrand_arr, m)?)?;
    m.add_function(wrap_pyfunction!(merge_time_circ_arr, m)?)?;
    m.add_function(wrap_pyfunction!(merge_time_circ_sgl, m)?)?;
    m.add_function(wrap_pyfunction!(orb_sep_evol_circ_arr, m)?)?;
    m.add_function(wrap_pyfunction!(orb_sep_evol_circ_sgl, m)?)?;
    m.add_function(wrap_pyfunction!(orb_sep_evol_ecc_integrand_arr, m)?)?;
    m.add_function(wrap_pyfunction!(orb_sep_evol_ecc_integrand_sgl, m)?)?;
    Ok(())
}
