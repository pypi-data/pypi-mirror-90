import setuptools
from setuptools import version

setuptools.setup(
  name='crazy_joe',
  version="0.1.1",
  description='',
  packages=setuptools.find_packages('src'),
  package_dir={'': 'src'},
  install_requires=[
    'numpy',
    'pytest'
  ]
)