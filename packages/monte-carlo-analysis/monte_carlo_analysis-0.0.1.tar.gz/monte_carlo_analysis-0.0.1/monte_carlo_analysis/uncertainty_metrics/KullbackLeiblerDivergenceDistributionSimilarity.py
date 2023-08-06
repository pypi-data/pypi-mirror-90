"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-10-13

**Project** : monte_carlo_analysis

**Implement class KullbackLeiblerDivergenceDistributionSimilarity**

"""
from monte_carlo_analysis.uncertainty_metrics import DistributionSimilarityUncertaintyMetric
import numpy as np
from numba import jit
from scipy.stats import entropy


class KullbackLeiblerDivergenceDistributionSimilarity(
    DistributionSimilarityUncertaintyMetric
):
    """
    Implement KullbackLeiblerDivergenceDistributionSimilarity

    :param nbins: Number of bins of the histogram
    :param epsilon: Number to avoid the division by zero
    """
    def __init__(self, nbins=100, epsilon=0.0000001):
        super(KullbackLeiblerDivergenceDistributionSimilarity, self)
        self.nbins = nbins
        self.epsilon = epsilon
        self.transformation = self.get_transformation(self.nbins, self.epsilon)

    def get_transformation(self, nbins, epsilon) -> callable:
        """
        Define the transformation applied to the distribution

        :return: Transformation to apply to the distribution
        """
        @jit
        def transformation(distribution_1: np.array, distribution_2: np.array) -> float:
            # Discretize the distribution the division
            # by the sum is due to np.histogram implementation
            discretized_distribution_1 = np.histogram(
                distribution_1, bins=nbins, range=(0, 1),
                density=True
            )[0]
            discretized_distribution_1 /= discretized_distribution_1.sum()
            discretized_distribution_1[discretized_distribution_1 == 0]=epsilon

            discretized_distribution_2 = np.histogram(
                distribution_2, bins=nbins, range=(0, 1),
                density=True
            )[0]
            discretized_distribution_2 /= discretized_distribution_2.sum()
            discretized_distribution_2[discretized_distribution_2 == 0]=epsilon
            return - 1/2 * (
                    entropy(discretized_distribution_1, discretized_distribution_2) +\
                            entropy(discretized_distribution_2, discretized_distribution_1)
                    )
            # distribution_diff = discretized_distribution_1 - discretized_distribution_2

            # # Treat 0 error cases
            # distribution_diff[np.where(discretized_distribution_1 == 0)] = 0
            # distribution_diff[np.where(discretized_distribution_2 == 0)] = 0
            # discretized_distribution_1[np.where(discretized_distribution_1 == 0)] = 1
            # discretized_distribution_2[np.where(discretized_distribution_2 == 0)] = 1

            # return np.sum(
            #     distribution_diff * (np.log(discretized_distribution_1) -\
            #             distribution_diff * np.log(discretized_distribution_2))
            # ) / nbins
        return transformation

