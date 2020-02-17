from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(name='slic app',
      ext_modules=cythonize("_slic.pyx"),
      include_dirs=[numpy.get_include()])
