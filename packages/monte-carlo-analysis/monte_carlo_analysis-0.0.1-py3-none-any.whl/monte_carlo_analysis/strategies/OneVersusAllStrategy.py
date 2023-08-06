
"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-10-29

**Project** : monte_carlo_analysis

**Implement OneVersusAllStrategy class**

"""
import numpy as np
from itertools import product
from monte_carlo_analysis.strategies import Strategy
from numba import jit


class OneVersusAllStrategy(Strategy):
    @staticmethod
    @jit
    def transformation(
            uncertainty_metric_transformation: callable,
            ensemble_output: np.array, counter: list
            ) -> np.array:

        # Get the dim size of the output uncertainty map
        uncertainty_map_shape = ensemble_output.shape[1:]

        # Initialize uncertainty metric
        uncertainty_map = np.zeros(uncertainty_map_shape)

        # Loop over the indexes of the output uncertainty metric
        for i in counter:
            for j in range(ensemble_output.shape[1]):
                uncertainty_map[(j,) + i] += uncertainty_metric_transformation(
                    np.concatenate(
                        (
                            ensemble_output[(slice(None), [j],) + i],
                            1 - ensemble_output[(slice(None), [j],) + i],
                            ), axis=1
                        )
                )
        return uncertainty_map

