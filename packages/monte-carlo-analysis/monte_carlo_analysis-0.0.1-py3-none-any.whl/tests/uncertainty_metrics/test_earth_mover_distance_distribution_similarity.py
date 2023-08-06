"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-10-13

**Project** : monte_carlo_analysis

**Test class EarthMoverDistanceDistributionSimilarity**

"""
from monte_carlo_analysis.uncertainty_metrics import EarthMoverDistanceDistributionSimilarity
import numpy as np


def test_earth_mover_distance_distribution_similarity_transformation() -> None:
    """
    Test the behaviour of the earth mover distance distribution similarity transformation
    for different histogram bin size.
    """
    # Define the distributions
    table_1 = np.array([0.03, 0.23, 0.33, 0.33, 0.53])
    table_2 = np.array([0.32, 0.42, 0.63, 0.82, 0.95])

    # Define the expected values for different nbins 
    values = [0.2, 0.36]
    nbins = [2, 5]
    for value_, nbins_ in zip(values, nbins):
        earth_mover_distance_distribution_similarity = EarthMoverDistanceDistributionSimilarity(
            nbins=nbins_
        )
        assert (
            (earth_mover_distance_distribution_similarity.transformation(
                table_1, table_2
            ) - value_) ** 2 < 0.0001
        )

