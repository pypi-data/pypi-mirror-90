"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-10-29

**Project** : monte_carlo_analysis

**Test ClassWiseDistributionStrategy**

"""
import numpy as np
from itertools import product
from monte_carlo_analysis.uncertainty_metrics import BhattacharyaCoefficentDistributionSimilarity
from monte_carlo_analysis.strategies import ClassWiseDistributionStrategy


def test_class_wise_distributions_similarity_strategy_call() -> None:
    """
    Test the call method of ClassWiseDistributionStrategy class
    """
    uncertainty_metric = BhattacharyaCoefficentDistributionSimilarity(nbins=10)
    strategy = ClassWiseDistributionStrategy(
        uncertainty_metric=uncertainty_metric
    )

    arrays = [
        np.ones((2, 3, 120)) / 3,
        np.ones((2, 3, 4, 30)) / 3,
        np.ones((2, 3, 4, 5, 6)) / 3,
    ]

    expected_uncertainty_maps = [
        np.ones((2, 3, 120)),
        np.ones((2, 3, 4, 30)),
        np.ones((2, 3, 4, 5, 6)),
    ]
    for array, expected_uncertainty_maps in zip(
        arrays, expected_uncertainty_maps
    ):
        assert (
            strategy(array) - expected_uncertainty_maps
        ).sum() ** 2 < 0.00001

