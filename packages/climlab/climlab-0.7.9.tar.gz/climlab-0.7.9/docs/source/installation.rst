.. highlight:: rst

Installation
============

Installing pre-built binaries with conda (Mac OSX, Linux, and Windows)
----------------------------------------------------------------------
By far the simplest and recommended way to install ``climlab`` is using conda_
(which is the wonderful package manager that comes with `Anaconda Python`_).

You can install CLIMLAB and all its dependencies with::

    conda install -c conda-forge climlab

Or (recommended) add ``conda-forge`` to your conda channels with::

    conda config --add channels conda-forge

and then simply do::

    conda install climlab

Binaries are available for OSX, Linux, and Windows.

For Windows, builds are available for 64-bit versions of Python 3.5 and Python 3.6, and will require numpy 1.14 or later.

Installing from source
----------------------

*This will only work if you have a properly configured Fortran compiler installed and available.*

If you do not use conda, it is **possible** to install CLIMLAB from source with::

    pip install climlab

which will download the latest stable release from the `pypi repository`_ and trigger the build process.

Alternatively, clone the source code repository with::

    git clone https://github.com/brian-rose/climlab.git

and, from the ``climlab`` directory, do::

    python -m pip install . --no-deps -vv

Please see :ref:`Contributing to CLIMLAB` for more details about how to build from source.

Installing from source without a Fortran compiler
-------------------------------------------------

Many parts of CLIMLAB are written in pure Python and should work on any system. Fortran builds are necessary for the Emanuel convection scheme and the RRTMG and CAM3 radiation schemes.

If you obtain the source code repository and do this from the repository root::

    python setup.py install

You should then find that you can still::

    import climlab

and use most of the package. You will see warning messages about the missing components.

.. _conda: https://conda.io/docs/
.. _`Anaconda Python`: https://www.continuum.io/downloads
.. _`pypi repository`: https://pypi.python.org




Source Code
=============

Stables releases as well as the current development version can be found on github:

  * `Stable Releases <https://github.com/brian-rose/climlab/releases>`_
  * `Development Version <https://github.com/brian-rose/climlab>`_


Dependencies
================

These are handled automatically if you install with conda_.

Required
------------
- Python 2.7, 3.6, 3.7, 3.8
- numpy
- scipy
- xarray (for data i/o)
- attrdict
- future
- requests

Recommended for full functionality
----------------------------------
- numba (used for acceleration of some components)
- pytest (to run the automated tests, important if you are developing new code)

`Anaconda Python`_ is highly recommended and will provide everything you need.
See "Installing pre-built binaries with conda" above.
