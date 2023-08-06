/*
 * BSD 3-Clause License
 *
 * Copyright (c) 2019, Doug Davis
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice, this
 *    list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 *    this list of conditions and the following disclaimer in the documentation
 *    and/or other materials provided with the distribution.
 *
 * 3. Neither the name of the copyright holder nor the names of its
 *    contributors may be used to endorse or promote products derived from
 *    this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
 * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#if __STDC_VERSION__ < 199901L
#error "C99 or later required"
#endif

#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

/* Python */
#include <Python.h>

/* NumPy */
#include <numpy/arrayobject.h>

/* OpenMP */
#include <omp.h>

/* C */
#include <math.h>
#include <stdbool.h>
#include <stdlib.h>

static PyObject* f1dw(PyObject* self, PyObject* args);
static PyObject* v1dw(PyObject* self, PyObject* args);
static PyObject* omp_gmt(PyObject* self, PyObject* args);

static PyMethodDef module_methods[] = {
    {"_f1dw", f1dw, METH_VARARGS, ""},
    {"_v1dw", v1dw, METH_VARARGS, ""},
    {"_omp_get_max_threads", omp_gmt, METH_NOARGS, ""},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "_C",
    "Backend C module",
    -1,
    module_methods,
    NULL, /* m_slots */
    NULL, /* m_traverse */
    0,    /* m_clear */
    NULL  /* m_free */
};

PyMODINIT_FUNC PyInit__C(void) {
  PyObject* m = PyModule_Create(&moduledef);
  import_array();
  return m;
}

enum _status_codes {
  SC_SUCCESS = 0,
  SC_ERROR = 1,
};

typedef enum _status_codes status_t;

#define GET_BIN_INCLUDE_FLOW(bin, x, xmin, xmax, norm, nbins) \
  do {                                                        \
    if (x < xmin) {                                           \
      bin = 0;                                                \
    }                                                         \
    else if (x >= xmax) {                                     \
      bin = nbins - 1;                                        \
    }                                                         \
    else {                                                    \
      bin = (int)((x - xmin) * norm * nbins);                 \
    }                                                         \
  } while (0)

#define DEFINE_FIXED_FILL_FUNCTION_INCLUDE_FLOW(T1, T2, suffix)                    \
  static void fixed_fill_include_flow_##suffix(T1* x, T2* w, T2* counts, T2* vars, \
                                               long nx, int nbins, double norm,    \
                                               double xmin, double xmax) {         \
    Py_BEGIN_ALLOW_THREADS;                                                        \
    _Pragma("omp parallel if (nx > 1000)") {                                       \
      T2* counts_ot = (T2*)(calloc(nbins, sizeof(T2)));                            \
      T2* vars_ot = (T2*)(calloc(nbins, sizeof(T2)));                              \
      int bin;                                                                     \
      T2 weight;                                                                   \
      _Pragma("omp for nowait") for (long i = 0; i < nx; ++i) {                    \
        GET_BIN_INCLUDE_FLOW(bin, x[i], xmin, xmax, norm, nbins);                  \
        weight = w[i];                                                             \
        counts_ot[bin] += weight;                                                  \
        vars_ot[bin] += weight * weight;                                           \
      }                                                                            \
      _Pragma("omp critical") for (long i = 0; i < nbins; ++i) {                   \
        counts[i] += counts_ot[i];                                                 \
        vars[i] += vars_ot[i];                                                     \
      }                                                                            \
      free(counts_ot);                                                             \
      free(vars_ot);                                                               \
    }                                                                              \
    Py_END_ALLOW_THREADS;                                                          \
  }

#define DEFINE_FIXED_FILL_FUNCTION_EXCLUDE_FLOW(T1, T2, suffix)                    \
  static void fixed_fill_exclude_flow_##suffix(T1* x, T2* w, T2* counts, T2* vars, \
                                               long nx, int nbins, double norm,    \
                                               double xmin, double xmax) {         \
    Py_BEGIN_ALLOW_THREADS;                                                        \
    _Pragma("omp parallel if (nx > 1000)") {                                       \
      T2* counts_ot = (T2*)(calloc(nbins, sizeof(T2)));                            \
      T2* vars_ot = (T2*)(calloc(nbins, sizeof(T2)));                              \
      int bin;                                                                     \
      T2 weight;                                                                   \
      T1 val;                                                                      \
      _Pragma("omp for nowait") for (long i = 0; i < nx; ++i) {                    \
        val = x[i];                                                                \
        if (val < xmin || val > xmax) continue;                                    \
        bin = (long)((val - xmin) * norm * nbins);                                 \
        weight = w[i];                                                             \
        counts_ot[bin] += weight;                                                  \
        vars_ot[bin] += weight * weight;                                           \
      }                                                                            \
      _Pragma("omp critical") for (long i = 0; i < nbins; ++i) {                   \
        counts[i] += counts_ot[i];                                                 \
        vars[i] += vars_ot[i];                                                     \
      }                                                                            \
      free(counts_ot);                                                             \
      free(vars_ot);                                                               \
    }                                                                              \
    Py_END_ALLOW_THREADS;                                                          \
  }

#define DEFINE_VAR_FILL_FUNCTION_INCLUDE_FLOW(T1, T2, suffix)                         \
  static void var_fill_include_flow_##suffix(T1* x, T2* w, double* edges, T2* counts, \
                                             T2* vars, long nx, int nbins) {          \
    Py_BEGIN_ALLOW_THREADS;                                                           \
    _Pragma("omp parallel if (nx > 1000)") {                                          \
      T2* counts_ot = (T2*)(calloc(nbins, sizeof(T2)));                               \
      T2* vars_ot = (T2*)(calloc(nbins, sizeof(T2)));                                 \
      int bin;                                                                        \
      T2 weight;                                                                      \
      T1 val;                                                                         \
      _Pragma("omp for nowait") for (long i = 0; i < nx; ++i) {                       \
        val = x[i];                                                                   \
        bin = get_bin_bslb(edges, nbins, val);                                        \
        weight = w[i];                                                                \
        counts_ot[bin] += weight;                                                     \
        vars_ot[bin] += weight * weight;                                              \
      }                                                                               \
      _Pragma("omp critical") for (long i = 0; i < nbins; ++i) {                      \
        counts[i] += counts_ot[i];                                                    \
        vars[i] += vars_ot[i];                                                        \
      }                                                                               \
      free(counts_ot);                                                                \
      free(vars_ot);                                                                  \
    }                                                                                 \
    Py_END_ALLOW_THREADS;                                                             \
  }

#define DEFINE_VAR_FILL_FUNCTION_EXCLUDE_FLOW(T1, T2, suffix)                         \
  static void var_fill_exclude_flow_##suffix(T1* x, T2* w, double* edges, T2* counts, \
                                             T2* vars, long nx, int nbins) {          \
    Py_BEGIN_ALLOW_THREADS;                                                           \
    _Pragma("omp parallel if (nx > 1000)") {                                          \
      T2* counts_ot = (T2*)(calloc(nbins, sizeof(T2)));                               \
      T2* vars_ot = (T2*)(calloc(nbins, sizeof(T2)));                                 \
      int bin;                                                                        \
      T2 weight;                                                                      \
      _Pragma("omp for nowait") for (long i = 0; i < nx; ++i) {                       \
        if (x[i] < edges[0] || x[i] >= edges[nbins]) continue;                        \
        bin = get_bin_bslb(edges, nbins, x[i]);                                       \
        weight = w[i];                                                                \
        counts_ot[bin] += weight;                                                     \
        vars_ot[bin] += weight * weight;                                              \
      }                                                                               \
      _Pragma("omp critical") for (long i = 0; i < nbins; ++i) {                      \
        counts[i] += counts_ot[i];                                                    \
        vars[i] += vars_ot[i];                                                        \
      }                                                                               \
      free(counts_ot);                                                                \
      free(vars_ot);                                                                  \
    }                                                                                 \
    Py_END_ALLOW_THREADS;                                                             \
  }

static int get_bin_bslb(double* edges, int nbins, double x) {
  if (x < edges[0]) {
    return 0;
  }
  if (x >= edges[nbins]) {
    return nbins - 1;
  }
  int lower_bound = 0;
  int upper_bound = nbins;
  int mid;
  while (upper_bound - lower_bound > 1) {
    mid = (upper_bound + lower_bound) / 2;
    if (x >= edges[mid]) {
      lower_bound = mid;
    }
    else {
      upper_bound = mid;
    }
  }
  return lower_bound;
}

static void var_to_err(PyArrayObject* var, int nbins) {
  double* arr = (double*)PyArray_DATA(var);
  for (int i = 0; i < nbins; ++i) {
    arr[i] = sqrt(arr[i]);
  }
}

static void var_to_err_f(PyArrayObject* var, int nbins) {
  float* arr = (float*)PyArray_DATA(var);
  for (int i = 0; i < nbins; ++i) {
    arr[i] = sqrtf(arr[i]);
  }
}

static status_t calc_err(PyArrayObject* var, int nbins) {
  if (PyArray_TYPE(var) == NPY_FLOAT64) {
    var_to_err(var, nbins);
    return SC_SUCCESS;
  }
  if (PyArray_TYPE(var) == NPY_FLOAT32) {
    var_to_err_f(var, nbins);
    return SC_SUCCESS;
  }
  return SC_ERROR;
}

DEFINE_FIXED_FILL_FUNCTION_INCLUDE_FLOW(float, float, f32f32);
DEFINE_FIXED_FILL_FUNCTION_INCLUDE_FLOW(float, double, f32f64);
DEFINE_FIXED_FILL_FUNCTION_INCLUDE_FLOW(double, double, f64f64);
DEFINE_FIXED_FILL_FUNCTION_INCLUDE_FLOW(double, float, f64f32);
DEFINE_FIXED_FILL_FUNCTION_INCLUDE_FLOW(unsigned int, float, ui32f32);
DEFINE_FIXED_FILL_FUNCTION_INCLUDE_FLOW(unsigned int, double, ui32f64);
DEFINE_FIXED_FILL_FUNCTION_INCLUDE_FLOW(int, float, i32f32);
DEFINE_FIXED_FILL_FUNCTION_INCLUDE_FLOW(int, double, i32f64);

DEFINE_FIXED_FILL_FUNCTION_EXCLUDE_FLOW(float, float, f32f32);
DEFINE_FIXED_FILL_FUNCTION_EXCLUDE_FLOW(float, double, f32f64);
DEFINE_FIXED_FILL_FUNCTION_EXCLUDE_FLOW(double, double, f64f64);
DEFINE_FIXED_FILL_FUNCTION_EXCLUDE_FLOW(double, float, f64f32);
DEFINE_FIXED_FILL_FUNCTION_EXCLUDE_FLOW(unsigned int, float, ui32f32);
DEFINE_FIXED_FILL_FUNCTION_EXCLUDE_FLOW(unsigned int, double, ui32f64);
DEFINE_FIXED_FILL_FUNCTION_EXCLUDE_FLOW(int, float, i32f32);
DEFINE_FIXED_FILL_FUNCTION_EXCLUDE_FLOW(int, double, i32f64);

DEFINE_VAR_FILL_FUNCTION_INCLUDE_FLOW(float, float, f32f32);
DEFINE_VAR_FILL_FUNCTION_INCLUDE_FLOW(float, double, f32f64);
DEFINE_VAR_FILL_FUNCTION_INCLUDE_FLOW(double, double, f64f64);
DEFINE_VAR_FILL_FUNCTION_INCLUDE_FLOW(double, float, f64f32);
DEFINE_VAR_FILL_FUNCTION_INCLUDE_FLOW(unsigned int, float, ui32f32);
DEFINE_VAR_FILL_FUNCTION_INCLUDE_FLOW(unsigned int, double, ui32f64);
DEFINE_VAR_FILL_FUNCTION_INCLUDE_FLOW(int, float, i32f32);
DEFINE_VAR_FILL_FUNCTION_INCLUDE_FLOW(int, double, i32f64);

DEFINE_VAR_FILL_FUNCTION_EXCLUDE_FLOW(float, float, f32f32);
DEFINE_VAR_FILL_FUNCTION_EXCLUDE_FLOW(float, double, f32f64);
DEFINE_VAR_FILL_FUNCTION_EXCLUDE_FLOW(double, double, f64f64);
DEFINE_VAR_FILL_FUNCTION_EXCLUDE_FLOW(double, float, f64f32);
DEFINE_VAR_FILL_FUNCTION_EXCLUDE_FLOW(unsigned int, float, ui32f32);
DEFINE_VAR_FILL_FUNCTION_EXCLUDE_FLOW(unsigned int, double, ui32f64);
DEFINE_VAR_FILL_FUNCTION_EXCLUDE_FLOW(int, float, i32f32);
DEFINE_VAR_FILL_FUNCTION_EXCLUDE_FLOW(int, double, i32f64);

#define FILL_CALL_FIXED(IS1, IS2, T1, T2, suffix)                                      \
  do {                                                                                 \
    if (x_is_##IS1 && w_is_##IS2) {                                                    \
      fixed_fill_##suffix((T1*)PyArray_DATA(x), (T2*)PyArray_DATA(w),                  \
                          (T2*)PyArray_DATA(c), (T2*)PyArray_DATA(v), nx, nbins, norm, \
                          xmin, xmax);                                                 \
      return SC_SUCCESS;                                                               \
    }                                                                                  \
  } while (0)

static status_t fill_f1dw_exclude_flow(PyArrayObject* x, PyArrayObject* w,
                                       PyArrayObject* c, PyArrayObject* v, long nx,
                                       int nbins, double xmin, double xmax) {
  bool x_is_float64 = PyArray_TYPE(x) == NPY_FLOAT64;
  bool x_is_float32 = PyArray_TYPE(x) == NPY_FLOAT32;
  bool x_is_uint32 = PyArray_TYPE(x) == NPY_UINT32;
  bool x_is_int32 = PyArray_TYPE(x) == NPY_INT32;
  bool w_is_float64 = PyArray_TYPE(w) == NPY_FLOAT64;
  bool w_is_float32 = PyArray_TYPE(w) == NPY_FLOAT32;
  double norm = 1.0 / (xmax - xmin);
  FILL_CALL_FIXED(float32, float32, float, float, exclude_flow_f32f32);
  FILL_CALL_FIXED(float64, float32, double, float, exclude_flow_f64f32);
  FILL_CALL_FIXED(float32, float64, float, double, exclude_flow_f32f64);
  FILL_CALL_FIXED(float64, float64, double, double, exclude_flow_f64f64);
  FILL_CALL_FIXED(uint32, float32, unsigned int, float, exclude_flow_ui32f32);
  FILL_CALL_FIXED(int32, float32, int, float, exclude_flow_i32f32);
  FILL_CALL_FIXED(uint32, float64, unsigned int, double, exclude_flow_ui32f64);
  FILL_CALL_FIXED(int32, float64, int, double, exclude_flow_i32f64);
  return SC_ERROR;
}

static status_t fill_f1dw_include_flow(PyArrayObject* x, PyArrayObject* w,
                                       PyArrayObject* c, PyArrayObject* v, long nx,
                                       int nbins, double xmin, double xmax) {
  bool x_is_float64 = PyArray_TYPE(x) == NPY_FLOAT64;
  bool x_is_float32 = PyArray_TYPE(x) == NPY_FLOAT32;
  bool w_is_float64 = PyArray_TYPE(w) == NPY_FLOAT64;
  bool w_is_float32 = PyArray_TYPE(w) == NPY_FLOAT32;
  bool x_is_uint32 = PyArray_TYPE(x) == NPY_UINT32;
  bool x_is_int32 = PyArray_TYPE(x) == NPY_INT32;
  double norm = 1.0 / (xmax - xmin);
  FILL_CALL_FIXED(float32, float32, float, float, include_flow_f32f32);
  FILL_CALL_FIXED(float64, float32, double, float, include_flow_f64f32);
  FILL_CALL_FIXED(float32, float64, float, double, include_flow_f32f64);
  FILL_CALL_FIXED(float64, float64, double, double, include_flow_f64f64);
  FILL_CALL_FIXED(uint32, float32, unsigned int, float, include_flow_ui32f32);
  FILL_CALL_FIXED(int32, float32, int, float, include_flow_i32f32);
  FILL_CALL_FIXED(uint32, float64, unsigned int, double, include_flow_ui32f64);
  FILL_CALL_FIXED(int32, float64, int, double, include_flow_i32f64);
  return SC_ERROR;
}

#define FILL_CALL_VAR(IS1, IS2, T1, T2, suffix)                          \
  do {                                                                   \
    if (x_is_##IS1 && w_is_##IS2) {                                      \
      var_fill_##suffix((T1*)PyArray_DATA(x), (T2*)PyArray_DATA(w),      \
                        (double*)PyArray_DATA(ed), (T2*)PyArray_DATA(c), \
                        (T2*)PyArray_DATA(v), nx, nbins);                \
      return SC_SUCCESS;                                                 \
    }                                                                    \
  } while (0)

static status_t fill_v1dw_exclude_flow(PyArrayObject* x, PyArrayObject* w,
                                       PyArrayObject* ed, PyArrayObject* c,
                                       PyArrayObject* v, long nx, int nbins) {
  bool x_is_float64 = PyArray_TYPE(x) == NPY_FLOAT64;
  bool x_is_float32 = PyArray_TYPE(x) == NPY_FLOAT32;
  bool x_is_uint32 = PyArray_TYPE(x) == NPY_UINT32;
  bool x_is_int32 = PyArray_TYPE(x) == NPY_INT32;
  bool w_is_float64 = PyArray_TYPE(w) == NPY_FLOAT64;
  bool w_is_float32 = PyArray_TYPE(w) == NPY_FLOAT32;
  FILL_CALL_VAR(float32, float32, float, float, exclude_flow_f32f32);
  FILL_CALL_VAR(float64, float32, double, float, exclude_flow_f64f32);
  FILL_CALL_VAR(float32, float64, float, double, exclude_flow_f32f64);
  FILL_CALL_VAR(float64, float64, double, double, exclude_flow_f64f64);
  FILL_CALL_VAR(uint32, float32, unsigned int, float, exclude_flow_ui32f32);
  FILL_CALL_VAR(int32, float32, int, float, exclude_flow_i32f32);
  FILL_CALL_VAR(uint32, float64, unsigned int, double, exclude_flow_ui32f64);
  FILL_CALL_VAR(int32, float64, int, double, exclude_flow_i32f64);
  return SC_ERROR;
}

static status_t fill_v1dw_include_flow(PyArrayObject* x, PyArrayObject* w,
                                       PyArrayObject* ed, PyArrayObject* c,
                                       PyArrayObject* v, long nx, int nbins) {
  bool x_is_float64 = PyArray_TYPE(x) == NPY_FLOAT64;
  bool x_is_float32 = PyArray_TYPE(x) == NPY_FLOAT32;
  bool x_is_uint32 = PyArray_TYPE(x) == NPY_UINT32;
  bool x_is_int32 = PyArray_TYPE(x) == NPY_INT32;
  bool w_is_float64 = PyArray_TYPE(w) == NPY_FLOAT64;
  bool w_is_float32 = PyArray_TYPE(w) == NPY_FLOAT32;
  FILL_CALL_VAR(float32, float32, float, float, include_flow_f32f32);
  FILL_CALL_VAR(float64, float32, double, float, include_flow_f64f32);
  FILL_CALL_VAR(float32, float64, float, double, include_flow_f32f64);
  FILL_CALL_VAR(float64, float64, double, double, include_flow_f64f64);
  FILL_CALL_VAR(uint32, float32, unsigned int, float, include_flow_ui32f32);
  FILL_CALL_VAR(int32, float32, int, float, include_flow_i32f32);
  FILL_CALL_VAR(uint32, float64, unsigned int, double, include_flow_ui32f64);
  FILL_CALL_VAR(int32, float64, int, double, include_flow_i32f64);
  return SC_ERROR;
}

static PyObject* f1dw(PyObject* Py_UNUSED(self), PyObject* args) {
  long nx, nw;
  int nbins;
  int flow, as_err;
  double xmin, xmax;
  PyObject *x_obj, *w_obj, *counts_obj, *vars_obj;
  PyArrayObject *x_array, *w_array, *counts_array, *vars_array;
  npy_intp dims[1];

  if (!PyArg_ParseTuple(args, "OOiddpp", &x_obj, &w_obj, &nbins, &xmin, &xmax, &flow,
                        &as_err)) {
    PyErr_SetString(PyExc_TypeError, "Error parsing function input");
    return NULL;
  }

  x_array = (PyArrayObject*)PyArray_FROM_OF(x_obj, NPY_ARRAY_IN_ARRAY);
  w_array = (PyArrayObject*)PyArray_FROM_OF(w_obj, NPY_ARRAY_IN_ARRAY);

  if (x_array == NULL || w_array == NULL) {
    PyErr_SetString(PyExc_TypeError, "Could not read input data or weights as array");
    Py_XDECREF(x_array);
    Py_XDECREF(w_array);
    return NULL;
  }

  nx = (long)PyArray_DIM(x_array, 0);
  nw = (long)PyArray_DIM(w_array, 0);
  if (nx != nw) {
    PyErr_SetString(PyExc_ValueError, "data and weights must have equal length");
    Py_DECREF(x_array);
    Py_DECREF(w_array);
    return NULL;
  }

  dims[0] = nbins;
  counts_obj = PyArray_ZEROS(1, dims, PyArray_TYPE(w_array), 0);
  vars_obj = PyArray_ZEROS(1, dims, PyArray_TYPE(w_array), 0);

  if (counts_obj == NULL || vars_obj == NULL) {
    PyErr_SetString(PyExc_RuntimeError, "Could not build output");
    Py_DECREF(x_array);
    Py_DECREF(w_array);
    Py_XDECREF(counts_obj);
    Py_XDECREF(vars_obj);
    return NULL;
  }

  counts_array = (PyArrayObject*)counts_obj;
  vars_array = (PyArrayObject*)vars_obj;

  status_t fill_result = 1;
  if (flow) {
    fill_result = fill_f1dw_include_flow(x_array, w_array, counts_array, vars_array, nx,
                                         nbins, xmin, xmax);
  }
  else {
    fill_result = fill_f1dw_exclude_flow(x_array, w_array, counts_array, vars_array, nx,
                                         nbins, xmin, xmax);
  }
  if (fill_result != SC_SUCCESS) {
    PyErr_SetString(PyExc_TypeError, "dtype of input arrays unsupported");
    Py_DECREF(x_array);
    Py_DECREF(w_array);
    Py_DECREF(counts_obj);
    Py_DECREF(vars_obj);
    return NULL;
  }

  if (as_err) {
    status_t calc_err_result = calc_err(vars_array, nbins);
    if (calc_err_result != SC_SUCCESS) {
      PyErr_SetString(PyExc_TypeError, "dtype of input arrays unsupported");
      Py_DECREF(x_array);
      Py_DECREF(w_array);
      Py_DECREF(counts_obj);
      Py_DECREF(vars_obj);
      return NULL;
    }
  }

  Py_DECREF(x_array);
  Py_DECREF(w_array);

  return Py_BuildValue("OO", counts_obj, vars_obj);
}

static PyObject* v1dw(PyObject* Py_UNUSED(self), PyObject* args) {
  long nx, nw, ne;
  int nbins;
  int flow, as_err;
  PyObject *e_obj, *x_obj, *w_obj, *counts_obj, *vars_obj;
  PyArrayObject *e_array, *x_array, *w_array, *counts_array, *vars_array;
  npy_intp dims[1];

  if (!PyArg_ParseTuple(args, "OOOpp", &x_obj, &w_obj, &e_obj, &flow, &as_err)) {
    PyErr_SetString(PyExc_TypeError, "Error parsing function input");
    return NULL;
  }

  x_array = (PyArrayObject*)PyArray_FROM_OF(x_obj, NPY_ARRAY_IN_ARRAY);
  w_array = (PyArrayObject*)PyArray_FROM_OF(w_obj, NPY_ARRAY_IN_ARRAY);
  e_array = (PyArrayObject*)PyArray_FROM_OTF(e_obj, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);

  if (x_array == NULL || w_array == NULL || e_array == NULL) {
    PyErr_SetString(PyExc_TypeError, "Could not read input data or weights as array");
    Py_XDECREF(x_array);
    Py_XDECREF(w_array);
    Py_XDECREF(e_array);
    return NULL;
  }

  nx = (long)PyArray_DIM(x_array, 0);
  nw = (long)PyArray_DIM(w_array, 0);
  ne = (long)PyArray_DIM(e_array, 0);
  nbins = ne - 1;
  if (nx != nw) {
    PyErr_SetString(PyExc_ValueError, "data and weights must have equal length");
    Py_DECREF(x_array);
    Py_DECREF(w_array);
    Py_DECREF(e_array);
    return NULL;
  }

  dims[0] = nbins;
  counts_obj = PyArray_ZEROS(1, dims, PyArray_TYPE(w_array), 0);
  vars_obj = PyArray_ZEROS(1, dims, PyArray_TYPE(w_array), 0);

  if (counts_obj == NULL || vars_obj == NULL) {
    PyErr_SetString(PyExc_RuntimeError, "Could not build output");
    Py_DECREF(x_array);
    Py_DECREF(w_array);
    Py_DECREF(e_array);
    Py_XDECREF(counts_obj);
    Py_XDECREF(vars_obj);
    return NULL;
  }

  counts_array = (PyArrayObject*)counts_obj;
  vars_array = (PyArrayObject*)vars_obj;

  status_t fill_result;
  if (flow) {
    fill_result = fill_v1dw_include_flow(x_array, w_array, e_array, counts_array,
                                         vars_array, nx, nbins);
  }
  else {
    fill_result = fill_v1dw_exclude_flow(x_array, w_array, e_array, counts_array,
                                         vars_array, nx, nbins);
  }
  if (fill_result != SC_SUCCESS) {
    PyErr_SetString(PyExc_TypeError, "dtype of input arrays unsupported");
    Py_DECREF(x_array);
    Py_DECREF(w_array);
    Py_DECREF(e_array);
    Py_DECREF(counts_obj);
    Py_DECREF(vars_obj);
    return NULL;
  }

  if (as_err) {
    status_t calc_err_result = calc_err(vars_array, nbins);
    if (calc_err_result != SC_SUCCESS) {
      PyErr_SetString(PyExc_TypeError, "dtype of input arrays unsupported");
      Py_DECREF(x_array);
      Py_DECREF(w_array);
      Py_DECREF(e_array);
      Py_DECREF(counts_obj);
      Py_DECREF(vars_obj);
      return NULL;
    }
  }

  Py_DECREF(x_array);
  Py_DECREF(w_array);
  Py_DECREF(e_array);

  return Py_BuildValue("OO", counts_obj, vars_obj);
}

static PyObject* omp_gmt(PyObject* Py_UNUSED(self), PyObject* Py_UNUSED(args)) {
  long nthreads = omp_get_max_threads();
  return PyLong_FromLong(nthreads);
}
