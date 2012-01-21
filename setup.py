from setuptools import setup, find_packages

PACKAGE = 'pypkm'
NAME = 'PyPKM'
DESCRIPTION = 'Easy PKM File Manipulation'
AUTHOR = 'Patrick Jacobs'
AUTHOR_EMAIL = 'ceolwulf@gmail.com'
URL = 'https://github.com/ceol/pypkm'
VERSION = __import__(PACKAGE).__version__


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="BSD",
    url=URL,
    packages=find_packages(),
    package_data={'': ['data']},
    install_requires=['construct==2.06'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Simplified BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
)