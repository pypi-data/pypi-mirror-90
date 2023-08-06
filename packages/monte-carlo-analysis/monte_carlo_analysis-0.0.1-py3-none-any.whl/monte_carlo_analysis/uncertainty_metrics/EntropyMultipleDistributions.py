"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-10-14

**Project** : monte_carlo_analysis

**Implement class EntropyMultipleDistributions**

"""
from monte_carlo_analysis.uncertainty_metrics import MultipleDistributionsUncertaintyMetric
import numpy as np
from numba import jit


class EntropyMultipleDistributions(MultipleDistributionsUncertaintyMetric):
    """
    Implement EntropyMultipleDistributions
    """
    def __init__(self):
        super(EntropyMultipleDistributions, self)
        self.transformation = self.get_transformation()

    def get_transformation(self) -> callable:
        """
        Define the variance transformation applied to the distribution

        :return: Transformation to apply varianceto the distribution
        """
        @jit
        def transformation(distributions: np.array) -> float:
            mean_prediction_per_class = np.mean(distributions, axis=0)

            # Generate the log_mean_prediction_per_class taking into account
            # the case of zero means
            log_mean_prediction_per_class = mean_prediction_per_class[:]
            log_mean_prediction_per_class[
                np.where(log_mean_prediction_per_class == 0)
            ] = 1
            log_mean_prediction_per_class = np.log(log_mean_prediction_per_class)

            return - np.sum(log_mean_prediction_per_class * mean_prediction_per_class)
        return transformation
