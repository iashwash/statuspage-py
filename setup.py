from statuspage import __version__
from setuptools import setup, find_packages

setup(
    name='statuspage',
    version=__version__,
    description='Python library for Statuspage.io APIs',
    author='Kunal Lillaney',
    author_email='lillaney@jhu.edu',
    url='https://github.io/kunallillaney/statuspage-py',
    license='Apache2.0',
    packages=find_packages(exclude=('tests')),
    setup_requires=[
    ],
    install_requires=[
      'requests'
    ],
)
