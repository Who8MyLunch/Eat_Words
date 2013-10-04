
from setuptools import setup, find_packages

version = '2012.05.24'

# Do it.
setup(name='eat_words',
      packages=find_packages(),
      package_data={'': ['*.yml', '*.png', '*.txt']},

      # Metadata
      version=version,
      author='Pierre V. Villeneuve',
      author_email='pierre.villeneuve@gmail.com',
      description='Play a nice game of scabble',
      )
