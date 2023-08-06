"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-10-13

**Project** : monte_carlo_analysis

**Test class KullbackLeiblerDivergenceDistributionSimilarity**

"""
from monte_carlo_analysis.uncertainty_metrics import KullbackLeiblerDivergenceDistributionSimilarity
import numpy as np


def test_kullback_leibler_divergence_distribution_similarity_transformation() -> None:
    """
    Test the behaviour of the kullback leibler divergence similarity transformation
    for different histogram bin size.
    """
    # Define the distributions
    table_1 = np.array([0.03, 0.23, 0.33, 0.33, 0.53])
    table_2 = np.array([0.32, 0.42, 0.63, 0.82, 0.95])

    # Define the expected values for different nbins 
    values = [-0.35835189384561095, -6.161811984073319]
    nbins = [2, 5]
    for value_, nbins_ in zip(values, nbins):
        kullback_leibler_divergence_distribution_similarity = KullbackLeiblerDivergenceDistributionSimilarity(
            nbins=nbins_
        )
        assert (
            (kullback_leibler_divergence_distribution_similarity.transformation(
                table_1, table_2
            ) - value_) ** 2 < 0.0001
        )
