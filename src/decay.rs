use pyo3::prelude::*;
// use rayon::prelude::*;
use numpy::{PyReadonlyArray1, PyArray1, PyArrayMethods};

const G: f64 = 6.67430e-11; // using si
const C_LIGHT: f64 = 299_792_458.0; // using m/s

#[pyfunction]
pub fn beta_arr<'py>(
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

    out_slice.iter_mut()
        .enumerate()
        .for_each(|(i, out_val)| {
            // using indices rather than iteration for this
            let o1 = obj1_slice[i];
            let o2 = obj2_slice[i];
            
            // write to out_val direclty, more c-like
            *out_val = factor * o1 * o2 * (o1 + o2);
        });

    // for (i, (&o1, &o2)) in obj1_slice.par_iter().zip(obj2_slice).enumerate() {
    //     out_slice[i] = factor * o1 * o2 * (o1 + o2);
    // };

    out_arr
}

#[pyfunction]
pub fn beta_sgl(d1: f64, d2: f64) -> f64 {
    let factor = 12.8 * G.powi(3) * C_LIGHT.powf(-5.0);
    factor * d1 * d2 * (d1 + d2)
}

#[pyfunction]
pub fn peters_ecc_const_sgl(ecc: f64) -> f64 {
    (1.0 - ecc.powi(2)) / 
    (
        ecc.powf(12.0/19.0) * (1.0 + (121.0 / 304.0) * ecc.powi(2)).powf(870.0/2299.0)
    )
}

#[pyfunction]
pub fn peters_ecc_const_arr<'py>(
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
pub fn peters_ecc_integrand_sgl(ecc: f64) -> f64 {
    ecc.powf(29.0/19.0) * (1.0 + (121.0/304.0) * ecc.powi(2)).powf(1181.0/2299.0) * (1.0 - ecc.powi(2)).powf(-3.0/2.0)
    //  pow(ecc,29./19.) * pow(1 + (121./304.) * pow(ecc,2),1181./2299.) * pow(1 - pow(ecc,2), -3./2.)
}

// gets us reliably 1% slower than C
// interesting
// maybe because this one's way heavier on the powf??

#[pyfunction]
pub fn peters_ecc_integrand_arr<'py>(
    py: Python<'py>,
    eccs: PyReadonlyArray1<'py, f64>
) -> Bound<'py, PyArray1<f64>>  {
    assert!(!eccs.is_empty().unwrap());

    let ecc_slice = eccs.as_slice().unwrap();

    let out_arr = unsafe{ PyArray1::new(py, ecc_slice.len(), false)};
    let out_slice = unsafe {out_arr.as_slice_mut().unwrap()};

    for (i, &ecc) in ecc_slice.iter().enumerate() {
        out_slice[i] = ecc.powf(29.0/19.0) * (1.0 + (121.0/304.0) * ecc.powi(2)).powf(1181.0/2299.0) * (1.0 - ecc.powi(2)).powf(-3.0/2.0)
    };
    
    out_arr



    // eccs.iter().map(|ecc| {
    //     ecc.powf(29.0/19.0) * (1.0 + (121.0/304.0) * ecc.powi(2)).powf(1181.0/2299.0) * (1.0 - ecc.powi(2)).powf(-3.0/2.0)
    //     // *out_ptr = pow(*ecc_ptr,29./19.) * pow(1 + (121./304.) * pow(*ecc_ptr,2),1181./2299.) * pow(1 - pow(*ecc_ptr,2), -3./2.);
    // }).collect()
}

// now let's see how we can optimize this one
#[pyfunction]
pub fn merge_time_circ_arr<'py>(
    py: Python<'py>,
    m1_arr: PyReadonlyArray1<'py, f64>,
    m2_arr: PyReadonlyArray1<'py, f64>,
    a_arr: PyReadonlyArray1<'py, f64>
    // m1_arr: Vec<f64>, 
    // m2_arr: Vec<f64>, 
    // a_arr: Vec<f64>
// ) -> Vec<f64> {
) -> Bound<'py, PyArray1<f64>>  {
    let beta_factor = 12.8 * G.powi(3) * C_LIGHT.powf(-5.0);

    assert!(!m1_arr.is_empty().unwrap());
    let npts = m1_arr.len().unwrap();
    assert!(m2_arr.len().unwrap() == npts);
    assert!(a_arr.len().unwrap() == npts);

    let m1_slice = m1_arr.as_slice().unwrap();
    let m2_slice = m2_arr.as_slice().unwrap();
    let a_slice = a_arr.as_slice().unwrap();

    let out_arr = unsafe{ PyArray1::new(py, m1_slice.len(), false)};
    let out_slice = unsafe {out_arr.as_slice_mut().unwrap()};

    for (i, ((m1, m2), a)) in m1_slice.iter().zip(m2_slice).zip(a_slice).enumerate() {
        let beta = beta_factor * m1 * m2 * (m1 + m2);
        
        out_slice[i] = (a.powi(2)).powi(2) / (4.0 * beta)
    };
    
    out_arr

    // m1_arr.iter().zip(m2_arr).zip(a_arr).map(|((m1, m2), a)| {
    //     let beta = beta_factor * m1 * m2 * (m1 + m2);
    //
    //     (a.powi(2)).powi(2) / (4.0 * beta)
    //     // *out_ptr = pow(pow(*a0_ptr, 2),2) / (4 * beta);
    // }).collect()
}

#[pyfunction]
pub fn merge_time_circ_sgl(m1: f64, m2: f64, a: f64) -> f64 {
    let beta_factor = 12.8 * G.powi(3) * C_LIGHT.powf(-5.0);
    let beta = beta_factor * m1 * m2 * (m1 + m2);
    (a.powi(2)).powi(2) / (4.0 * beta)
}

#[pyfunction]
pub fn orb_sep_evol_circ_arr<'py>(
    py: Python<'py>,
    m1_arr: PyReadonlyArray1<'py, f64>,
    m2_arr: PyReadonlyArray1<'py, f64>,
    a0_arr: PyReadonlyArray1<'py, f64>,
    t_arr: PyReadonlyArray1<'py, f64>
    // m1_arr: Vec<f64>, 
    // m2_arr: Vec<f64>, 
    // a0_arr: Vec<f64>,
    // t_arr: Vec<f64>
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

    // m1_arr.iter().zip(m2_arr).zip(a0_arr).zip(t_arr)
    //     .map(|(((m1, m2), a0), t)| { 
    //         let beta = beta_factor * m1 * m2 * (m1 + m2);
    //         (a0.powi(2).powi(2) - (4.0 * beta * t)).sqrt().sqrt()
    //     }).collect()
}

#[pyfunction]
pub fn orb_sep_evol_circ_sgl(m1: f64, m2: f64, a0: f64, t: f64) -> f64 {
    let beta_factor = 12.8 * G.powi(3) * C_LIGHT.powf(-5.0);

    let beta = beta_factor * m1 * m2 * (m1 + m2);
    (a0.powi(2).powi(2) - (4.0 * beta * t)).sqrt().sqrt()
}

#[pyfunction]
pub fn orb_sep_evol_ecc_integrand_arr<'py>(
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
        // holy number soup batman
        // out_slice[i] = preamble * (ecc / 
        //
        //     (c0 * (ecc.powf(12.0/19.0) * (1.0 + 0.3980263157894737 * ecc_sq).powf(0.3784253988664629) / (1.0 - ecc_sq) )).powi(4)
        // ) * (
        //     1.0 + 0.3980263157894737 * ecc_sq
        // ) / (1.0 - ecc_sq).powf(2.5);

        let sep = c0 / peters_ecc_const_sgl(ecc);
        out_slice[i] = preamble * (ecc/sep.powi(4)) * (1.0 + (121.0/304.0) * ecc.powi(2)) / (1.0 - ecc.powi(2)).powf(2.5);
    }
// double ecc_sq = pow(*ecc_ptr,2);
//         *out_ptr = preamble * (*ecc_ptr/pow(pow(
//                 c0 * (pow(*ecc_ptr,12./19.) * pow(1. + (0.3980263157894737) * ecc_sq, 0.3784253988664629)) / (1. - ecc_sq),2),2)
//             ) * 
//             (1. + (0.3980263157894737)*ecc_sq) / pow(1. - ecc_sq,2.5);

    out_arr
}

#[pyfunction]
pub fn orb_sep_evol_ecc_integrand_sgl(
    preamble: f64, 
    c0: f64,
    ecc: f64, 
) -> f64 {
    let sep = c0 / peters_ecc_const_sgl(ecc);
    preamble * (ecc/sep.powi(4)) * (1.0 + (121.0/304.0) * ecc.powi(2)) / (1.0 - (ecc).powi(2)).powf(2.5)
}
