use pyo3::prelude::*;
use numpy::{PyArray1, PyArrayMethods, PyReadonlyArray1};

#[pyfunction]
pub fn lambda_tilde_of_eta_lambda1_lambda2<'py>(
    py: Python<'py>,
    eta_arr: PyReadonlyArray1<'py, f64>,
    lambda1_arr: PyReadonlyArray1<'py, f64>,
    lambda2_arr: PyReadonlyArray1<'py, f64>,
) -> Bound<'py, PyArray1<f64>> {

    assert!(!eta_arr.is_empty().unwrap());
    assert!(lambda1_arr.len().unwrap() == eta_arr.len().unwrap());
    assert!(lambda2_arr.len().unwrap() == eta_arr.len().unwrap());

    let eta_slice = eta_arr.as_slice().unwrap();
    let lambda1_slice = lambda1_arr.as_slice().unwrap();
    let lambda2_slice = lambda2_arr.as_slice().unwrap();

    let out_arr = unsafe{ PyArray1::new(py, eta_slice.len(), false)};
    let out_slice = unsafe {out_arr.as_slice_mut().unwrap()};

    for (i, ((eta, lambda1), lambda2)) in eta_slice.iter().zip(lambda1_slice).zip(lambda2_slice).enumerate() {
        let eta2 = eta.powi(2);

        out_slice[i] = (8.0/13.0)*(((1.0 + (7.0*eta) - (31.0*eta2))*(lambda1 + lambda2)) +
                ((1.0 - (4.0*eta)).sqrt() * (1.0 + (9.0*eta) - (11.0*eta2))*(lambda1-lambda2)));
    }
    out_arr
}

#[pyfunction]
pub fn delta_lambda_of_eta_lambda1_lambda2<'py>(
    py: Python<'py>,
    eta_arr: PyReadonlyArray1<'py, f64>,
    lambda1_arr: PyReadonlyArray1<'py, f64>,
    lambda2_arr: PyReadonlyArray1<'py, f64>,
) -> Bound<'py, PyArray1<f64>> {

    assert!(!eta_arr.is_empty().unwrap());
    assert!(lambda1_arr.len().unwrap() == eta_arr.len().unwrap());
    assert!(lambda2_arr.len().unwrap() == eta_arr.len().unwrap());

    let eta_slice = eta_arr.as_slice().unwrap();
    let lambda1_slice = lambda1_arr.as_slice().unwrap();
    let lambda2_slice = lambda2_arr.as_slice().unwrap();

    let out_arr = unsafe{ PyArray1::new(py, eta_slice.len(), false)};
    let out_slice = unsafe {out_arr.as_slice_mut().unwrap()};

    for (i, ((eta, lambda1), lambda2)) in eta_slice.iter().zip(lambda1_slice).zip(lambda2_slice).enumerate() {
        let eta2 = eta.powi(2);
        let eta3 = eta.powi(3);

        out_slice[i] = 0.5 * ( 
            (1.-4.*eta).sqrt() * 
            ((1.0 + ((-13272.0 * eta + 8944.0 * eta2)/1319.0))*(lambda1 + lambda2)) + 
            (1.0 + (-15910.0*eta + 32850.0*eta2 + 3380.*eta3)/1319.0)*(lambda1 - lambda2));
    }
    out_arr
}


#[pyfunction]
pub fn lambda1_of_eta_lambda_tilde_delta_lambda<'py>(
    py: Python<'py>,
    eta_arr: PyReadonlyArray1<'py, f64>,
    lambda_tilde_arr: PyReadonlyArray1<'py, f64>,
    delta_lambda_arr: PyReadonlyArray1<'py, f64>,
) -> Bound<'py, PyArray1<f64>> {

    assert!(!eta_arr.is_empty().unwrap());
    assert!(lambda_tilde_arr.len().unwrap() == eta_arr.len().unwrap());
    assert!(delta_lambda_arr.len().unwrap() == eta_arr.len().unwrap());

    let eta_slice = eta_arr.as_slice().unwrap();
    let lambda_tilde_slice = lambda_tilde_arr.as_slice().unwrap();
    let delta_lambda_slice = delta_lambda_arr.as_slice().unwrap();

    let out_arr = unsafe{ PyArray1::new(py, eta_slice.len(), false)};
    let out_slice = unsafe {out_arr.as_slice_mut().unwrap()};

    for (i, ((eta, lambda_tilde), delta_lambda)) in eta_slice.iter().zip(lambda_tilde_slice).zip(delta_lambda_slice).enumerate() {
        let eta2 = eta.powi(2);
        let eta3 = eta.powi(3);
        let determinant = (1.0 - 4.0 * eta).sqrt();

        let a = (8./13.)*(1. + 7.*eta - 31.*eta2);
        let b = (8./13.)*determinant*(1. + 9.*eta - 11.*eta2);
        let c = 0.5*determinant*(1. + (-13272.*eta + 8944.0*eta2)/1319.0);
        let d = 0.5*(1. + (-15910.*eta + 32850.*eta2 + 3380.*eta3)/1319.0);

        // this could potentially resolve the discrepancy if 
        // it was also included in the C version?
        // but at present, no solution
        let den = 2.0 * (b * c - a * d);
        // let den = ((a+b)*(c-d)) - ((a-b)*(c+d));
        
        out_slice[i] = ( (c - d) * lambda_tilde - (a - b) * delta_lambda ) / den;
    }
    out_arr
}



#[pyfunction]
pub fn lambda2_of_eta_lambda_tilde_delta_lambda<'py>(
    py: Python<'py>,
    eta_arr: PyReadonlyArray1<'py, f64>,
    lambda_tilde_arr: PyReadonlyArray1<'py, f64>,
    delta_lambda_arr: PyReadonlyArray1<'py, f64>,
) -> Bound<'py, PyArray1<f64>> {

    assert!(!eta_arr.is_empty().unwrap());
    assert!(lambda_tilde_arr.len().unwrap() == eta_arr.len().unwrap());
    assert!(delta_lambda_arr.len().unwrap() == eta_arr.len().unwrap());

    let eta_slice = eta_arr.as_slice().unwrap();
    let lambda_tilde_slice = lambda_tilde_arr.as_slice().unwrap();
    let delta_lambda_slice = delta_lambda_arr.as_slice().unwrap();

    let out_arr = unsafe{ PyArray1::new(py, eta_slice.len(), false)};
    let out_slice = unsafe {out_arr.as_slice_mut().unwrap()};

    for (i, ((eta, lambda_tilde), delta_lambda)) in eta_slice.iter().zip(lambda_tilde_slice).zip(delta_lambda_slice).enumerate() {
        let eta2 = eta.powi(2);
        let eta3 = eta.powi(3);
        let determinant = (1.0 - 4.0 * eta).sqrt();

        let a = (8./13.)*(1. + 7.*eta - 31.*eta2);
        let b = (8./13.)*determinant*(1. + 9.*eta - 11.*eta2);
        let c = 0.5*determinant*(1. + (-13272.*eta + 8944.0*eta2)/1319.0);
        let d = 0.5*(1. + (-15910.*eta + 32850.*eta2 + 3380.*eta3)/1319.0);

        let den = ((a+b)*(c-d)) - ((a-b)*(c+d));
        
        out_slice[i] = (-(c+d)*lambda_tilde + (a+b)*delta_lambda )/den;
    }
    out_arr
}
