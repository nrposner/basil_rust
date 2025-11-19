import time
import numpy as np
import polars as pl
from typing import List, Callable, Any, Tuple, Dict

# --- IMPORTS (As provided) ---
from basil_core.astro.orbit._decay import _orb_sep_evol_ecc_integrand_arr as orb_c # ty: ignore
from basil_core.astro.orbit._decay import _beta_arr as beta_c # ty: ignore
from basil_core.astro.orbit._decay import _peters_ecc_const_arr as peters_c # ty: ignore
from basil_core.astro.orbit._decay import _peters_ecc_integrand_arr as peters_int_c # ty: ignore
from basil_core.astro.orbit._decay import _merge_time_circ_arr as merge_c # ty: ignore
from basil_core.astro.orbit._decay import _orb_sep_evol_circ_arr as evol_c # ty: ignore
from basil_core.astro.orbit._kepler import _orbital_period_of_m1_m2_a_arr as kepler_c # ty: ignore

from basil_core.astro.orbit._DWD_RLOF import _DWD_r_of_m as dwd_r_c # ty: ignore
from basil_core.astro.orbit._DWD_RLOF import _DWD_RLOF_a_of_m1_m2_r1_r2 as dwd_a_c # ty: ignore
from basil_core.astro.orbit._DWD_RLOF import _DWD_RLOF_P_of_m1_m2_r1_r2 as dwd_p_c # ty: ignore

from basil_core.astro.coordinates._coordinates import _mc_of_m1_m2 as mc_c # ty: ignore
from basil_core.astro.coordinates._coordinates import _eta_of_m1_m2 as eta_c # ty: ignore
from basil_core.astro.coordinates._coordinates import _M_of_mc_eta as m_of_mc_eta_c # ty: ignore
from basil_core.astro.coordinates._coordinates import _m1_of_M_eta as m1_of_m_eta_c # ty: ignore
from basil_core.astro.coordinates._coordinates import _m2_of_M_eta as m2_of_m_eta_c # ty: ignore
from basil_core.astro.coordinates._coordinates import _detector_of_source as detector_of_source_c # ty: ignore
from basil_core.astro.coordinates._coordinates import _source_of_detector as source_of_detector_c # ty: ignore

from basil_core.astro.coordinates._tides import _lambda_tilde_of_eta_lambda1_lambda2 as ltell_c # ty: ignore
from basil_core.astro.coordinates._tides import _delta_lambda_of_eta_lambda1_lambda2 as dlell_c # ty: ignore
from basil_core.astro.coordinates._tides import _lambda1_of_eta_lambda_tilde_delta_lambda as l1eltdl_c # ty: ignore
from basil_core.astro.coordinates._tides import _lambda2_of_eta_lambda_tilde_delta_lambda as l2eltdl_c # ty: ignore

from basil_core.astro.coordinates._spin import _chieff_of_m1_m2_chi1z_chi2z as chieff_c # ty: ignore
from basil_core.astro.coordinates._spin import _chiMinus_of_m1_m2_chi1z_chi2z as chiminus_c # ty: ignore
from basil_core.astro.coordinates._spin import _chi1z_of_m1_m2_chieff_chiMinus as chi1z_c # ty: ignore
from basil_core.astro.coordinates._spin import _chi2z_of_m1_m2_chieff_chiMinus as chi2z_c # ty: ignore

# Rust Imports
from basil import orb_sep_evol_ecc_integrand_arr as orb_rust # ty: ignore
from basil import beta_arr as beta_rust # ty: ignore
from basil import peters_ecc_const_arr as peters_rust # ty: ignore
from basil import peters_ecc_integrand_arr as peters_int_rust # ty: ignore
from basil import merge_time_circ_arr as merge_rust # ty: ignore
from basil import orb_sep_evol_circ_arr as evol_rust # ty: ignore
from basil import orbital_period_of_m1_m2_a_arr as kepler_rust # ty: ignore
from basil import dwd_r_of_m as dwd_r_rust # ty: ignore
from basil import dwd_rlof_a_of_m1_m2_r1_r2 as dwd_a_rust # ty: ignore
from basil import dwd_rlof_p_of_m1_m2_r1_r2 as dwd_p_rust # ty: ignore
from basil import mc_of_m1_m2 as mc_rust # ty: ignore
from basil import eta_of_m1_m2 as eta_rust # ty: ignore
from basil import mc_and_eta_of_m1_m2 as mc_eta_rust # ty: ignore

from basil import m_of_mc_eta as m_of_mc_eta_rust # ty: ignore
from basil import m1_of_m_eta as m1_of_m_eta_rust # ty: ignore
from basil import m2_of_m_eta as m2_of_m_eta_rust # ty: ignore
from basil import source_of_detector as source_of_detector_rust # ty: ignore
from basil import detector_of_source as detector_of_source_rust # ty: ignore

from basil import lambda_tilde_of_eta_lambda1_lambda2 as ltell_rust # ty: ignore
from basil import delta_lambda_of_eta_lambda1_lambda2 as dlell_rust # ty: ignore
from basil import lambda1_of_eta_lambda_tilde_delta_lambda as l1eltdl_rust # ty: ignore
from basil import lambda2_of_eta_lambda_tilde_delta_lambda as l2eltdl_rust # ty: ignore

from basil import chieff_of_m1_m2_chi1z_chi2z as chieff_rust # ty: ignore
from basil import chiminus_of_m1_m2_chi1z_chi2z as chiminus_rust # ty: ignore
from basil import chi1z_of_m1_m2_chieff_chiminus as chi1z_rust # ty: ignore
from basil import chi2z_of_m1_m2_chieff_chiminus as chi2z_rust # ty: ignore

# Global configuration
TEST_ITERS = 10000
PREAMBLE = 0.234
C0 = 0.432

# --- HARNESS ---

def check_equality(res_c, res_rust):
    """
    Helper to check equality, handling tuple returns (like mc_and_eta) 
    and NaN equality.
    """
    if isinstance(res_c, tuple) and isinstance(res_rust, tuple):
        if len(res_c) != len(res_rust):
            return False
        return all(np.allclose(c, r, equal_nan=True) for c, r in zip(res_c, res_rust))
    
    return np.allclose(res_c, res_rust, equal_nan=True)

def run_benchmark(
    function_name: str,
    c_func: Callable,
    rust_func: Callable,
    input_generator: Callable[[int], Tuple],
    sizes: List[int],
    test_iters: int = TEST_ITERS
) -> List[Dict[str, Any]]:
    
    print(f"Benchmarking {function_name}...")
    results = []

    for size in sizes:
        c_times = []
        rust_times = []
        passed_checks = True

        for _ in range(test_iters):
            # Generate inputs
            # Note: We explicitly do NOT time input generation
            args = input_generator(size)

            # Rust Timing
            start_time = time.perf_counter_ns()
            rust_result = rust_func(*args)
            rust_times.append(time.perf_counter_ns() - start_time)

            # C Timing
            start_time = time.perf_counter_ns()
            c_result = c_func(*args)
            c_times.append(time.perf_counter_ns() - start_time)

            # Equality Check
            # If it fails once, we mark the whole size batch as failed, 
            # but we continue benchmarking to get performance data.
            if passed_checks:
                if not check_equality(c_result, rust_result):
                    passed_checks = False

        # Aggregation
        avg_c = np.mean(c_times)
        avg_rust = np.mean(rust_times)
        
        results.append({
            "function_name": function_name,
            "array_size": size,
            "c_runtime_ns_total": np.sum(c_times),
            "rust_runtime_ns_total": np.sum(rust_times),
            "c_ns_per_element": avg_c / size,
            "rust_ns_per_element": avg_rust / size,
            "speedup_factor": avg_c / avg_rust if avg_rust > 0 else 0.0,
            "passed_equality_check": passed_checks
        })
        
    return results

# --- INPUT GENERATORS ---

def gen_1_arr(size):
    return (np.random.rand(size),)

def gen_2_arr(size):
    return (np.random.rand(size), np.random.rand(size))

def gen_3_arr(size):
    return (np.random.rand(size), np.random.rand(size), np.random.rand(size))

def gen_4_arr(size):
    return (np.random.rand(size), np.random.rand(size), np.random.rand(size), np.random.rand(size))

def gen_3_arr_div10(size):
    # Specifically for tides functions that used / 10
    return (np.random.rand(size)/10, np.random.rand(size)/10, np.random.rand(size)/10)

def gen_3_arr_clipped(size):
    # Specifically for lambda1 stability checks
    return (
        np.clip(np.random.rand(size), 0.01, 0.24),
        np.clip(np.random.rand(size), 0.01, 0.24),
        np.clip(np.random.rand(size), 0.01, 0.24)
    )

def gen_orb(size):
    # Takes constants preamble, c0, then array
    return (PREAMBLE, C0, np.random.rand(size))

# --- MAIN ---

def main():
    all_results = []
    sizes = [10000]
    # sizes = [500, 1000, 5000, 10000]
    
    # List of benchmarks to run
    # Format: (Name, C_Func, Rust_Func, Input_Generator)
    benchmarks = [
        ("beta_arr", beta_c, beta_rust, gen_2_arr),
        ("orb_sep_evol_circ_arr", evol_c, evol_rust, gen_4_arr),
        ("peters_ecc_const_arr", peters_c, peters_rust, gen_1_arr),
        ("peters_ecc_integrand_arr", peters_int_c, peters_int_rust, gen_1_arr),
        ("merge_time_circ_arr", merge_c, merge_rust, gen_3_arr),
        ("orb_sep_evol_ecc_integrand_arr", orb_c, orb_rust, gen_orb),
        ("orbital_period_of_m1_m2_a_arr", kepler_c, kepler_rust, gen_3_arr),
        ("dwd_r_arr", dwd_r_c, dwd_r_rust, gen_1_arr),
        ("dwd_a_arr", dwd_a_c, dwd_a_rust, gen_4_arr),
        ("dwd_p_arr", dwd_p_c, dwd_p_rust, gen_4_arr),
        ("mc_of_m1_m2", mc_c, mc_rust, gen_2_arr),
        ("eta_of_m1_m2", eta_c, eta_rust, gen_2_arr),
        
        # mc_and_eta is special: C requires two calls, Rust requires one. 
        # We wrap C to match Rust's tuple output.
        (
            "mc_and_eta_of_m1_m2", 
            lambda x, y: (mc_c(x, y), eta_c(x, y)), 
            mc_eta_rust, 
            gen_2_arr
        ),
        
        ("m_of_mc_eta", m_of_mc_eta_c, m_of_mc_eta_rust, gen_2_arr),
        ("m1_of_m_eta", m1_of_m_eta_c, m1_of_m_eta_rust, gen_2_arr),
        ("m2_of_m_eta", m2_of_m_eta_c, m2_of_m_eta_rust, gen_2_arr),
        ("source_of_detector", source_of_detector_c, source_of_detector_rust, gen_2_arr),
        ("detector_of_source", detector_of_source_c, detector_of_source_rust, gen_2_arr),
        ("lambda_tilde_of_eta_lambda1_lambda2", ltell_c, ltell_rust, gen_3_arr_div10),
        ("delta_lambda_of_eta_lambda1_lambda2", dlell_c, dlell_rust, gen_3_arr_div10),
        
        # Unstable functions included
        ("lambda1_of_eta_lambda_tilde_delta_lambda", l1eltdl_c, l1eltdl_rust, gen_3_arr_clipped),
        ("lambda2_of_eta_lambda_tilde_delta_lambda", l2eltdl_c, l2eltdl_rust, gen_3_arr_div10),
        
        ("chieff_of_m1_m2_chi1z_chi2z", chieff_c, chieff_rust, gen_4_arr),
        ("chiMinus_of_m1_m2_chi1z_chi2z", chiminus_c, chiminus_rust, gen_4_arr),
        ("chi1z_of_m1_m2_chieff_chiMinus", chi1z_c, chi1z_rust, gen_4_arr),
        ("chi2z_of_m1_m2_chieff_chiMinus", chi2z_c, chi2z_rust, gen_4_arr),
    ]

    # Execution Loop
    for name, c_func, r_func, generator in benchmarks:
        data = run_benchmark(name, c_func, r_func, generator, sizes)
        all_results.extend(data)

    # Create DataFrame
    df = pl.DataFrame(all_results)
    
    # Configuration for pretty printing
    pl.Config.set_tbl_rows(100)
    pl.Config.set_tbl_cols(10)
    print("\n=== Benchmark Results ===\n")
    print(df)

    df.write_csv("benchmark_csv")
    
    # Optional: Verify unstable functions were caught correctly
    failed = df.filter(pl.col("passed_equality_check") == False)
    if not failed.is_empty():
        print("\n=== Functions with Numerical Instabilities (Equality Check Failed) ===")
        print(failed.select(["function_name", "array_size", "passed_equality_check"]))

if __name__ == "__main__":
    main()
