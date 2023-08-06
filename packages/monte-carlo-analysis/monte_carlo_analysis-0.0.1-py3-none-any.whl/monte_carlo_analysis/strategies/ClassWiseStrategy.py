"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-10-29

**Project** : monte_carlo_analysis

**Implement ClassWiseStrategy class**

"""
import numpy as np
from itertools import product
from monte_carlo_analysis.strategies import Strategy
from numba import jit


class ClassWiseStrategy(Strategy):
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
                    ensemble_output[(slice(None), j,) + i]
                )
        return uncertainty_map

