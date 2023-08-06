"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-09-30

**Project** : monte_carlo_analysis

**Implement class SingleDistributionUncertaintyMetric**

"""
from monte_carlo_analysis.uncertainty_metrics import UncertaintyMetric
import numpy as np


class SingleDistributionUncertaintyMetric(UncertaintyMetric):
    def __init__(self):
        super(SingleDistributionUncertaintyMetric, self)
        self.transformation = np.vectorize(self.get_transformation())

    def get_transformation(self) -> callable:
        """
        Define the transformation applied to the distribution

        :return: Transformation to apply to the distribution
        """
        def transformation(distribution: np.array) -> float:
            pass
        return transformation

