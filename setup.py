
from setuptools import setup, find_packages


version = '2019.6.18'

dependencies = ['numpy', 'ordered_namespace']


setuptools.setup(install_requires=dependencies,
                 package_data={'': ['*.yml', '*.png', '*.txt']},
                 include_package_data=True,
                 packages=setuptools.find_packages(),
                 version=version)
