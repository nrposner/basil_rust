import time
import numpy as np

from basil_core.astro.orbit._decay import _orb_sep_evol_ecc_integrand_arr as orb_c # ty: ignore[unresolved-import]
from basil_core.astro.orbit._decay import _beta_arr as beta_c # ty: ignore[unresolved-import]
from basil_core.astro.orbit._decay import _peters_ecc_const_arr as peters_c # ty: ignore[unresolved-import]
from basil_core.astro.orbit._decay import _peters_ecc_integrand_arr as peters_int_c # ty: ignore[unresolved-import]
from basil_core.astro.orbit._decay import _merge_time_circ_arr as merge_c # ty: ignore[unresolved-import]
from basil_core.astro.orbit._decay import _orb_sep_evol_circ_arr as evol_c # ty: ignore[unresolved-import]
from basil_core.astro.orbit._kepler import _orbital_period_of_m1_m2_a_arr as kepler_c # ty: ignore[unresolved-import]

from basil_core.astro.orbit._DWD_RLOF import _DWD_r_of_m as dwd_r_c # ty: ignore[unresolved-import]
from basil_core.astro.orbit._DWD_RLOF import _DWD_RLOF_a_of_m1_m2_r1_r2 as dwd_a_c # ty: ignore[unresolved-import]
from basil_core.astro.orbit._DWD_RLOF import _DWD_RLOF_P_of_m1_m2_r1_r2 as dwd_p_c # ty: ignore[unresolved-import]

from basil_core.astro.coordinates._coordinates import _mc_of_m1_m2 as mc_c # ty: ignore[unresolved-import]
from basil_core.astro.coordinates._coordinates import _eta_of_m1_m2 as eta_c # ty: ignore[unresolved-import]
from basil_core.astro.coordinates._coordinates import _M_of_mc_eta as m_of_mc_eta_c # ty: ignore[unresolved-import]
from basil_core.astro.coordinates._coordinates import _m1_of_M_eta as m1_of_m_eta_c # ty: ignore[unresolved-import]
from basil_core.astro.coordinates._coordinates import _m2_of_M_eta as m2_of_m_eta_c # ty: ignore[unresolved-import]
from basil_core.astro.coordinates._coordinates import _detector_of_source as detector_of_source_c # ty: ignore[unresolved-import]
from basil_core.astro.coordinates._coordinates import _source_of_detector as source_of_detector_c # ty: ignore[unresolved-import]

from basil_core.astro.coordinates._tides import _lambda_tilde_of_eta_lambda1_lambda2 as ltell_c # ty: ignore[unresolved-import]
from basil_core.astro.coordinates._tides import _delta_lambda_of_eta_lambda1_lambda2 as dlell_c # ty: ignore[unresolved-import]
from basil_core.astro.coordinates._tides import _lambda1_of_eta_lambda_tilde_delta_lambda as l1eltdl_c # ty: ignore[unresolved-import]
from basil_core.astro.coordinates._tides import _lambda2_of_eta_lambda_tilde_delta_lambda as l2eltdl_c # ty: ignore[unresolved-import]



from basil import orb_sep_evol_ecc_integrand_arr as orb_rust # ty: ignore[unresolved-import]
from basil import beta_arr as beta_rust # ty: ignore[unresolved-import]
from basil import peters_ecc_const_arr as peters_rust # ty: ignore[unresolved-import]
from basil import peters_ecc_integrand_arr as peters_int_rust # ty: ignore[unresolved-import]
from basil import merge_time_circ_arr as merge_rust # ty: ignore[unresolved-import]
from basil import orb_sep_evol_circ_arr as evol_rust # ty: ignore[unresolved-import]
from basil import orbital_period_of_m1_m2_a_arr as kepler_rust # ty: ignore[unresolved-import] 
from basil import dwd_r_of_m as dwd_r_rust # ty: ignore[unresolved-import] 
from basil import dwd_rlof_a_of_m1_m2_r1_r2 as dwd_a_rust # ty: ignore[unresolved-import] 
from basil import dwd_rlof_p_of_m1_m2_r1_r2 as dwd_p_rust # ty: ignore[unresolved-import] 
from basil import mc_of_m1_m2 as mc_rust # ty: ignore[unresolved-import] 
from basil import eta_of_m1_m2 as eta_rust # ty: ignore[unresolved-import] 
from basil import mc_and_eta_of_m1_m2 as mc_eta_rust # ty: ignore[unresolved-import] 

from basil import m_of_mc_eta as m_of_mc_eta_rust # ty: ignore[unresolved-import] 
from basil import m1_of_m_eta as m1_of_m_eta_rust # ty: ignore[unresolved-import] 
from basil import m2_of_m_eta as m2_of_m_eta_rust # ty: ignore[unresolved-import] 
from basil import source_of_detector as source_of_detector_rust # ty: ignore[unresolved-import] 
from basil import detector_of_source as detector_of_source_rust # ty: ignore[unresolved-import] 

# tides
from basil import lambda_tilde_of_eta_lambda1_lambda2 as ltell_rust # ty: ignore[unresolved-import]
from basil import delta_lambda_of_eta_lambda1_lambda2 as dlell_rust # ty: ignore[unresolved-import]
from basil import lambda1_of_eta_lambda_tilde_delta_lambda as l1eltdl_rust # ty: ignore[unresolved-import]
from basil import lambda2_of_eta_lambda_tilde_delta_lambda as l2eltdl_rust # ty: ignore[unresolved-import]

# test_iters = 1000
preamble = 0.234
c0 = 0.432


# this is NUMERICALLY UNSTABLE
# GCC and LLVM handle the instability differently
# we cannot guarantee the same answers to within floating-point precision here
def benchmark_l2eltdl(size: int, test_iters: int = 1000) -> tuple[list[float], list[float]]:
    c_times = []
    rust_times = []

    # generate a random numpy array of size `size`
    for i in range(test_iters):
        input1 = np.random.rand(size) / 10
        input2 = np.random.rand(size) / 10
        input3 = np.random.rand(size) / 10

        assert not np.allclose(input1, input2)

        start_time = time.perf_counter_ns()
        rust_result = l2eltdl_rust(input1, input2, input3)
        rust_time = time.perf_counter_ns() - start_time
        rust_times.append(rust_time)

        start_time = time.perf_counter_ns()
        c_result = l2eltdl_c(input1, input2, input3)
        c_time = time.perf_counter_ns() - start_time
        c_times.append(c_time)

        assert np.allclose(c_result, rust_result), \
            "C and rust results do not match"

    return (c_times, rust_times)


# this is NUMERICALLY UNSTABLE
# GCC and LLVM handle the instability differently
# we cannot guarantee the same answers to within floating-point precision here
def benchmark_l1eltdl(size: int, test_iters: int = 1000) -> tuple[list[float], list[float]]:
    c_times = []
    rust_times = []

    # generate a random numpy array of size `size`
    for i in range(test_iters):
        input1 = np.clip(np.random.rand(size), 0.01, 0.24)
        input2 = np.clip(np.random.rand(size), 0.01, 0.24)
        input3 = np.clip(np.random.rand(size), 0.01, 0.24)
        # input2 = np.random.rand(size)
        # input3 = np.random.rand(size)

        assert not np.allclose(input1, input2)

        start_time = time.perf_counter_ns()
        rust_result = l1eltdl_rust(input1, input2, input3)
        rust_time = time.perf_counter_ns() - start_time
        rust_times.append(rust_time)

        start_time = time.perf_counter_ns()
        c_result = l1eltdl_c(input1, input2, input3)
        c_time = time.perf_counter_ns() - start_time
        c_times.append(c_time)

        # print(f"dimension of c_result: ", c_result.shape)
        # print(f"dimension of rust_result: ", rust_result.shape)
        # print(c_result[0:10])
        # print(rust_result[0:10])

        # if there are any places where these are not equal, give us
        # the array location and the values

        # bools = np.isclose(c_result, rust_result, equal_nan=True)
        # inds = [i for i, x in enumerate(bools) if not x]
        # for ind in inds:
        #     print("C: ", c_result[ind], "Rust: ", rust_result[ind])

        assert np.allclose(c_result, rust_result, equal_nan=True), \
            "C and rust results do not match"

    return (c_times, rust_times)

def benchmark_dlell(size: int, test_iters: int = 1000) -> tuple[list[float], list[float]]:
    c_times = []
    rust_times = []

    # generate a random numpy array of size `size`
    for i in range(test_iters):
        input1 = np.random.rand(size) / 10
        input2 = np.random.rand(size) / 10
        input3 = np.random.rand(size) / 10

        assert not np.allclose(input1, input2)

        start_time = time.perf_counter_ns()
        rust_result = dlell_rust(input1, input2, input3)
        rust_time = time.perf_counter_ns() - start_time
        rust_times.append(rust_time)

        start_time = time.perf_counter_ns()
        c_result = dlell_c(input1, input2, input3)
        c_time = time.perf_counter_ns() - start_time
        c_times.append(c_time)

        assert np.allclose(c_result, rust_result), \
            "C and rust results do not match"

    return (c_times, rust_times)


def benchmark_ltell(size: int, test_iters: int = 1000) -> tuple[list[float], list[float]]:
    c_times = []
    rust_times = []

    # generate a random numpy array of size `size`
    for i in range(test_iters):
        input1 = np.random.rand(size) / 10
        input2 = np.random.rand(size) / 10
        input3 = np.random.rand(size) / 10

        assert not np.allclose(input1, input2)

        start_time = time.perf_counter_ns()
        rust_result = ltell_rust(input1, input2, input3)
        rust_time = time.perf_counter_ns() - start_time
        rust_times.append(rust_time)

        start_time = time.perf_counter_ns()
        c_result = ltell_c(input1, input2, input3)
        c_time = time.perf_counter_ns() - start_time
        c_times.append(c_time)

        assert np.allclose(c_result, rust_result), \
            "C and rust results do not match"

    return (c_times, rust_times)



def benchmark_detector_of_source(size: int, test_iters: int = 1000) -> tuple[list[float], list[float]]:
    c_times = []
    rust_times = []

    # generate a random numpy array of size `size`
    for i in range(test_iters):
        input1 = np.random.rand(size)
        input2 = np.random.rand(size)

        assert not np.allclose(input1, input2)

        start_time = time.perf_counter_ns()
        rust_result = detector_of_source_rust(input1, input2)
        rust_time = time.perf_counter_ns() - start_time
        rust_times.append(rust_time)

        start_time = time.perf_counter_ns()
        c_result = detector_of_source_c(input1, input2)
        c_time = time.perf_counter_ns() - start_time
        c_times.append(c_time)

        assert np.allclose(c_result, rust_result), \
            "C and rust results do not match"

    return (c_times, rust_times)

def benchmark_source_of_detector(size: int, test_iters: int = 1000) -> tuple[list[float], list[float]]:
    c_times = []
    rust_times = []

    # generate a random numpy array of size `size`
    for i in range(test_iters):
        input1 = np.random.rand(size)
        input2 = np.random.rand(size)

        assert not np.allclose(input1, input2)

        start_time = time.perf_counter_ns()
        rust_result = source_of_detector_rust(input1, input2)
        rust_time = time.perf_counter_ns() - start_time
        rust_times.append(rust_time)

        start_time = time.perf_counter_ns()
        c_result = source_of_detector_c(input1, input2)
        c_time = time.perf_counter_ns() - start_time
        c_times.append(c_time)

        assert np.allclose(c_result, rust_result), \
            "C and rust results do not match"

    return (c_times, rust_times)

def benchmark_m2_of_m_eta(size: int, test_iters: int = 1000) -> tuple[list[float], list[float]]:
    c_times = []
    rust_times = []

    # generate a random numpy array of size `size`
    for i in range(test_iters):
        input1 = np.random.rand(size)
        input2 = np.random.rand(size)

        assert not np.allclose(input1, input2)

        start_time = time.perf_counter_ns()
        rust_result = m2_of_m_eta_rust(input1, input2)
        rust_time = time.perf_counter_ns() - start_time
        rust_times.append(rust_time)

        start_time = time.perf_counter_ns()
        c_result = m2_of_m_eta_c(input1, input2)
        c_time = time.perf_counter_ns() - start_time
        c_times.append(c_time)

        assert np.allclose(c_result, rust_result, equal_nan =True), \
            "C and rust results do not match"

    return (c_times, rust_times)

def benchmark_m1_of_m_eta(size: int, test_iters: int = 1000) -> tuple[list[float], list[float]]:
    c_times = []
    rust_times = []

    # generate a random numpy array of size `size`
    for i in range(test_iters):
        input1 = np.random.rand(size)
        input2 = np.random.rand(size)

        assert not np.allclose(input1, input2)

        start_time = time.perf_counter_ns()
        rust_result = m1_of_m_eta_rust(input1, input2)
        rust_time = time.perf_counter_ns() - start_time
        rust_times.append(rust_time)

        start_time = time.perf_counter_ns()
        c_result = m1_of_m_eta_c(input1, input2)
        c_time = time.perf_counter_ns() - start_time
        c_times.append(c_time)

        assert np.allclose(c_result, rust_result, equal_nan=True), \
            "C and rust results do not match"

    return (c_times, rust_times)

def benchmark_m_of_mc_eta(size: int, test_iters: int = 1000) -> tuple[list[float], list[float]]:
    c_times = []
    rust_times = []

    # generate a random numpy array of size `size`
    for i in range(test_iters):
        input1 = np.random.rand(size)
        input2 = np.random.rand(size)

        assert not np.allclose(input1, input2)

        start_time = time.perf_counter_ns()
        rust_result = m_of_mc_eta_rust(input1, input2)
        rust_time = time.perf_counter_ns() - start_time
        rust_times.append(rust_time)

        start_time = time.perf_counter_ns()
        c_result = m_of_mc_eta_c(input1, input2)
        c_time = time.perf_counter_ns() - start_time
        c_times.append(c_time)

        assert np.allclose(c_result, rust_result), \
            "C and rust results do not match"

    return (c_times, rust_times)


def benchmark_mc_of_m1_m2(size: int, test_iters: int = 1000) -> tuple[list[float], list[float]]:
    c_times = []
    rust_times = []

    # generate a random numpy array of size `size`
    for i in range(test_iters):
        input1 = np.random.rand(size)
        input2 = np.random.rand(size)

        assert not np.allclose(input1, input2)

        start_time = time.perf_counter_ns()
        rust_result = mc_rust(input1, input2)
        rust_time = time.perf_counter_ns() - start_time
        rust_times.append(rust_time)

        start_time = time.perf_counter_ns()
        c_result = mc_c(input1, input2)
        c_time = time.perf_counter_ns() - start_time
        c_times.append(c_time)

        assert np.allclose(c_result, rust_result), \
            "C and rust results do not match"

    return (c_times, rust_times)


def benchmark_eta_of_m1_m2(size: int, test_iters: int = 1000) -> tuple[list[float], list[float]]:
    c_times = []
    rust_times = []

    # generate a random numpy array of size `size`
    for i in range(test_iters):
        input1 = np.random.rand(size)
        input2 = np.random.rand(size)

        assert not np.allclose(input1, input2)

        start_time = time.perf_counter_ns()
        rust_result = eta_rust(input1, input2)
        rust_time = time.perf_counter_ns() - start_time
        rust_times.append(rust_time)

        start_time = time.perf_counter_ns()
        c_result = eta_c(input1, input2)
        c_time = time.perf_counter_ns() - start_time
        c_times.append(c_time)

        assert np.allclose(c_result, rust_result), \
            "C and rust results do not match"

    return (c_times, rust_times)


def benchmark_mc_and_eta_of_m1_m2(size: int, test_iters: int = 1000) -> tuple[list[float], list[float]]:
    c_times = []
    rust_times = []

    # generate a random numpy array of size `size`
    for i in range(test_iters):
        input1 = np.random.rand(size)
        input2 = np.random.rand(size)

        assert not np.allclose(input1, input2)

        start_time = time.perf_counter_ns()
        rust_result = mc_eta_rust(input1, input2)
        rust_time = time.perf_counter_ns() - start_time
        rust_times.append(rust_time)

        start_time = time.perf_counter_ns()
        c_mc_result = mc_c(input1, input2)
        c_eta_result = eta_c(input1, input2)
        c_time = time.perf_counter_ns() - start_time
        c_times.append(c_time)

        assert np.allclose(c_mc_result, rust_result[0]), \
            "C and rust mc results do not match"
        assert np.allclose(c_eta_result, rust_result[1]), \
            "C and rust eta results do not match"

    return (c_times, rust_times)

def benchmark_dwd_a_arr(size: int, test_iters: int = 1000) -> tuple[list[float], list[float]]:
    c_times = []
    rust_times = []

    # generate a random numpy array of size `size`
    for i in range(test_iters):
        input1 = np.random.rand(size)
        input2 = np.random.rand(size)
        input3 = np.random.rand(size)
        input4 = np.random.rand(size)

        assert not np.allclose(input1, input2)

        start_time = time.perf_counter_ns()
        rust_result = dwd_a_rust(input1, input2, input3, input4)
        rust_time = time.perf_counter_ns() - start_time
        rust_times.append(rust_time)

        start_time = time.perf_counter_ns()
        c_result = dwd_a_c(input1, input2, input3, input4)
        c_time = time.perf_counter_ns() - start_time
        c_times.append(c_time)

        assert np.allclose(c_result, rust_result), \
            "C and rust results do not match"

    return (c_times, rust_times)


def benchmark_dwd_p_arr(size: int, test_iters: int = 1000) -> tuple[list[float], list[float]]:
    c_times = []
    rust_times = []

    # generate a random numpy array of size `size`
    for i in range(test_iters):
        input1 = np.random.rand(size)
        input2 = np.random.rand(size)
        input3 = np.random.rand(size)
        input4 = np.random.rand(size)

        assert not np.allclose(input1, input2)

        start_time = time.perf_counter_ns()
        rust_result = dwd_p_rust(input1, input2, input3, input4)
        rust_time = time.perf_counter_ns() - start_time
        rust_times.append(rust_time)

        start_time = time.perf_counter_ns()
        c_result = dwd_p_c(input1, input2, input3, input4)
        c_time = time.perf_counter_ns() - start_time
        c_times.append(c_time)

        assert np.allclose(c_result, rust_result), \
            "C and rust results do not match"

    return (c_times, rust_times)


def benchmark_kepler_arr(size: int, test_iters: int = 1000) -> tuple[list[float], list[float]]:
    c_times = []
    rust_times = []

    # generate a random numpy array of size `size`
    for i in range(test_iters):
        input1 = np.random.rand(size)
        input2 = np.random.rand(size)
        input3 = np.random.rand(size)

        assert not np.allclose(input1, input2)

        start_time = time.perf_counter_ns()
        rust_result = kepler_rust(input1, input2, input3)
        rust_time = time.perf_counter_ns() - start_time
        rust_times.append(rust_time)

        start_time = time.perf_counter_ns()
        c_result = kepler_c(input1, input2, input3)
        c_time = time.perf_counter_ns() - start_time
        c_times.append(c_time)

        assert np.allclose(c_result, rust_result), \
            "C and rust results do not match"

    return (c_times, rust_times)


def benchmark_merge_arr(size: int, test_iters: int = 1000) -> tuple[list[float], list[float]]:
    c_times = []
    rust_times = []

    # generate a random numpy array of size `size`
    for i in range(test_iters):
        input1 = np.random.rand(size)
        input2 = np.random.rand(size)
        input3 = np.random.rand(size)

        assert not np.allclose(input1, input2)

        start_time = time.perf_counter_ns()
        rust_result = merge_rust(input1, input2, input3)
        rust_time = time.perf_counter_ns() - start_time
        rust_times.append(rust_time)

        start_time = time.perf_counter_ns()
        c_result = merge_c(input1, input2, input3)
        c_time = time.perf_counter_ns() - start_time
        c_times.append(c_time)

        assert np.allclose(c_result, rust_result), \
            "C and rust results do not match"

    return (c_times, rust_times)


def benchmark_evol_arr(size: int, test_iters: int = 1000) -> tuple[list[float], list[float]]:
    c_times = []
    rust_times = []

    # generate a random numpy array of size `size`
    for i in range(test_iters):
        input1 = np.random.rand(size)
        input2 = np.random.rand(size)
        input3 = np.random.rand(size)
        input4 = np.random.rand(size)

        assert not np.allclose(input1, input2)

        start_time = time.perf_counter_ns()
        rust_result = evol_rust(input1, input2, input3, input4)
        rust_time = time.perf_counter_ns() - start_time
        rust_times.append(rust_time)

        start_time = time.perf_counter_ns()
        c_result = evol_c(input1, input2, input3, input4)
        c_time = time.perf_counter_ns() - start_time
        c_times.append(c_time)

        assert np.allclose(c_result, rust_result), \
            "C and rust results do not match"

    return (c_times, rust_times)

def benchmark_beta_arr(size: int, test_iters: int = 1000) -> tuple[list[float], list[float]]:
    c_times = []
    rust_times = []

    # generate a random numpy array of size `size`
    for i in range(test_iters):
        input1 = np.random.rand(size)
        input2 = np.random.rand(size)

        assert not np.allclose(input1, input2)

        start_time = time.perf_counter_ns()
        rust_result = beta_rust(input1, input2)
        rust_time = time.perf_counter_ns() - start_time
        rust_times.append(rust_time)

        start_time = time.perf_counter_ns()
        c_result = beta_c(input1, input2)
        c_time = time.perf_counter_ns() - start_time
        c_times.append(c_time)

        assert np.allclose(c_result, rust_result), \
            "C and rust results do not match"

    return (c_times, rust_times)


def benchmark_peters_arr(size: int, test_iters: int = 1000) -> tuple[list[float], list[float]]:
    c_times = []
    rust_times = []

    # generate a random numpy array of size `size`
    for i in range(test_iters):
        input = np.random.rand(size)

        start_time = time.perf_counter_ns()
        c_result = peters_c(input)
        c_time = time.perf_counter_ns() - start_time
        c_times.append(c_time)

        start_time = time.perf_counter_ns()
        rust_result = peters_rust(input)
        rust_time = time.perf_counter_ns() - start_time
        rust_times.append(rust_time)

        assert np.allclose(c_result, rust_result), \
            "C and rust results do not match"

    return (c_times, rust_times)



def benchmark_peters_int_arr(size: int, test_iters: int = 1000) -> tuple[list[float], list[float]]:
    c_times = []
    rust_times = []

    # generate a random numpy array of size `size`
    for i in range(test_iters):
        input = np.random.rand(size)

        start_time = time.perf_counter_ns()
        c_result = peters_int_c(input)
        c_time = time.perf_counter_ns() - start_time
        c_times.append(c_time)

        start_time = time.perf_counter_ns()
        rust_result = peters_int_rust(input)
        rust_time = time.perf_counter_ns() - start_time
        rust_times.append(rust_time)

        assert np.allclose(c_result, rust_result), \
            "C and rust results do not match"

    return (c_times, rust_times)


def benchmark_orb_arr(size: int, test_iters: int = 1000) -> tuple[list[float], list[float]]:
    c_times = []
    rust_times = []

    # generate a random numpy array of size `size`
    for i in range(test_iters):
        input = np.random.rand(size)

        start_time = time.perf_counter_ns()
        c_result = orb_c(preamble, c0, input)
        c_time = time.perf_counter_ns() - start_time
        c_times.append(c_time)

        start_time = time.perf_counter_ns()
        rust_result = orb_rust(preamble, c0, input)
        rust_time = time.perf_counter_ns() - start_time
        rust_times.append(rust_time)

        assert np.allclose(c_result, rust_result), \
            "C and rust results do not match"

    return (c_times, rust_times)

def benchmark():

    # print("")
    # print("beta_arr")
    #
    # (c_times, rust_times) = benchmark_beta_arr(500)
    # print("Beta Arrays: 500 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")
    #
    # (c_times, rust_times) = benchmark_beta_arr(1000)
    # print("Beta Arrays: 1000 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")
    #
    # (c_times, rust_times) = benchmark_beta_arr(5000)
    # print("Beta Arrays: 5000 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")
    #
    # (c_times, rust_times) = benchmark_beta_arr(10000)
    # print("Beta Arrays: 10000 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")
    #
    #
    # print("")
    # print("orb_sep_evol_circ_arr")
    #
    # (c_times, rust_times) = benchmark_evol_arr(500)
    # print("evol Arrays: 500 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")
    #
    # (c_times, rust_times) = benchmark_evol_arr(1000)
    # print("evol Arrays: 1000 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")
    #
    # (c_times, rust_times) = benchmark_evol_arr(5000)
    # print("evol Arrays: 5000 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")
    #
    # (c_times, rust_times) = benchmark_evol_arr(10000)
    # print("evol Arrays: 10000 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")



    # print("")
    # print("peters_int_ecc_const_arr")
    #
    # (c_times, rust_times) = benchmark_peters_int_arr(500)
    # print("peters_int Arrays: 500 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")
    #
    # (c_times, rust_times) = benchmark_peters_int_arr(1000)
    # print("peters_int Arrays: 1000 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")
    #
    # (c_times, rust_times) = benchmark_peters_int_arr(5000)
    # print("peters_int Arrays: 5000 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")
    #
    # (c_times, rust_times) = benchmark_peters_int_arr(10000)
    # print("peters_int Arrays: 10000 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    # print("")
    # print("merge_time_circ_arr")
    #
    # (c_times, rust_times) = benchmark_merge_arr(500)
    # print("Arrays: 500 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")
    #
    # (c_times, rust_times) = benchmark_merge_arr(1000)
    # print("Arrays: 1000 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")
    #
    # (c_times, rust_times) = benchmark_merge_arr(5000)
    # print("Arrays: 5000 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")
    #
    # (c_times, rust_times) = benchmark_merge_arr(10000)
    # print("Arrays: 10000 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")


    # print("")
    # print("orb_sep_evol_ecc_integrand_arr")
    #
    # (c_times, rust_times) = benchmark_orb_arr(500)
    # print("Orb Arrays: 500 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")
    #
    # (c_times, rust_times) = benchmark_orb_arr(1000)
    # print("Orb Arrays: 1000 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")
    #
    # (c_times, rust_times) = benchmark_orb_arr(5000)
    # print("Orb Arrays: 5000 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")
    #
    # (c_times, rust_times) = benchmark_orb_arr(10000)
    # print("Orb Arrays: 10000 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")


    # print("")
    # print("orbital_period_of_m1_m2_a_arr")
    #
    # (c_times, rust_times) = benchmark_kepler_arr(500)
    # print("kepler Arrays: 500 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")
    #
    # (c_times, rust_times) = benchmark_kepler_arr(1000)
    # print("kepler Arrays: 1000 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")
    #
    # (c_times, rust_times) = benchmark_kepler_arr(5000)
    # print("kepler Arrays: 5000 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")
    #
    # (c_times, rust_times) = benchmark_kepler_arr(10000)
    # print("kepler Arrays: 10000 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")



    # print("")
    # print("dwd_a_arr")
    #
    # (c_times, rust_times) = benchmark_dwd_a_arr(500)
    # print("Arrays: 500 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")
    #
    # (c_times, rust_times) = benchmark_dwd_a_arr(1000)
    # print("Arrays: 1000 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")
    #
    # (c_times, rust_times) = benchmark_dwd_a_arr(5000)
    # print("Arrays: 5000 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")
    #
    # (c_times, rust_times) = benchmark_dwd_a_arr(10000)
    # print("Arrays: 10000 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")
    #
    #
    # print("")
    # print("dwd_p_arr")
    #
    # (c_times, rust_times) = benchmark_dwd_p_arr(500)
    # print("Arrays: 500 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")
    #
    # (c_times, rust_times) = benchmark_dwd_p_arr(1000)
    # print("Arrays: 1000 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")
    #
    # (c_times, rust_times) = benchmark_dwd_p_arr(5000)
    # print("Arrays: 5000 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")
    #
    # (c_times, rust_times) = benchmark_dwd_p_arr(10000)
    # print("Arrays: 10000 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    print("")
    print("mc_of_m1_m2")

    (c_times, rust_times) = benchmark_mc_of_m1_m2(500)
    print("Arrays: 500 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    (c_times, rust_times) = benchmark_mc_of_m1_m2(1000)
    print("Arrays: 1000 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    (c_times, rust_times) = benchmark_mc_of_m1_m2(5000)
    print("Arrays: 5000 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    (c_times, rust_times) = benchmark_mc_of_m1_m2(10000)
    print("Arrays: 10000 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    print("")
    print("eta_of_m1_m2")

    (c_times, rust_times) = benchmark_eta_of_m1_m2(500)
    print("Arrays: 500 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    (c_times, rust_times) = benchmark_eta_of_m1_m2(1000)
    print("Arrays: 1000 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    (c_times, rust_times) = benchmark_eta_of_m1_m2(5000)
    print("Arrays: 5000 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    (c_times, rust_times) = benchmark_eta_of_m1_m2(10000)
    print("Arrays: 10000 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")


    # print("")
    # print("mc_and_eta_of_m1_m2")
    #
    # (c_times, rust_times) = benchmark_mc_and_eta_of_m1_m2(500)
    # print("Arrays: 500 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")
    #
    # (c_times, rust_times) = benchmark_mc_and_eta_of_m1_m2(1000)
    # print("Arrays: 1000 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")
    #
    # (c_times, rust_times) = benchmark_mc_and_eta_of_m1_m2(5000)
    # print("Arrays: 5000 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")
    #
    # (c_times, rust_times) = benchmark_mc_and_eta_of_m1_m2(10000)
    # print("Arrays: 10000 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")


    print("")
    print("m_of_mc_eta")

    (c_times, rust_times) = benchmark_m_of_mc_eta(500)
    print("Arrays: 500 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    (c_times, rust_times) = benchmark_m_of_mc_eta(1000)
    print("Arrays: 1000 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    (c_times, rust_times) = benchmark_m_of_mc_eta(5000)
    print("Arrays: 5000 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    (c_times, rust_times) = benchmark_m_of_mc_eta(10000)
    print("Arrays: 10000 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")


    print("")
    print("m1_of_m_eta")

    (c_times, rust_times) = benchmark_m1_of_m_eta(500)
    print("Arrays: 500 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    (c_times, rust_times) = benchmark_m1_of_m_eta(1000)
    print("Arrays: 1000 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    (c_times, rust_times) = benchmark_m1_of_m_eta(5000)
    print("Arrays: 5000 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    (c_times, rust_times) = benchmark_m1_of_m_eta(10000)
    print("Arrays: 10000 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")


    print("")
    print("m2_of_m_eta")

    (c_times, rust_times) = benchmark_m2_of_m_eta(500)
    print("Arrays: 500 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    (c_times, rust_times) = benchmark_m2_of_m_eta(1000)
    print("Arrays: 1000 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    (c_times, rust_times) = benchmark_m2_of_m_eta(5000)
    print("Arrays: 5000 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    (c_times, rust_times) = benchmark_m2_of_m_eta(10000)
    print("Arrays: 10000 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")


    print("")
    print("source_of_detector")

    (c_times, rust_times) = benchmark_source_of_detector(500)
    print("Arrays: 500 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    (c_times, rust_times) = benchmark_source_of_detector(1000)
    print("Arrays: 1000 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    (c_times, rust_times) = benchmark_source_of_detector(5000)
    print("Arrays: 5000 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    (c_times, rust_times) = benchmark_source_of_detector(10000)
    print("Arrays: 10000 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")
    print("")
    print("detector_of_source")

    (c_times, rust_times) = benchmark_detector_of_source(500)
    print("Arrays: 500 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    (c_times, rust_times) = benchmark_detector_of_source(1000)
    print("Arrays: 1000 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    (c_times, rust_times) = benchmark_detector_of_source(5000)
    print("Arrays: 5000 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    (c_times, rust_times) = benchmark_detector_of_source(10000)
    print("Arrays: 10000 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")



    print("")
    print("lambda_tilde_of_eta_lambda1_lambda2")

    (c_times, rust_times) = benchmark_ltell(500)
    print("Arrays: 500 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    (c_times, rust_times) = benchmark_ltell(1000)
    print("Arrays: 1000 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    (c_times, rust_times) = benchmark_ltell(5000)
    print("Arrays: 5000 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    (c_times, rust_times) = benchmark_ltell(10000)
    print("Arrays: 10000 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    print("")
    print("delta_lambda_of_eta_lambda1_lambda2")

    (c_times, rust_times) = benchmark_dlell(500)
    print("Arrays: 500 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    (c_times, rust_times) = benchmark_dlell(1000)
    print("Arrays: 1000 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    (c_times, rust_times) = benchmark_dlell(5000)
    print("Arrays: 5000 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    (c_times, rust_times) = benchmark_dlell(10000)
    print("Arrays: 10000 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")



    # removing due to numerical instability
    #
    # print("")
    # print("lambda1_of_eta_lambda_tilde_delta_lambda")
    #
    # (c_times, rust_times) = benchmark_l1eltdl(500)
    # print("Arrays: 500 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")
    #
    # (c_times, rust_times) = benchmark_l1eltdl(1000)
    # print("Arrays: 1000 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")
    #
    # (c_times, rust_times) = benchmark_l1eltdl(5000)
    # print("Arrays: 5000 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")
    #
    # (c_times, rust_times) = benchmark_l1eltdl(10000)
    # print("Arrays: 10000 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")


    # print("")
    # print("lambda2_of_eta_lambda_tilde_delta_lambda")
    #
    # (c_times, rust_times) = benchmark_l2eltdl(500)
    # print("Arrays: 500 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")
    #
    # (c_times, rust_times) = benchmark_l2eltdl(1000)
    # print("Arrays: 1000 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")
    #
    # (c_times, rust_times) = benchmark_l2eltdl(5000)
    # print("Arrays: 5000 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")
    #
    # (c_times, rust_times) = benchmark_l2eltdl(10000)
    # print("Arrays: 10000 long")
    # print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    # print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    # print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")





if __name__ == "__main__":
    benchmark()
