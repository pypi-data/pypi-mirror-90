"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-10-29

**Project** : monte_carlo_analysis

**Test ClassWise strategy**

"""
import numpy as np
from monte_carlo_analysis.uncertainty_metrics import VarianceSingleDistribution
from monte_carlo_analysis.strategies import ClassWiseStrategy


def test_class_wise_strategy_strategy_call() -> None:
    """
    Test the call method of ClassWiseStrategy class
    """
    uncertainty_metric = VarianceSingleDistribution()
    strategy = ClassWiseStrategy(
        uncertainty_metric=uncertainty_metric
    )
    arrays = [
        np.arange(2*3*4*5*6).reshape(2, 3, 120),
        np.arange(2*3*4*5*6).reshape(2, 3, 4, 30),
        np.arange(2*3*4*5*6).reshape(2, 3, 4, 5, 6),
    ]
    expected_uncertainty_maps = [
        32400. * np.ones((3, 120)),
        32400. * np.ones((3, 4, 30)),
        32400. * np.ones((3, 4, 5, 6)),
    ]
    for array, expected_uncertainty_maps in zip(
        arrays, expected_uncertainty_maps
    ):
        assert (
            strategy(array) - expected_uncertainty_maps
        ).sum() ** 2 < 0.00001

