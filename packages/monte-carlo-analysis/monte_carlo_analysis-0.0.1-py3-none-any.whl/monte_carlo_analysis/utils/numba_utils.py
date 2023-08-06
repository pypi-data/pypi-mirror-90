"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-10-23

**Project** : monte_carlo_analysis

** Implement numba util functions **

Numba histogram
- Code adapted from: https://numba.pydata.org/numba-examples/examples/density_estimation/histogram/results.html

"""
import numba
import numpy as np


@numba.jit(nopython=True)
def get_bin_edges(bins: int, min_value: float, max_value: float) -> np.array:
    """
    Compute the number of bins

    :param bins: Number of bin in the histogram
    :param min_value: Minimum value of the histogram
    :param max_value: Minimum value of the histogram
    """
    bin_edges = np.zeros((bins+1,), dtype=np.float64)
    delta = (max_value - min_value) / bins
    for i in range(bin_edges.shape[0]):
        bin_edges[i] = min_value + i * delta

    bin_edges[-1] = max_value  # Avoid roundoff error on last point
    return bin_edges


@numba.jit(nopython=True)
def compute_bin(
        x: np.array, bin_edges: np.array,
        min_value: float, max_value: float
        ) -> np.array:
    """
    Compute the histogram bins

    :param x: Flat array
    :param bin_edges: Edges of the bin
    :param min_value: Minimum value of the histogram
    :param max_value: Minimum value of the histogram
    """
    # assuming uniform bins for now
    n = bin_edges.shape[0] - 1

    # special case to mirror NumPy behavior for last bin
    if x == max_value:
        return n - 1 # max_value always in last bin

    bin = int(n * (x - min_value) / (max_value - min_value))

    if bin < 0 or bin >= n:
        return None
    else:
        return bin


@numba.jit(nopython=True)
def numba_histogram(
        a: np.array, bins: int, min_value: float = None,
        max_value: float = None, normalized: bool = False
        ) -> tuple:
    """
    Compute an histogram using numba

    :param a: array to transform to histogram
    :param bins: Number of bins
    :param min_value: Minimum value of the histogram
    :param max_value: Minimum value of the histogram
    :param normalized: Set normalization of the array
    """
    if min_value is None:
        min_value = a.min()
    if max_value is None:
        max_value = a.max()

    hist = np.zeros((bins,))
    bin_edges = get_bin_edges(
        bins, min_value, max_value
        )
    if normalized:
        increment = 1. / a.shape[0]
    else:
        increment = 1.
    for x in a.flat:
        bin = compute_bin(
            x, bin_edges, min_value,
            max_value
            )
        if bin is not None:
            hist[int(bin)] += increment
    return hist, bin_edges

@numba.jit(nopython=True)
def numba_cumul_histogram(
        a: np.array, bins: int, min_value: float = None,
        max_value: float = None, normalized: bool = False
        ) -> tuple:
    """
    Compute a cumulated histogram using numba

    :param a: array to transform to histogram
    :param bins: Number of bins
    :param min_value: Minimum value of the histogram
    :param max_value: Minimum value of the histogram
    :param normalized: Set normalization of the array
    """
    if min_value is None:
        min_value = a.min()
    if max_value is None:
        max_value = a.max()

    hist = np.zeros((bins,))
    bin_edges = get_bin_edges(
        bins, min_value, max_value
        )
    if normalized:
        increment = 1. / a.shape[0]
    else:
        increment = 1.
    for x in a.flat:
        bin = compute_bin(
            x, bin_edges, min_value,
            max_value
            )
        if bin is not None:
            hist[int(bin)] += increment
    for i in range(1, bins):
        hist[i] = hist[i - 1] + hist[i]
    return hist, bin_edges

