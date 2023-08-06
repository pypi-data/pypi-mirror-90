Quick Start
===========

First use:

.. code-block:: python

   >>> import histmp
   >>> x = np.random.randn(10000)
   >>> w = np.random.uniform(0.5, 0.8, x.shape[0])
   >>> h, err = histmp.histogram(x, bins=20, range=(-3, 3), weights=w)
