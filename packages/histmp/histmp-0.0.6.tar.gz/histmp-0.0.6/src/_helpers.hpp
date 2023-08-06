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

#ifndef HISTMP__HELPERS_H
#define HISTMP__HELPERS_H

#include <algorithm>
#include <cmath>
#include <iterator>
#include <vector>

namespace helpers {

/// get the bin index for a fixed with histsgram with x potentially outside range
template <typename T1, typename T2, typename T3>
inline T2 get_bin(T1 x, T2 nbins, T3 xmin, T3 xmax, T3 norm) {
  if (x < xmin) {
    return static_cast<T2>(0);
  }
  else if (x >= xmax) {
    return nbins - 1;
  }
  return static_cast<T2>((x - xmin) * norm * nbins);
}

/// get the bin index for a fixed with histogram assuming x in the range
template <typename T1, typename T2, typename T3>
inline T2 get_bin(T1 x, T2 nbins, T3 xmin, T3 norm) {
  return static_cast<T2>((x - xmin) * norm * nbins);
}

/// get the bin index for a variable width histogram with x potentially outside range
template <typename T1, typename T2, typename T3>
inline T2 get_bin(T1 x, T2 nbins, const std::vector<T3>& edges) {
  if (x < edges.front()) {
    return static_cast<T2>(0);
  }
  else if (x >= edges.back()) {
    return nbins - 1;
  }
  else {
    auto s = static_cast<T2>(std::distance(
        std::begin(edges), std::lower_bound(std::begin(edges), std::end(edges), x)));
    return s - 1;
  }
}

/// get the bin index for a variable width histogram assuming x is in the range
template <typename T1, typename T2>
inline int get_bin(T1 x, const std::vector<T2>& edges) {
  auto s = static_cast<int>(std::distance(
      std::begin(edges), std::lower_bound(std::begin(edges), std::end(edges), x)));
  return s - 1;
}

/// convert width width binning histogram result into a density histogram
template <typename T>
inline void densify(T* counts, T* vars, int nbins, double xmin, double xmax) {
  T integral = 0.0;
  T sum_vars = 0.0;
  double bin_width = (xmax - xmin) / nbins;
  for (int i = 0; i < nbins; ++i) {
    integral += counts[i];
    sum_vars += vars[i];
  }
  double f1 = 1.0 / std::pow(bin_width * integral, 2);
  for (int i = 0; i < nbins; ++i) {
    vars[i] = f1 * (vars[i] + (std::pow(counts[i] / integral, 2) * sum_vars));
    counts[i] = counts[i] / bin_width / integral;
  }
}

/// convert variable width binning histogram result into a density histogram
template <typename T1, typename T2>
inline void densify(T1* counts, T1* vars, const T2* edges, int nbins) {
  T1 integral = 0.0;
  T1 sum_vars = 0.0;
  std::vector<T2> bin_widths(nbins);
  for (int i = 0; i < nbins; ++i) {
    integral += counts[i];
    sum_vars += vars[i];
    bin_widths[i] = edges[i + 1] - edges[i];
  }
  for (int i = 0; i < nbins; ++i) {
    vars[i] = (vars[i] + (std::pow(counts[i] / integral, 2) * sum_vars)) /
              std::pow(bin_widths[i] * integral, 2);
    counts[i] = counts[i] / bin_widths[i] / integral;
  }
}

/// sqrt variance array entries to convert it to standard error
template <typename T,
          typename = typename std::enable_if<std::is_arithmetic<T>::value>::type>
inline void array_sqrt(T* arr, int n) {
  for (int i = 0; i < n; ++i) {
    arr[i] = std::sqrt(arr[i]);
  }
}

}  // namespace helpers

#endif
