"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-09-30

**Project** : monte_carlo_analysis

**Implement class EntropySingleDistribution**

"""
from monte_carlo_analysis.uncertainty_metrics import SingleDistributionUncertaintyMetric
import numpy as np
from numba import jit


class EntropySingleDistribution(SingleDistributionUncertaintyMetric):
    """
    Implement EntropySingleDistribution

    :param nbins: Number of bins of the histogram
    """
    def __init__(self, nbins=100):
        super(EntropySingleDistribution, self)
        self.nbins = nbins
        self.transformation = self.get_transformation(self.nbins)

    def get_transformation(self, nbins) -> callable:
        """
        Define the variance transformation applied to the distribution

        :return: Transformation to apply varianceto the distribution
        """
        @jit
        def transformation(distribution: np.array) -> float:
            # Discretize the distribution the division
            # by the sum is due to np.histogram implementation
            discretized_distribution = np.histogram(
                distribution, bins=nbins, range=(0, 1),
                density=True
            )[0]
            discretized_distribution /= discretized_distribution.sum()

            # Remove the 0 of the log
            log_discretized = discretized_distribution[:]
            log_discretized[np.where(log_discretized == 0)] = 1
            log_discretized = np.log(log_discretized)

            return - np.sum(discretized_distribution * log_discretized) / nbins
        return transformation
