"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-09-30

**Project** : monte_carlo_analysis

**Test class VarianceSingleDistribution**

"""
from monte_carlo_analysis.uncertainty_metrics import VarianceSingleDistribution
import numpy as np


def test_variance_single_distribution_transformation() -> None:
    """
    Test the behaviour of the variance single distribution
    """
    table = np.array([0, 1])
    variance_single_distribution = VarianceSingleDistribution()
    assert (variance_single_distribution.transformation(table) - 0.25) ** 2 < 0.0001
