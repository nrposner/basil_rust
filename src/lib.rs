mod coordinates;
mod decay;
mod dwd;
mod gw;
mod kepler;
mod spin;
mod tides;

use pyo3::prelude::*;
use decay::*;
use dwd::*;
use gw::*;
use kepler::*;
use coordinates::*;
use spin::*;
use tides::*;

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

    m.add_function(wrap_pyfunction!(orbital_period_of_m1_m2_a_arr, m)?)?;

    m.add_function(wrap_pyfunction!(dwd_r_of_m, m)?)?;
    m.add_function(wrap_pyfunction!(dwd_rlof_a_of_m1_m2_r1_r2, m)?)?;
    m.add_function(wrap_pyfunction!(dwd_rlof_p_of_m1_m2_r1_r2, m)?)?;

    m.add_function(wrap_pyfunction!(mc_of_m1_m2, m)?)?;
    m.add_function(wrap_pyfunction!(eta_of_m1_m2, m)?)?;
    m.add_function(wrap_pyfunction!(mc_and_eta_of_m1_m2, m)?)?;
    m.add_function(wrap_pyfunction!(m_of_mc_eta, m)?)?;
    m.add_function(wrap_pyfunction!(m1_of_m_eta, m)?)?;
    m.add_function(wrap_pyfunction!(m2_of_m_eta, m)?)?;
    m.add_function(wrap_pyfunction!(source_of_detector, m)?)?;
    m.add_function(wrap_pyfunction!(detector_of_source, m)?)?;

    m.add_function(wrap_pyfunction!(lambda_tilde_of_eta_lambda1_lambda2, m)?)?;
    m.add_function(wrap_pyfunction!(delta_lambda_of_eta_lambda1_lambda2, m)?)?;

    // these two are numerically unstable
    m.add_function(wrap_pyfunction!(lambda1_of_eta_lambda_tilde_delta_lambda, m)?)?;
    m.add_function(wrap_pyfunction!(lambda2_of_eta_lambda_tilde_delta_lambda, m)?)?;

    m.add_function(wrap_pyfunction!(chieff_of_m1_m2_chi1z_chi2z, m)?)?;
    m.add_function(wrap_pyfunction!(chiminus_of_m1_m2_chi1z_chi2z, m)?)?;
    m.add_function(wrap_pyfunction!(chi1z_of_m1_m2_chieff_chiminus, m)?)?;
    m.add_function(wrap_pyfunction!(chi2z_of_m1_m2_chieff_chiminus, m)?)?;

    // gw
    m.add_function(wrap_pyfunction!(beta, m)?)?;
    m.add_function(wrap_pyfunction!(orbital_separation_evolve, m)?)?;
    m.add_function(wrap_pyfunction!(time_of_orbital_shrinkage, m)?)?;
    m.add_function(wrap_pyfunction!(time_to_merge_of_m1_m2_a0, m)?)?;
    m.add_function(wrap_pyfunction!(orbital_period_evolved_gw, m)?)?;

    Ok(())
}
