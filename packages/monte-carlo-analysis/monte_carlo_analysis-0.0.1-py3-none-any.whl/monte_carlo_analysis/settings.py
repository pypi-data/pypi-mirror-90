"""
**Author** : Robin Camarasa

**Institution** : Erasmus MC

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-08-07

**Project** : monte_carlo_analysis

** Settings of the monte_carlo_analysis project**

"""
from pathlib import Path


# Define root path
ROOT_PATH = Path(
    __file__
).absolute().parents[2]

# Define src path
SRC_ROOT = Path(
    __file__
).absolute().parents[1]


# Define data path
DATA_PATH = ROOT_PATH / 'data'

# Results paths
RESULTS_PATH = ROOT_PATH / 'results'

# Ressources paths
RESSOURCES_PATH = SRC_ROOT / 'ressources'

# Ressources paths
TESTS_PATH = SRC_ROOT / 'tests'

# Ressources paths
TESTS_OUTPUT = SRC_ROOT / 'tests_output'
