
"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-10-29

**Project** : monte_carlo_analysis

**Test OneVersusAll strategy**

"""
import numpy as np
from monte_carlo_analysis.uncertainty_metrics import EntropyMultipleDistributions
from monte_carlo_analysis.strategies import OneVersusAllStrategy


def test_one_versus_all_strategy_call() -> None:
    """
    Test the call method of OneVersusAllStrategy class
    """
    uncertainty_metric = EntropyMultipleDistributions()
    strategy = OneVersusAllStrategy(
        uncertainty_metric=uncertainty_metric
    )
    arrays = [
        np.ones((2, 3, 120)) / 3,
        np.ones((2, 3, 4, 30)) / 3,
        np.ones((2, 3, 4, 5, 6)) / 3,
    ]
    expected_uncertainty_maps = [
        0.63651417 * np.ones((3, 120)),
        0.63651417 * np.ones((3, 4, 30)),
        0.63651417 * np.ones((3, 4, 5, 6))
    ]
    for array, expected_uncertainty_maps in zip(
        arrays, expected_uncertainty_maps
    ):
        assert (
            strategy(array) - expected_uncertainty_maps
        ).sum() ** 2 < 0.00001

