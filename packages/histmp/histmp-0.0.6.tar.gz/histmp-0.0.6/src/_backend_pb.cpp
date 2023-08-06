// BSD 3-Clause License
//
// Copyright (c) 2019, Doug Davis
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
//
// 1. Redistributions of source code must retain the above copyright notice, this
//    list of conditions and the following disclaimer.
//
// 2. Redistributions in binary form must reproduce the above copyright notice,
//    this list of conditions and the following disclaimer in the documentation
//    and/or other materials provided with the distribution.
//
// 3. Neither the name of the copyright holder nor the names of its
//    contributors may be used to endorse or promote products derived from
//    this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
// AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
// DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
// FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
// DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
// SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
// CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
// OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
// OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

// Local
#include "_helpers.hpp"

// OpenMP
#include <omp.h>

// pybind11
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>

namespace py = pybind11;

template <typename T1, typename T2>
py::tuple f1dmw(const py::array_t<T1>& x, const py::array_t<T2>& w, std::size_t nbins,
                double xmin, double xmax, bool flow, bool as_err) {
  std::size_t ndata = static_cast<std::size_t>(x.shape(0));
  std::size_t nweightvars = static_cast<std::size_t>(w.shape(1));
  double norm = 1.0 / (xmax - xmin);
  py::array_t<T2> counts({static_cast<std::size_t>(nbins), nweightvars});
  py::array_t<T2> vars({static_cast<std::size_t>(nbins), nweightvars});
  std::memset(counts.mutable_data(), 0, sizeof(T2) * nbins * nweightvars);
  std::memset(vars.mutable_data(), 0, sizeof(T2) * nbins * nweightvars);
  auto counts_proxy = counts.template mutable_unchecked<2>();
  auto vars_proxy = vars.template mutable_unchecked<2>();
  auto x_proxy = x.template unchecked<1>();
  auto w_proxy = w.template unchecked<2>();

  if (flow) {
#pragma omp parallel if (ndata > 1000)
    {
      std::vector<std::vector<T2>> counts_ot;
      std::vector<std::vector<T2>> vars_ot;
      for (std::size_t i = 0; i < nweightvars; ++i) {
        counts_ot.emplace_back(nbins, 0);
        vars_ot.emplace_back(nbins, 0);
      }
#pragma omp for nowait
      for (std::size_t i = 0; i < ndata; i++) {
        auto bin = helpers::get_bin(x_proxy(i), nbins, xmin, xmax, norm);
        for (std::size_t j = 0; j < nweightvars; j++) {
          T2 weight = w_proxy(i, j);
          counts_ot[j][bin] += weight;
          vars_ot[j][bin] += weight * weight;
        }
      }
#pragma omp critical
      for (std::size_t i = 0; i < nbins; ++i) {
        for (std::size_t j = 0; j < nweightvars; ++j) {
          counts_proxy(i, j) += counts_ot[j][i];
          vars_proxy(i, j) += vars_ot[j][i];
        }
      }
    }
  }

  else {
#pragma omp parallel if (ndata > 1000)
    {
      std::vector<std::vector<T2>> counts_ot;
      std::vector<std::vector<T2>> vars_ot;
      for (std::size_t i = 0; i < nweightvars; ++i) {
        counts_ot.emplace_back(nbins, 0);
        vars_ot.emplace_back(nbins, 0);
      }
#pragma omp for nowait
      for (std::size_t i = 0; i < ndata; i++) {
        T1 x_i = x_proxy(i);
        if (x_i < xmin) continue;
        if (x_i >= xmax) continue;
        auto bin = helpers::get_bin(x_proxy(i), nbins, xmin, norm);
        for (std::size_t j = 0; j < nweightvars; j++) {
          T2 weight = w_proxy(i, j);
          counts_ot[j][bin] += weight;
          vars_ot[j][bin] += weight * weight;
        }
      }
#pragma omp critical
      for (std::size_t i = 0; i < nbins; ++i) {
        for (std::size_t j = 0; j < nweightvars; ++j) {
          counts_proxy(i, j) += counts_ot[j][i];
          vars_proxy(i, j) += vars_ot[j][i];
        }
      }
    }
  }

  if (as_err) {
    helpers::array_sqrt(vars.mutable_data(), nbins * nweightvars);
  }

  return py::make_tuple(counts, vars);
}

template <typename T1, typename T2>
py::tuple v1dmw(
    const py::array_t<T1>& x, const py::array_t<T2>& w,
    const py::array_t<double, py::array::c_style | py::array::forcecast>& edges,
    bool flow, bool as_err) {
  std::size_t ndata = static_cast<std::size_t>(x.shape(0));
  std::size_t nweightvars = static_cast<std::size_t>(w.shape(1));
  std::size_t nedges = static_cast<std::size_t>(edges.shape(0));
  std::size_t nbins = nedges - 1;
  std::vector<T1> edges_v(nedges);
  edges_v.assign(edges.data(), edges.data() + nedges);

  py::array_t<T2> counts({static_cast<std::size_t>(nbins), nweightvars});
  py::array_t<T2> vars({static_cast<std::size_t>(nbins), nweightvars});
  std::memset(counts.mutable_data(), 0, sizeof(T2) * nbins * nweightvars);
  std::memset(vars.mutable_data(), 0, sizeof(T2) * nbins * nweightvars);
  auto counts_proxy = counts.template mutable_unchecked<2>();
  auto vars_proxy = vars.template mutable_unchecked<2>();
  auto x_proxy = x.template unchecked<1>();
  auto w_proxy = w.template unchecked<2>();

  if (flow) {
#pragma omp parallel if (ndata > 1000)
    {
      std::vector<std::vector<T2>> counts_ot;
      std::vector<std::vector<T2>> vars_ot;
      for (std::size_t i = 0; i < nweightvars; ++i) {
        counts_ot.emplace_back(nbins, 0);
        vars_ot.emplace_back(nbins, 0);
      }
#pragma omp for nowait
      for (std::size_t i = 0; i < ndata; i++) {
        auto bin = helpers::get_bin(x_proxy(i), nbins, edges_v);
        for (std::size_t j = 0; j < nweightvars; j++) {
          T2 weight = w_proxy(i, j);
          counts_ot[j][bin] += weight;
          vars_ot[j][bin] += weight * weight;
        }
      }
#pragma omp critical
      for (std::size_t i = 0; i < nbins; ++i) {
        for (std::size_t j = 0; j < nweightvars; ++j) {
          counts_proxy(i, j) += counts_ot[j][i];
          vars_proxy(i, j) += vars_ot[j][i];
        }
      }
    }
  }

  else {
#pragma omp parallel if (ndata > 1000)
    {
      std::vector<std::vector<T2>> counts_ot;
      std::vector<std::vector<T2>> vars_ot;
      for (std::size_t i = 0; i < nweightvars; ++i) {
        counts_ot.emplace_back(nbins, 0);
        vars_ot.emplace_back(nbins, 0);
      }
#pragma omp for nowait
      for (std::size_t i = 0; i < ndata; i++) {
        T1 x_i = x_proxy(i);
        if (x_i < edges_v.front()) continue;
        if (x_i >= edges_v.back()) continue;
        auto bin = helpers::get_bin(x_proxy(i), edges_v);
        for (std::size_t j = 0; j < nweightvars; j++) {
          T2 weight = w_proxy(i, j);
          counts_ot[j][bin] += weight;
          vars_ot[j][bin] += weight * weight;
        }
      }
#pragma omp critical
      for (std::size_t i = 0; i < nbins; ++i) {
        for (std::size_t j = 0; j < nweightvars; ++j) {
          counts_proxy(i, j) += counts_ot[j][i];
          vars_proxy(i, j) += vars_ot[j][i];
        }
      }
    }
  }

  if (as_err) {
    helpers::array_sqrt(vars.mutable_data(), nbins * nweightvars);
  }

  return py::make_tuple(counts, vars);
}

PYBIND11_MODULE(_CPP_PB, m) {
  m.doc() = "pybind11 backend";

  using namespace pybind11::literals;

  m.def("_f1dmw", &f1dmw<float, double>, "x"_a.noconvert(), "weights"_a.noconvert(),
        "nbins"_a, "xmin"_a, "xmax"_a, "flow"_a, "as_err"_a);

  m.def("_f1dmw", &f1dmw<float, float>, "x"_a.noconvert(), "weights"_a.noconvert(),
        "nbins"_a, "xmin"_a, "xmax"_a, "flow"_a, "as_err"_a);

  m.def("_f1dmw", &f1dmw<double, double>, "x"_a.noconvert(), "weights"_a.noconvert(),
        "nbins"_a, "xmin"_a, "xmax"_a, "flow"_a, "as_err"_a);

  m.def("_f1dmw", &f1dmw<double, float>, "x"_a.noconvert(), "weights"_a.noconvert(),
        "nbins"_a, "xmin"_a, "xmax"_a, "flow"_a, "as_err"_a);

  m.def("_f1dmw", &f1dmw<int, double>, "x"_a.noconvert(), "weights"_a.noconvert(),
        "nbins"_a, "xmin"_a, "xmax"_a, "flow"_a, "as_err"_a);

  m.def("_f1dmw", &f1dmw<int, float>, "x"_a.noconvert(), "weights"_a.noconvert(),
        "nbins"_a, "xmin"_a, "xmax"_a, "flow"_a, "as_err"_a);

  m.def("_f1dmw", &f1dmw<int, double>, "x"_a.noconvert(), "weights"_a.noconvert(),
        "nbins"_a, "xmin"_a, "xmax"_a, "flow"_a, "as_err"_a);

  m.def("_f1dmw", &f1dmw<int, float>, "x"_a.noconvert(), "weights"_a.noconvert(),
        "nbins"_a, "xmin"_a, "xmax"_a, "flow"_a, "as_err"_a);

  m.def("_f1dmw", &f1dmw<unsigned int, double>, "x"_a.noconvert(),
        "weights"_a.noconvert(), "nbins"_a, "xmin"_a, "xmax"_a, "flow"_a, "as_err"_a);

  m.def("_f1dmw", &f1dmw<unsigned int, float>, "x"_a.noconvert(),
        "weights"_a.noconvert(), "nbins"_a, "xmin"_a, "xmax"_a, "flow"_a, "as_err"_a);

  m.def("_f1dmw", &f1dmw<long, double>, "x"_a.noconvert(), "weights"_a.noconvert(),
        "nbins"_a, "xmin"_a, "xmax"_a, "flow"_a, "as_err"_a);

  m.def("_f1dmw", &f1dmw<long, float>, "x"_a.noconvert(), "weights"_a.noconvert(),
        "nbins"_a, "xmin"_a, "xmax"_a, "flow"_a, "as_err"_a);

  m.def("_f1dmw", &f1dmw<unsigned long, double>, "x"_a.noconvert(),
        "weights"_a.noconvert(), "nbins"_a, "xmin"_a, "xmax"_a, "flow"_a, "as_err"_a);

  m.def("_f1dmw", &f1dmw<unsigned long, float>, "x"_a.noconvert(),
        "weights"_a.noconvert(), "nbins"_a, "xmin"_a, "xmax"_a, "flow"_a, "as_err"_a);

  m.def("_v1dmw", &v1dmw<float, double>, "x"_a.noconvert(), "weights"_a.noconvert(),
        "edges"_a, "flow"_a, "as_err"_a);

  m.def("_v1dmw", &v1dmw<float, float>, "x"_a.noconvert(), "weights"_a.noconvert(),
        "edges"_a, "flow"_a, "as_err"_a);

  m.def("_v1dmw", &v1dmw<double, double>, "x"_a.noconvert(), "weights"_a.noconvert(),
        "edges"_a, "flow"_a, "as_err"_a);

  m.def("_v1dmw", &v1dmw<double, float>, "x"_a.noconvert(), "weights"_a.noconvert(),
        "edges"_a, "flow"_a, "as_err"_a);

  m.def("_v1dmw", &v1dmw<int, double>, "x"_a.noconvert(), "weights"_a.noconvert(),
        "edges"_a, "flow"_a, "as_err"_a);

  m.def("_v1dmw", &v1dmw<int, float>, "x"_a.noconvert(), "weights"_a.noconvert(),
        "edges"_a, "flow"_a, "as_err"_a);

  m.def("_v1dmw", &v1dmw<int, double>, "x"_a.noconvert(), "weights"_a.noconvert(),
        "edges"_a, "flow"_a, "as_err"_a);

  m.def("_v1dmw", &v1dmw<int, float>, "x"_a.noconvert(), "weights"_a.noconvert(),
        "edges"_a, "flow"_a, "as_err"_a);

  m.def("_v1dmw", &v1dmw<unsigned int, double>, "x"_a.noconvert(),
        "weights"_a.noconvert(), "edges"_a, "flow"_a, "as_err"_a);

  m.def("_v1dmw", &v1dmw<unsigned int, float>, "x"_a.noconvert(),
        "weights"_a.noconvert(), "edges"_a, "flow"_a, "as_err"_a);

  m.def("_v1dmw", &v1dmw<long, double>, "x"_a.noconvert(), "weights"_a.noconvert(),
        "edges"_a, "flow"_a, "as_err"_a);

  m.def("_v1dmw", &v1dmw<long, float>, "x"_a.noconvert(), "weights"_a.noconvert(),
        "edges"_a, "flow"_a, "as_err"_a);

  m.def("_v1dmw", &v1dmw<unsigned long, double>, "x"_a.noconvert(),
        "weights"_a.noconvert(), "edges"_a, "flow"_a, "as_err"_a);

  m.def("_v1dmw", &v1dmw<unsigned long, float>, "x"_a.noconvert(),
        "weights"_a.noconvert(), "edges"_a, "flow"_a, "as_err"_a);
}
