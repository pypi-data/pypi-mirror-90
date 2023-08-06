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
#include <stdlib.h>

static PyObject* peek_2d(PyObject* self, PyObject* args);

static PyMethodDef module_methods[] = {
    {"peek_2d", peek_2d, METH_VARARGS, "play with 2d array"}, {NULL, NULL, 0, NULL}};

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "_exp",
    "Experimental C module",
    -1,
    module_methods,
    NULL, /* m_slots */
    NULL, /* m_traverse */
    0,    /* m_clear */
    NULL  /* m_free */
};

PyMODINIT_FUNC PyInit__exp(void) {
  PyObject* m = PyModule_Create(&moduledef);
  import_array();
  return m;
}

static PyObject* peek_2d(PyObject* Py_UNUSED(self), PyObject* args) {
  // long nx;
  int nbins;
  double xmin, xmax;
  // double norm;

  PyObject* x;
  PyArrayObject* x_arr;
  PyObject* weights;
  PyArrayObject* weights_arr;
  PyArray_Descr* weights_descr;
  int weights_ndim;
  npy_intp* weights_dims;

  int weights_nrows;
  int weights_ncols;

  if (!PyArg_ParseTuple(args, "OOidd", &x, &weights, &nbins, &xmin, &xmax)) {
    PyErr_SetString(PyExc_TypeError, "Error parsing function input");
    return NULL;
  }

  x_arr = (PyArrayObject*)PyArray_FROM_OF(x, NPY_ARRAY_IN_ARRAY);
  weights_arr = (PyArrayObject*)PyArray_FROM_OF(weights, NPY_ARRAY_IN_ARRAY);

  weights_descr = PyArray_DESCR(weights_arr);
  weights_ndim = PyArray_NDIM(weights_arr);
  weights_dims = PyArray_DIMS(weights_arr);

  weights_nrows = weights_dims[0];
  weights_ncols = weights_dims[1];

  /*
  for (int irow = 0; irow < nrows; ++irow) {
    double val = arrd[col + irow * ncols];
    printf("%f\n", val);
  }
  */

  return Py_BuildValue("");
}
