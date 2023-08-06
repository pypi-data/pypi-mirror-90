"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-10-01

**Project** : monte_carlo_analysis

**Implement class BhattacharyaCoefficentDistributionSimilarity**

"""
from monte_carlo_analysis.uncertainty_metrics import DistributionSimilarityUncertaintyMetric
import numpy as np
from monte_carlo_analysis.utils.numba_utils import numba_histogram
from numba import jit


class BhattacharyaCoefficentDistributionSimilarity(DistributionSimilarityUncertaintyMetric):
    """
    Implement BhattacharyaCoefficentDistributionSimilarity

    :param nbins: Number of bins of the histogram
    """
    def __init__(self, nbins=100):
        super(BhattacharyaCoefficentDistributionSimilarity, self)
        self.nbins = nbins
        self.transformation = self.get_transformation(nbins)

    def get_transformation(self, nbins: int) -> callable:
        """
        Define the transformation applied to the distribution

        :param nbins: number of bins in the histogram
        :return: transformation to apply to the distribution
        """
        #@jit(nopython=True)
        def transformation(distribution_1: np.array, distribution_2) -> float:
            # discretize the distribution the division
            # by the sum is due to np.histogram implementation
            discretized_distribution_1 = numba_histogram(
                distribution_1, bins=nbins, min_value=0, max_value=1,
                normalized=True
            )[0]

            discretized_distribution_2 = numba_histogram(
                distribution_2, bins=nbins, min_value=0, max_value=1,
                normalized=True
            )[0]

            return np.sum(
                np.sqrt(discretized_distribution_1 * discretized_distribution_2)
            )
        return transformation
