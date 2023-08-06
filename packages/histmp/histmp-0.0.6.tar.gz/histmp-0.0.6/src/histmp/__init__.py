# BSD 3-Clause License
#
# Copyright (c) 2019, Doug Davis
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

__doc__ = "Calculate histograms with blazing speed."

__version__ = "0.0.6.dev0"
version_info = tuple(__version__.split("."))

import numpy as np
from histmp._CPP import _f1dw, _v1dw, _omp_get_max_threads
from histmp._CPP_PB import _f1dmw, _v1dmw


__all__ = ["histogram", "omp_get_max_threads"]


def _likely_uniform_bins(edges):
    """Test if bin edges describe a set of fixed width bins"""
    diffs = np.ediff1d(edges)
    ones = np.ones_like(diffs)
    max_close = np.allclose(ones, diffs / np.amax(diffs))
    min_close = np.allclose(ones, diffs / np.amin(diffs))
    return max_close and min_close


def omp_get_max_threads():
    """Get the number of threads available to OpenMP.

    This returns the result of calling the OpenMP C API function `of
    the same name
    <https://www.openmp.org/spec-html/5.0/openmpsu112.html>`_.

    Returns
    -------
    int
        the maximum number of available threads

    """
    return _omp_get_max_threads()


def histogram(x, bins=10, range=None, weights=None, density=False, flow=False):
    """Calculate a histogram for one dimensional data.

    Parameters
    ----------
    x : array_like
        the data to histogram.
    bins : int or array_like
        if int: the number of bins; if array_like: the bin edges.
    range : tuple(float, float), optional
        the definition of the edges of the bin range (start, stop).
    weights : array_like, optional
        a set of weights associated with the elements of ``x``. This
        can also be a two dimensional set of multiple weights
        varitions with shape (len(x), n_weight_variations).
    density : bool
        normalize counts such that the integral over the range is
        equal to 1. If ``weights`` is two dimensional this argument is
        ignored.
    flow : bool
        if ``True``, include under/overflow in the first/last bins.

    Returns
    -------
    :py:obj:`numpy.ndarray`
        the bin counts
    :py:obj:`numpy.ndarray`
        the standard error of each bin count, :math:`\sqrt{\sum_i w_i^2}`

    """
    x = np.ascontiguousarray(x)
    if weights is not None:
        weights = np.ascontiguousarray(weights)
    else:
        weights = np.ones_like(x, order="C")
        if not (weights.dtype == np.float32 or weights.dtype == np.float64):
            weights = weights.astype(np.float64)

    if isinstance(bins, int):
        if range is not None:
            start, stop = range[0], range[1]
        else:
            start, stop = np.amin(x), np.amax(x)
        if weights.shape == x.shape:
            return _f1dw(x, weights, bins, start, stop, flow, density, True)
        else:
            return _f1dmw(x, weights, bins, start, stop, flow, True)

    else:
        if range is not None:
            raise TypeError("range must be None if bins is non-int")
        bins = np.ascontiguousarray(bins)
        if not np.all(bins[1:] >= bins[:-1]):
            raise ValueError("bins sequence must monotonically increase")
        if _likely_uniform_bins(bins):
            if weights.shape == x.shape:
                return _f1dw(
                    x, weights, len(bins) - 1, bins[0], bins[-1], flow, density, True
                )
            else:
                return _f1dmw(x, weights, len(bins) - 1, bins[0], bins[-1], flow, True)
        if weights.shape == x.shape:
            return _v1dw(x, weights, bins, flow, density, True)
        else:
            return _v1dmw(x, weights, bins, flow, True)
