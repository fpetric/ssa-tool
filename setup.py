from setuptools import setup, find_packages

with open('README.org') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='ssa',
    version='0.1.0',
    description='A utility for the creation and evaluation of self-stabilizing algorithms',
    long_description=readme,
    author='Sean Allred',
    author_email='code@seanallred.com',
    url='https://github.com/vermiculus/ssa-tool',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
