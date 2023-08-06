"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-10-13

**Project** : monte_carlo_analysis

**Implement class EarthMoverDistanceDistributionSimilarity**

"""
from monte_carlo_analysis.utils.numba_utils import numba_cumul_histogram
from monte_carlo_analysis.uncertainty_metrics import DistributionSimilarityUncertaintyMetric
import numpy as np
from numba import jit


class EarthMoverDistanceDistributionSimilarity(DistributionSimilarityUncertaintyMetric):
    """
    Implement EarthMoverDistanceDistributionSimilarity

    :param nbins: Number of bins of the histogram
    """
    def __init__(self, nbins=100):
        super(EarthMoverDistanceDistributionSimilarity, self)
        self.nbins = nbins
        self.transformation = self.get_transformation(nbins)

    def get_transformation(self, nbins: int) -> callable:
        """
        Define the transformation applied to the distribution

        :param nbins: number of bins in the histogram
        :return: transformation to apply to the distribution
        """
        @jit(nopython=True)
        def transformation(distribution_1: np.array, distribution_2) -> float:
            # In 1D the EarthMoverdistance is proportional to the L1 distance
            # between 2 histogram
            cum_discretized_distribution_1 = numba_cumul_histogram(
                distribution_1, bins=nbins, min_value=0, max_value=1,
                normalized=True
            )[0]

            cum_discretized_distribution_2 = numba_cumul_histogram(
                distribution_2, bins=nbins, min_value=0, max_value=1,
                normalized=True
            )[0]

            return np.sum(np.abs(
                cum_discretized_distribution_1 - cum_discretized_distribution_2
            )) / nbins
        return transformation
