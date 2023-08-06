# HINT: Go back to the object-oriented programming lesson "Putting Code on PyPi" and "Exercise: Upload to PyPi"

# HINT: Here is an example of a setup.py file
# https://packaging.python.org/tutorials/packaging-projects/

from setuptools import setup

setup(name='gaussian_probability',
      version='0.1',
      description='Gaussian distirbution',
      author = 'Yessy Marie',
      packages=['gaussian_probability'],
      zip_safe=False)