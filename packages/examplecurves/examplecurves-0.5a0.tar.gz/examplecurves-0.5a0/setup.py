# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="examplecurves",
    author="David Scheliga",
    author_email="david.scheliga@ivw.uni-kl.de",
    url="https://gitlab.com/david.scheliga/examplecurves",
    project_urls={
        "Documentation": "https://examplecurves.readthedocs.io/en/latest/",
        "Source Code Repository": "https://gitlab.com/david.scheliga/examplecurves",
    },
    description="Module for providing exemplary, reproducible curves for testing and debugging.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GNU General Public License v3 (GPLv3)",
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3",
    ],
    keywords="curve, testing, debugging, engineering",
    python_requires=">=3.6",
    install_requires=["importlib_resources;python_version=='3.6'"],
    extras_require={"dev": ["doctestprinter", "Sphinx"]},
    packages=find_packages(),
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    include_package_data=True,
)
