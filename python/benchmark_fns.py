import time
import numpy as np

from basil_core.astro.orbit._decay import _orb_sep_evol_ecc_integrand_arr as orb_c # ty: ignore[unresolved-import]
from basil_core.astro.orbit._decay import _beta_arr as beta_c # ty: ignore[unresolved-import]
from basil_core.astro.orbit._decay import _peters_ecc_const_arr as peters_c # ty: ignore[unresolved-import]

from basil import orb_sep_evol_ecc_integrand_arr as orb_rust # ty: ignore[unresolved-import]
from basil import beta_arr as beta_rust # ty: ignore[unresolved-import]
from basil import peters_ecc_const_arr as peters_rust # ty: ignore[unresolved-import]


# test_iters = 1000
preamble = 0.234
c0 = 0.432

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

    print("")
    print("beta_arr")

    (c_times, rust_times) = benchmark_beta_arr(500)
    print("Beta Arrays: 500 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    (c_times, rust_times) = benchmark_beta_arr(1000)
    print("Beta Arrays: 1000 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    (c_times, rust_times) = benchmark_beta_arr(5000)
    print("Beta Arrays: 5000 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    (c_times, rust_times) = benchmark_beta_arr(10000)
    print("Beta Arrays: 10000 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    print("")
    print("peters_ecc_const_arr")

    (c_times, rust_times) = benchmark_peters_arr(500)
    print("peters Arrays: 500 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    (c_times, rust_times) = benchmark_peters_arr(1000)
    print("peters Arrays: 1000 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    (c_times, rust_times) = benchmark_peters_arr(5000)
    print("peters Arrays: 5000 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    (c_times, rust_times) = benchmark_peters_arr(10000)
    print("peters Arrays: 10000 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    print("")
    print("orb_sep_evol_ecc_integrand_arr")

    (c_times, rust_times) = benchmark_orb_arr(500)
    print("Orb Arrays: 500 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    (c_times, rust_times) = benchmark_orb_arr(1000)
    print("Orb Arrays: 1000 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    (c_times, rust_times) = benchmark_orb_arr(5000)
    print("Orb Arrays: 5000 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")

    (c_times, rust_times) = benchmark_orb_arr(10000)
    print("Orb Arrays: 10000 long")
    print(f"    C averaged:   {np.mean(c_times):.5f} nanoseconds")
    print(f"    Rust averaged:  {np.mean(rust_times):.5f} nanoseconds")
    print(f"    Differential (C / Rust):  {np.mean(c_times)/np.mean(rust_times):.2f}x")






if __name__ == "__main__":
    benchmark()
