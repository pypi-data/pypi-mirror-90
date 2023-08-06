#!/usr/bin/env python
import setuptools

__version__ = "1.0.8"


CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.2",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Topic :: Scientific/Engineering :: Information Analysis",
    "Topic :: Scientific/Engineering :: Mathematics",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

setuptools.setup(
    name="somtime",
    version=__version__,
    description="Python implementation of Self Organizing Map with capability to use Dynamic Time Warping (DTW) as a distance measure.",
    long_description = "Self Organizing Map with capability to use Dynamic Time Warping (DTW) as a distance measure for time series based data. For non time-series data Euclidean distance can be used by setting window size to 0. The SOM can be used for both univariate time series data and multi-variate time series data.",
    author="A. Javed",
    author_email="alijaved@live.com",
    packages=setuptools.find_packages(),
    zip_safe=True,
    license="",
    download_url = "https://github.com/ali-javed/somtime/archive/1.0.8.tar.gz",
    url="https://github.com/ali-javed/somtime",
    install_requires=['numpy','matplotlib']
)
