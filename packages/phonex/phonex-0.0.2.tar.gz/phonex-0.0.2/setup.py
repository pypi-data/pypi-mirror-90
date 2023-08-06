from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='phonex',
      version='0.0.2',
      description='Phonex algorithm for python3',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/damiencorpataux/phonex',
      author='Damien Corpataux',
      author_email='d@mien.ch',
      license='MIT',
      packages=['phonex'],
      zip_safe=False)