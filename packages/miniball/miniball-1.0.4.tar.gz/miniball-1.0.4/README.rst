.. image:: https://img.shields.io/pypi/v/miniball.svg
   :target: https://pypi.org/project/miniball/
   :alt: miniball on PyPI

.. image:: https://travis-ci.com/marmakoide/miniball.svg?branch=master
   :target: https://travis-ci.com/marmakoide/miniball
   :alt: miniball on TravisCI
   
.. image:: https://img.shields.io/badge/license-MIT-green.svg
   :target: https://github.com/marmakoide/miniball/blob/master/LICENSE
   :alt: MIT License badge

========
miniball
========

A Python module to efficiently compute the smallest bounding ball of a point 
set, in arbitrary number of dimensions.

The algorithm runs in approximatively linear time in respects to the number of
input points. This is NOT a derivative nor a port of 
`Bernd Gaertner's C++ library <https://people.inf.ethz.ch/gaertner/subdir/software/miniball.html>`__.

This project is licensed under the MIT License

Requirements
============

miniball 1.0 requires

* Python 2.7, >=3.4
* Numpy

Installation
============

.. code-block:: console

	$ pip install miniball


Usage
=====

Here is how you can get the smallest bounding ball of a set of points S

.. code-block:: pycon

	>>> import numpy
	>>> import miniball
	>>> S = numpy.random.randn(100, 2)
	>>> C, r2 = miniball.get_bounding_ball(S)

The center of the bounding ball is C, its radius is the square root of r2. 
The input coordinates S can be integer, they will automatically cast to floating
point internally.

And that's it ! miniball does only one thing with one function.

Implementation notes
====================

The algorithm implemented is Welzl's algorithm. It is a pure Python implementation,
it is not a binding of the popular C++ package `Bernd Gaertner's miniball <https://people.inf.ethz.ch/gaertner/subdir/software/miniball.html>`__.

The algorithm, although often presented in its recursive form, is here implemented
in an iterative fashion. Python have an hard-coded recursion limit, therefore
a recursive implementation of Welzl's algorithm would have an artificially limited
number of point it could process.

Authors
=======

* **Alexandre Devert** - *Initial work* - [marmakoide](https://github.com/marmakoide)

License
=======

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
