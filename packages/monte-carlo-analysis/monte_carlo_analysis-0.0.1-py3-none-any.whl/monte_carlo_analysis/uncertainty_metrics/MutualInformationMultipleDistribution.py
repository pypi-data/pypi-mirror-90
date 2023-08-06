"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-10-14

**Project** : monte_carlo_analysis

**Implement class MutualInformationMultipleDistributions**

"""
from monte_carlo_analysis.uncertainty_metrics import MultipleDistributionsUncertaintyMetric
import numpy as np
from numba import jit


class MutualInformationMultipleDistributions(MultipleDistributionsUncertaintyMetric):
    """
    Implement MutualInformationMultipleDistributions
    """
    def __init__(self):
        super(MutualInformationMultipleDistributions, self)
        self.transformation = self.get_transformation()

    def get_transformation(self) -> callable:
        """
        Define the variance transformation applied to the distribution

        :return: Transformation to apply variance to the distributions
        """
        @jit
        def transformation(distributions: np.array) -> float:
            # Compute entropy
            mean_prediction_per_class = np.mean(distributions, axis=0)

            # Generate the log_mean_prediction_per_class taking into account
            # the case of zero means
            log_mean_prediction_per_class = mean_prediction_per_class[:]
            log_mean_prediction_per_class[
                np.where(log_mean_prediction_per_class == 0)
            ] = 1
            log_mean_prediction_per_class = np.log(log_mean_prediction_per_class)
            entropy = - np.sum(
                log_mean_prediction_per_class * mean_prediction_per_class
            )

            # Compute conditional entropy

            # Generate the log prediction taking into account
            # the case of zero means
            log_prediction = distributions[:]
            log_prediction[
                np.where(distributions == 0)
            ] = 1
            log_prediction = np.log(log_prediction)
            conditional_entropy = -1.0/distributions.shape[0] * np.sum(
                log_prediction * distributions
            )

            return entropy - conditional_entropy
        return transformation
