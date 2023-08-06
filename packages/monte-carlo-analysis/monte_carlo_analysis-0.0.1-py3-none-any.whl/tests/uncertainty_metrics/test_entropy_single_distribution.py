
"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-09-30

**Project** : monte_carlo_analysis

**Test class EntropySingleDistribution**

"""
from monte_carlo_analysis.uncertainty_metrics import EntropySingleDistribution
import numpy as np


def test_entropy_single_distribution_transformation() -> None:
    """
    Test the behaviour of the entropy single distribution
    for different histogram bin size.
    """
    # Define the distribution
    table = np.array([0.03, 0.23, 0.33, 0.33, 0.53])

    # Define the expected values for different nbins 
    nbins = [2, 5]
    values = [0.25020121176909393, 0.19005410784664695]
    for value_, nbins_ in zip(values, nbins):
        entropy_single_distribution = EntropySingleDistribution(
            nbins=nbins_
        )
        assert (
            entropy_single_distribution.transformation(table) - value_
        ) ** 2 < 0.0001
