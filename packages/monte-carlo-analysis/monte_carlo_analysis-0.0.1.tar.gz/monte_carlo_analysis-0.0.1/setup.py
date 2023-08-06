"""
**Author** : Robin Camarasa

**Institution** : monte_carlo_analysis

**Position** : Erasmus MC

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-08-07

**Project** : monte_carlo_analysis

** monte_carlo_analysis setup file**

"""
import os
import sys
from subprocess import check_output
from pathlib import Path

from setuptools import find_packages, setup


# Main path
SRC_ROOT = Path(
    __file__
).absolute().parent

# Get long description
try:
    readme_path = SRC_ROOT / 'README.md'
    with readme_path.open('r') as readme_handler:
        long_description = readme_handler.read()
except:
    long_description = 'Error'


# Get version
try:
    command = 'git tag'.format(
        SRC_ROOT.resolve()
    )
    print(command)
    with os.popen(cmd=command) as stream:
          version = stream.readlines()[-1][:-1]
except:
    version='Error'

# Get requirements
try:
    requirements_path = SRC_ROOT / 'requirements.txt'
    with requirements_path.open('r') as requirements_handler:
        requirements = [
            dependency
            for dependency in requirements_handler.readlines()
            if not 'monte_carlo_analysis' in dependency
        ]
except:
    requirements=[]


setup(
    name='monte_carlo_analysis',
    author='Robin Camarasa',
    version=version,
    packages=find_packages(),
    description='Package that analyses the output of a monte-carlo dropout network',
    long_description_content_type="text/markdown",
    long_description=long_description,
    install_requires=requirements,
    author_email='r.camarasa@erasmusmc.nl',
)

