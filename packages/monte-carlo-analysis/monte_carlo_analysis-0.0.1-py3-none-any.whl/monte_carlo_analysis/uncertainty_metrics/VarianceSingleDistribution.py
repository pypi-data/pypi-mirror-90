"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-09-30

**Project** : monte_carlo_analysis

**Implement class VarianceSingleDistribution**

"""
from monte_carlo_analysis.uncertainty_metrics import SingleDistributionUncertaintyMetric
import numpy as np
from numba import jit


class VarianceSingleDistribution(SingleDistributionUncertaintyMetric):
    def __init__(self):
        super(VarianceSingleDistribution, self)
        self.transformation = self.get_transformation()

    def get_transformation(self) -> callable:
        """
        Define the variance transformation applied to the distribution

        :return: Transformation to apply varianceto the distribution
        """
        @jit(nopython=True)
        def transformation(distribution: np.array) -> float:
            return np.std(distribution) ** 2
        return transformation

