try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='pypkm',
      version='0.0',
      description='PKM File Manipulation',
      author='Patrick Jacobs',
      author_email='ceolwulf@gmail.com',
      keywords=['pkm', 'pokemon'],
      url='http://bitbucket.org/ceol/pypkm',
      packages=['pypkm'],
      package_data={'pypkm': ['*.sqlite']},
     )