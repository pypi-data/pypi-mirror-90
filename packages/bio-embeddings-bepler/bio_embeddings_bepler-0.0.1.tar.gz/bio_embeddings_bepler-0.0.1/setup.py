from distutils.core import setup

import numpy as np
from setuptools import find_packages
from Cython.Build import cythonize

setup(
    name="bio_embeddings_bepler",
    version="0.0.1",
    packages=find_packages(),
    ext_modules=cythonize(["bepler/metrics.pyx", "bepler/alignment.pyx"]),
    include_dirs=[np.get_include()],
)
