"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-10-16

**Project** : monte_carlo_analysis

**Implement TopDistributionsSimilarityStrategy class**

"""
import numpy as np
from itertools import product
from monte_carlo_analysis.strategies import Strategy
from numba import jit


class TopDistributionsSimilarityStrategy(Strategy):
    @staticmethod
    #@jit
    def transformation(
            uncertainty_metric_transformation: callable,
            ensemble_output: np.array, counter: list
            ) -> np.array:
        """
        Compute the strategy

        :param ensemble_output: Ensemble error
        """
        # Get the dim size of the output uncertainty map
        uncertainty_map_shape = ensemble_output.shape[2:]

        # Initialize uncertainty metric
        uncertainty_map = np.zeros(uncertainty_map_shape)

        # Loop over the indexes of the output uncertainty metric
        for i in counter:
            j2, j1 = np.argsort(
                    np.mean(
                        ensemble_output[(slice(None), slice(None) , *i)],
                        axis=0
                        )
                    )[-2:].tolist()
            uncertainty_map[i] = uncertainty_metric_transformation(
                ensemble_output[(slice(None), j1, *i)],
                ensemble_output[(slice(None), j2, *i)]
                )
        return uncertainty_map

