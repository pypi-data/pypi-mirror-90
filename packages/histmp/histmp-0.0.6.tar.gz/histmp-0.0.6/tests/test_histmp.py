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

import os
import multiprocessing
import histmp as hm
import numpy as np
import pytest


x_f32 = np.random.random(10000).astype(np.float32)
x_f64 = np.random.random(10000).astype(np.float64)
x_ui32 = np.abs(5 * np.random.random(10000)).astype(np.uint32)
x_i32 = (8 * np.random.random(10000)).astype(np.int32)

w_f32 = np.random.uniform(0.5, 0.6, x_f32.shape[0]).astype(np.float32)
w_f64 = np.random.uniform(0.5, 0.6, x_f64.shape[0]).astype(np.float64)


class TestMisc:
    def test_omp_get_max_threads(self):
        nthreads = os.getenv("OMP_NUM_THREADS")
        if nthreads is None:
            nthreads = multiprocessing.cpu_count()
        assert int(nthreads) == hm.omp_get_max_threads()


class TestFixedNoFlow:
    def test_fixed_noflow_f32f32(self):
        nbins, xmin, xmax = (12, -3, 3)
        hm_res = hm.histogram(
            x_f32, weights=w_f32, bins=nbins, range=(xmin, xmax), flow=False
        )
        np_res = np.histogram(x_f32, bins=nbins, range=(xmin, xmax), weights=w_f32)
        assert np.allclose(hm_res[0], np_res[0])

    def test_fixed_noflow_f64f32(self):
        nbins, xmin, xmax = (12, -3, 3)
        hm_res = hm.histogram(
            x_f64, weights=w_f32, bins=nbins, range=(xmin, xmax), flow=False
        )
        np_res = np.histogram(x_f64, bins=nbins, range=(xmin, xmax), weights=w_f32)
        assert np.allclose(hm_res[0], np_res[0])

    def test_fixed_noflow_f64f64(self):
        nbins, xmin, xmax = (12, -3, 3)
        hm_res = hm.histogram(
            x_f64, weights=w_f64, bins=nbins, range=(xmin, xmax), flow=False
        )
        np_res = np.histogram(x_f64, bins=nbins, range=(xmin, xmax), weights=w_f64)
        assert np.allclose(hm_res[0], np_res[0])

    def test_fixed_noflow_f32f64(self):
        nbins, xmin, xmax = (12, -3, 3)
        hm_res = hm.histogram(
            x_f32, weights=w_f64, bins=nbins, range=(xmin, xmax), flow=False
        )
        np_res = np.histogram(x_f32, bins=nbins, range=(xmin, xmax), weights=w_f64)
        assert np.allclose(hm_res[0], np_res[0])

    def test_fixed_noflow_ui32f64(self):
        nbins, xmin, xmax = (3, 0.5, 3.5)
        hm_res = hm.histogram(
            x_ui32, weights=w_f64, bins=nbins, range=(xmin, xmax), flow=False
        )
        np_res = np.histogram(x_ui32, bins=nbins, range=(xmin, xmax), weights=w_f64)
        assert np.allclose(hm_res[0], np_res[0])

    def test_fixed_noflow_ui32f32(self):
        nbins, xmin, xmax = (4, -0.5, 3.5)
        hm_res = hm.histogram(
            x_ui32, weights=w_f32, bins=nbins, range=(xmin, xmax), flow=False
        )
        np_res = np.histogram(x_ui32, bins=nbins, range=(xmin, xmax), weights=w_f32)
        assert np.allclose(hm_res[0], np_res[0],)


class TestFixedNoFlowDensity:
    def test_fixed_noflow_f32f32(self):
        nbins, xmin, xmax = (12, -4, 5)
        hm_res = hm.histogram(
            x_f32,
            weights=w_f32,
            bins=nbins,
            range=(xmin, xmax),
            density=True,
            flow=False,
        )
        np_res = np.histogram(
            x_f32, bins=nbins, range=(xmin, xmax), weights=w_f32, density=True
        )
        assert np.allclose(hm_res[0], np_res[0])

    def test_fixed_noflow_f64f32(self):
        nbins, xmin, xmax = (12, -2, 1)
        hm_res = hm.histogram(
            x_f64,
            weights=w_f32,
            bins=nbins,
            range=(xmin, xmax),
            density=True,
            flow=False,
        )
        np_res = np.histogram(
            x_f64, bins=nbins, range=(xmin, xmax), weights=w_f32, density=True
        )
        assert np.allclose(hm_res[0], np_res[0])

    def test_fixed_noflow_f64f64(self):
        nbins, xmin, xmax = (12, -2, 3)
        hm_res = hm.histogram(
            x_f64,
            weights=w_f64,
            bins=nbins,
            range=(xmin, xmax),
            density=True,
            flow=False,
        )
        np_res = np.histogram(
            x_f64, bins=nbins, range=(xmin, xmax), weights=w_f64, density=True
        )
        assert np.allclose(hm_res[0], np_res[0])

    def test_fixed_noflow_f32f64(self):
        nbins, xmin, xmax = (12, -3, 3)
        hm_res = hm.histogram(
            x_f32,
            weights=w_f64,
            bins=nbins,
            range=(xmin, xmax),
            density=True,
            flow=False,
        )
        np_res = np.histogram(
            x_f32, bins=nbins, range=(xmin, xmax), weights=w_f64, density=True
        )
        assert np.allclose(hm_res[0], np_res[0])

    def test_fixed_noflow_ui32f64(self):
        nbins, xmin, xmax = (3, 0.5, 3.5)
        hm_res = hm.histogram(
            x_ui32,
            weights=w_f64,
            bins=nbins,
            range=(xmin, xmax),
            density=True,
            flow=False,
        )
        np_res = np.histogram(
            x_ui32, bins=nbins, range=(xmin, xmax), weights=w_f64, density=True
        )
        assert np.allclose(hm_res[0], np_res[0])

    def test_fixed_noflow_ui32f32(self):
        nbins, xmin, xmax = (4, -0.5, 3.5)
        hm_res = hm.histogram(
            x_ui32,
            weights=w_f32,
            bins=nbins,
            range=(xmin, xmax),
            density=True,
            flow=False,
        )
        np_res = np.histogram(
            x_ui32, bins=nbins, range=(xmin, xmax), weights=w_f32, density=True
        )
        assert np.allclose(hm_res[0], np_res[0],)


class TestFixedFlow:
    def test_fixed_flow_f32f32(self):
        nbins, xmin, xmax = (12, -3, 3)
        hm_res = hm.histogram(
            x_f32, weights=w_f32, bins=nbins, range=(xmin, xmax), flow=True
        )
        np_res = np.histogram(x_f32, bins=nbins, range=(xmin, xmax), weights=w_f32)
        underflow = np.sum(w_f32[x_f32 < xmin])
        overflow = np.sum(w_f32[x_f32 > xmax])
        np_res[0][0] += underflow
        np_res[0][-1] += overflow
        assert np.allclose(hm_res[0], np_res[0])

    def test_fixed_flow_f64f32(self):
        nbins, xmin, xmax = (12, -3, 3)
        hm_res = hm.histogram(
            x_f64, weights=w_f32, bins=nbins, range=(xmin, xmax), flow=True
        )
        np_res = np.histogram(x_f64, bins=nbins, range=(xmin, xmax), weights=w_f32)
        underflow = np.sum(w_f32[x_f64 < xmin])
        overflow = np.sum(w_f32[x_f64 > xmax])
        np_res[0][0] += underflow
        np_res[0][-1] += overflow
        assert np.allclose(hm_res[0], np_res[0])

    def test_fixed_flow_f64f64(self):
        nbins, xmin, xmax = (12, -3, 3)
        hm_res = hm.histogram(
            x_f64, weights=w_f64, bins=nbins, range=(xmin, xmax), flow=True
        )
        np_res = np.histogram(x_f64, bins=nbins, range=(xmin, xmax), weights=w_f64)
        underflow = np.sum(w_f64[x_f64 < xmin])
        overflow = np.sum(w_f64[x_f64 > xmax])
        np_res[0][0] += underflow
        np_res[0][-1] += overflow
        assert np.allclose(hm_res[0], np_res[0])

    def test_fixed_flow_except(self):
        x = x_f64.astype(np.int16)
        nbins, xmin, xmax = (15, -2.1, 3.2)
        with pytest.raises(TypeError) as excinfo:
            hm_res = hm.histogram(
                x, weights=w_f64, bins=nbins, range=(xmin, xmax), flow=True
            )
        assert str(excinfo.value) == "dtype of input arrays unsupported"
        w = w_f64.astype(np.int8)
        with pytest.raises(TypeError) as excinfo:
            hm_res = hm.histogram(
                x_f64, weights=w, bins=nbins, range=(xmin, xmax), flow=True
            )
        assert str(excinfo.value) == "dtype of input arrays unsupported"

    def test_fixed_flow_f32f64(self):
        nbins, xmin, xmax = (12, -3, 3)
        hm_res = hm.histogram(
            x_f32, weights=w_f64, bins=nbins, range=(xmin, xmax), flow=True
        )
        np_res = np.histogram(x_f32, bins=nbins, range=(xmin, xmax), weights=w_f64)
        underflow = np.sum(w_f64[x_f32 < xmin])
        overflow = np.sum(w_f64[x_f32 > xmax])
        np_res[0][0] += underflow
        np_res[0][-1] += overflow
        assert np.allclose(hm_res[0], np_res[0])

    def test_fixed_flow_ui32f64(self):
        nbins, xmin, xmax = (3, 0.5, 3.5)
        hm_res = hm.histogram(
            x_ui32, weights=w_f64, bins=nbins, range=(xmin, xmax), flow=True
        )
        np_res = np.histogram(x_ui32, bins=nbins, range=(xmin, xmax), weights=w_f64)
        underflow = np.sum(w_f64[x_ui32 < xmin])
        overflow = np.sum(w_f64[x_ui32 > xmax])
        np_res[0][0] += underflow
        np_res[0][-1] += overflow
        assert np.allclose(hm_res[0], np_res[0])

    def test_fixed_flow_ui32f32(self):
        nbins, xmin, xmax = (4, -0.5, 3.5)
        hm_res = hm.histogram(
            x_ui32, weights=w_f32, bins=nbins, range=(xmin, xmax), flow=True
        )
        np_res = np.histogram(x_ui32, bins=nbins, range=(xmin, xmax), weights=w_f32)
        underflow = np.sum(w_f32[x_ui32 < xmin])
        overflow = np.sum(w_f32[x_ui32 > xmax])
        np_res[0][0] += underflow
        np_res[0][-1] += overflow
        assert np.allclose(hm_res[0], np_res[0], rtol=1.0e-03, atol=1.0e-05)


class TestVarNoFlow:
    def test_var_noflow_f32f32(self):
        edges = np.array([-2, -1.2, -0.8, -0.1, 1.0, 2.5, 3.0])
        hm_res = hm.histogram(x_f32, weights=w_f32, bins=edges, flow=False)
        np_res = np.histogram(x_f32, bins=edges, weights=w_f32)
        assert np.allclose(hm_res[0], np_res[0])

    def test_var_noflow_f64f32(self):
        edges = np.array([-2, -1.2, -0.8, -0.1, 1.0, 2.5, 3.0])
        hm_res = hm.histogram(x_f64, weights=w_f32, bins=edges, flow=False)
        np_res = np.histogram(x_f64, bins=edges, weights=w_f32)
        assert np.allclose(hm_res[0], np_res[0])

    def test_var_noflow_f64f64(self):
        edges = np.array([-2, -1.2, -0.8, -0.1, 1.0, 2.5, 3.0])
        hm_res = hm.histogram(x_f64, weights=w_f64, bins=edges, flow=False)
        np_res = np.histogram(x_f64, bins=edges, weights=w_f64)
        assert np.allclose(hm_res[0], np_res[0])

    def test_var_noflow_f32f64(self):
        edges = np.array([-2, -1.2, -0.8, -0.1, 1.0, 2.5, 3.0])
        hm_res = hm.histogram(x_f32, weights=w_f64, bins=edges, flow=False)
        np_res = np.histogram(x_f32, bins=edges, weights=w_f64)
        assert np.allclose(hm_res[0], np_res[0])

    def test_var_noflow_ui32f64(self):
        edges = np.array([1.1, 2.2, 3.3, 4.4])
        hm_res = hm.histogram(x_ui32, weights=w_f64, bins=edges, flow=False)
        np_res = np.histogram(x_ui32, bins=edges, weights=w_f64)
        assert np.allclose(hm_res[0], np_res[0])

    def test_var_noflow_ui32f32(self):
        edges = np.array([-0.1, 1.1, 2.2, 3.3, 4.4])
        hm_res = hm.histogram(x_ui32, weights=w_f32, bins=edges, flow=False)
        np_res = np.histogram(x_ui32, bins=edges, weights=w_f32)
        assert np.allclose(hm_res[0], np_res[0], rtol=1.0e-03, atol=1.0e-05)


class TestVarNoFlowDensity:
    def test_var_noflow_f32f32(self):
        edges = np.array([-2, -1.2, -0.8, -0.1, 1.0, 2.5, 3.0])
        hm_res = hm.histogram(
            x_f32, weights=w_f32, bins=edges, density=True, flow=False
        )
        np_res = np.histogram(x_f32, bins=edges, weights=w_f32, density=True)
        assert np.allclose(hm_res[0], np_res[0])

    def test_var_noflow_f64f32(self):
        edges = np.array([-2, -1.2, -0.8, -0.1, 1.0, 2.5, 3.0])
        hm_res = hm.histogram(
            x_f64, weights=w_f32, bins=edges, density=True, flow=False
        )
        np_res = np.histogram(x_f64, bins=edges, weights=w_f32, density=True)
        assert np.allclose(hm_res[0], np_res[0])

    def test_var_noflow_f64f64(self):
        edges = np.array([-2, -1.2, -0.8, -0.1, 1.0, 2.5, 3.0])
        hm_res = hm.histogram(
            x_f64, weights=w_f64, bins=edges, density=True, flow=False
        )
        np_res = np.histogram(x_f64, bins=edges, weights=w_f64, density=True)
        assert np.allclose(hm_res[0], np_res[0])

    def test_var_noflow_f32f64(self):
        edges = np.array([-2, -1.2, -0.8, -0.1, 1.0, 2.5, 3.0])
        hm_res = hm.histogram(
            x_f32, weights=w_f64, bins=edges, density=True, flow=False
        )
        np_res = np.histogram(x_f32, bins=edges, weights=w_f64, density=True)
        assert np.allclose(hm_res[0], np_res[0])

    def test_var_noflow_ui32f64(self):
        edges = np.array([1.1, 2.2, 3.3, 4.4])
        hm_res = hm.histogram(
            x_ui32, weights=w_f64, bins=edges, density=True, flow=False
        )
        np_res = np.histogram(x_ui32, bins=edges, weights=w_f64, density=True)
        assert np.allclose(hm_res[0], np_res[0])

    def test_var_noflow_ui32f32(self):
        edges = np.array([-0.1, 1.1, 2.2, 3.3, 4.4])
        hm_res = hm.histogram(
            x_ui32, weights=w_f32, bins=edges, density=True, flow=False
        )
        np_res = np.histogram(x_ui32, bins=edges, weights=w_f32, density=True)
        assert np.allclose(hm_res[0], np_res[0], rtol=1.0e-03, atol=1.0e-05)


class TestVarFlow:
    def test_var_flow_f32f32(self):
        edges = np.array([-2, -1.2, -0.8, -0.1, 1.0, 2.5, 3.0])
        hm_res = hm.histogram(x_f32, weights=w_f32, bins=edges, flow=True)
        np_res = np.histogram(x_f32, bins=edges, weights=w_f32)
        underflow = np.sum(w_f32[x_f32 < edges[0]])
        overflow = np.sum(w_f32[x_f32 > edges[-1]])
        np_res[0][0] += underflow
        np_res[0][-1] += overflow
        assert np.allclose(hm_res[0], np_res[0])

    def test_var_flow_f64f32(self):
        edges = np.array([-2, -1.2, -0.8, -0.1, 1.0, 2.5, 3.0])
        hm_res = hm.histogram(x_f64, weights=w_f32, bins=edges, flow=True)
        np_res = np.histogram(x_f64, bins=edges, weights=w_f32)
        underflow = np.sum(w_f32[x_f64 < edges[0]])
        overflow = np.sum(w_f32[x_f64 > edges[-1]])
        np_res[0][0] += underflow
        np_res[0][-1] += overflow
        assert np.allclose(hm_res[0], np_res[0])

    def test_var_flow_except(self):
        edges = np.array([-2, -1.2, -0.8, -0.1, 1.0, 2.5, 3.0])
        x = x_f64.astype(np.int16)
        with pytest.raises(TypeError) as excinfo:
            hm_res = hm.histogram(x, weights=w_f64, bins=edges, flow=True)
        assert str(excinfo.value) == "dtype of input arrays unsupported"
        w = w_f64.astype(np.int8)
        with pytest.raises(TypeError) as excinfo:
            hm_res = hm.histogram(x_f64, weights=w, bins=edges, flow=True)
        assert str(excinfo.value) == "dtype of input arrays unsupported"

    def test_var_flow_f64f64(self):
        edges = np.array([-2, -1.2, -0.8, -0.1, 1.0, 2.5, 3.0])
        hm_res = hm.histogram(x_f64, weights=w_f64, bins=edges, flow=True)
        np_res = np.histogram(x_f64, bins=edges, weights=w_f64)
        underflow = np.sum(w_f64[x_f64 < edges[0]])
        overflow = np.sum(w_f64[x_f64 > edges[-1]])
        np_res[0][0] += underflow
        np_res[0][-1] += overflow
        assert np.allclose(hm_res[0], np_res[0])

    def test_var_flow_f32f64(self):
        edges = np.array([-2, -1.2, -0.8, -0.1, 1.0, 2.5, 3.0])
        hm_res = hm.histogram(x_f32, weights=w_f64, bins=edges, flow=True)
        np_res = np.histogram(x_f32, bins=edges, weights=w_f64)
        underflow = np.sum(w_f64[x_f32 < edges[0]])
        overflow = np.sum(w_f64[x_f32 > edges[-1]])
        np_res[0][0] += underflow
        np_res[0][-1] += overflow
        assert np.allclose(hm_res[0], np_res[0])

    def test_var_flow_ui32f64(self):
        edges = np.array([1.1, 2.2, 3.3, 4.4])
        hm_res = hm.histogram(x_ui32, weights=w_f64, bins=edges, flow=True)
        np_res = np.histogram(x_ui32, bins=edges, weights=w_f64)
        underflow = np.sum(w_f64[x_ui32 < edges[0]])
        overflow = np.sum(w_f64[x_ui32 > edges[-1]])
        np_res[0][0] += underflow
        np_res[0][-1] += overflow
        assert np.allclose(hm_res[0], np_res[0])

    def test_var_flow_ui32f32(self):
        edges = np.array([-0.1, 1.1, 2.2, 3.3, 4.4])
        hm_res = hm.histogram(x_ui32, weights=w_f32, bins=edges, flow=True)
        np_res = np.histogram(x_ui32, bins=edges, weights=w_f32)
        underflow = np.sum(w_f32[x_ui32 < edges[0]])
        overflow = np.sum(w_f32[x_ui32 > edges[-1]])
        np_res[0][0] += underflow
        np_res[0][-1] += overflow
        assert np.allclose(hm_res[0], np_res[0], rtol=1.0e-03, atol=1.0e-05)


class TestMutiWeight:
    x_f32 = np.random.randn(10000).astype(np.float32)
    x_f64 = np.random.randn(10000).astype(np.float64)
    w_f32 = np.abs(np.random.randn(x_f32.shape[0], 13)).astype(np.float32) + 1
    w_f64 = np.abs(np.random.randn(x_f64.shape[0], 13)).astype(np.float64) + 1
    edges = np.unique(np.around(np.random.randn(32), 1))

    def test_fixed_mw_f32f32(self):
        nbins, xmin, xmax = (34, -3, 3)
        hm_res_n, hm_res_e = hm.histogram(
            self.x_f32, weights=self.w_f32, bins=nbins, range=(xmin, xmax), flow=False
        )
        for i in range(self.w_f32.shape[1]):
            hm_res_i = hm_res_n.T[i]
            np_res_i, __ = np.histogram(
                self.x_f32, weights=self.w_f32.T[i], bins=nbins, range=(xmin, xmax)
            )
            assert np.allclose(hm_res_i, np_res_i)

    def test_fixed_mw_f64f64(self):
        nbins, xmin, xmax = (34, -3, 3)
        hm_res_n, hm_res_e = hm.histogram(
            self.x_f64, weights=self.w_f64, bins=nbins, range=(xmin, xmax), flow=False
        )
        for i in range(self.w_f64.shape[1]):
            hm_res_i = hm_res_n.T[i]
            np_res_i, __ = np.histogram(
                self.x_f64, weights=self.w_f64.T[i], bins=nbins, range=(xmin, xmax)
            )
            assert np.allclose(hm_res_i, np_res_i)

    def test_var_mw_f32f32(self):
        hm_res_n, hm_res_e = hm.histogram(
            self.x_f32, weights=self.w_f32, bins=self.edges, flow=False
        )
        for i in range(self.w_f32.shape[1]):
            hm_res_i = hm_res_n.T[i]
            np_res_i, __ = np.histogram(self.x_f32, weights=self.w_f32.T[i], bins=self.edges)
            #assert np.allclose(np.around(hm_res_i, 2), np.around(np_res_i, 2))
            np.testing.assert_allclose(hm_res_i, np_res_i, rtol=1.0e-3)

    def test_var_mw_f64f64(self):
        hm_res_n, hm_res_e = hm.histogram(
            self.x_f64, weights=self.w_f64, bins=self.edges, flow=False
        )
        for i in range(self.w_f64.shape[1]):
            hm_res_i = hm_res_n.T[i]
            np_res_i, __ = np.histogram(self.x_f64, weights=self.w_f64.T[i], bins=self.edges)
            assert np.allclose(hm_res_i, np_res_i)
