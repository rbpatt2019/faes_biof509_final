from setuptools import find_packages, setup
import subprocess

__version__ = subprocess.check_output(["git", "describe", "--abbrev=0"]).strip()
__version__ = str(__version__)[2:-1]

setup(
    name="src",
    packages=find_packages(),
    version=__version__,
    description="Predicting neurodegeneration from global proteomics",
    author="Ryan B Patterson",
    license="GPLv3",
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-mypy", "pytest-instafail"],
)
