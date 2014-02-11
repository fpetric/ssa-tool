
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'A utility for the creation and evaluation of self-stabilizing algorithms',
    'author': 'Sean Allred',
    'url': 'http://github.com/vermiculus/smp',
    'download_url': 'http://github.com/vermiculus/smp',
    'author_email': 'seallred@smcm.edu',
    'version': '0.1',
    'install_requires': ['networkx', 'pygame'],
    'packages': ['ssa'],
    'scripts': [],
    'name': 'ssa',
    'py_modules': ['core', 'creation', 'simulation']
}

setup(**config)
