from setuptools import find_packages, setup

setup(
    name='src',
    packages=find_packages(),
    version='0.1.0',
    description='Predicting neurodegeneration from global proteomics',
    author='Ryan B Patterson',
    license='GPLv3',
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-mypy'],
)
