"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-10-16

**Project** : monte_carlo_analysis

**Test TopDistributionSimilarityStrategy**

"""
import numpy as np
from itertools import product
from monte_carlo_analysis.uncertainty_metrics import BhattacharyaCoefficentDistributionSimilarity
from monte_carlo_analysis.strategies import TopDistributionsSimilarityStrategy


def test_top_distributions_similarity_strategy_call() -> None:
    """
    Test the call method of TopDistributionSimilarityStrategy class
    """
    uncertainty_metric = BhattacharyaCoefficentDistributionSimilarity(nbins=10)
    strategy = TopDistributionsSimilarityStrategy(
        uncertainty_metric=uncertainty_metric
    )

    def generate_array(
        number_of_predictions: int, number_of_features: int,
        shape: list
    ) -> np.array:
        if len(shape) == 0:
            # If dimension is null generate the prediction output
            return np.array(
                [
                    np.ones(number_of_features)/(np.arange(number_of_features).sum())
                    for i in range(number_of_predictions)
                    ]
                )
        # Recursive call over the dimension
        return np.moveaxis(
            np.array(
                [
                    generate_array(
                        number_of_predictions, number_of_features,
                        shape[:-1]
                        )
                    for i in range(shape[-1])
                    ]
                ), 0, -1
            )

    # Generate array of different shapes (corresponding to 1D, 2D and 3D examples) 
    # with identique distribution for every prediction
    arrays = [
            generate_array(
                number_of_predictions=2, number_of_features=3, shape=[120]
                ),
            generate_array(
                number_of_predictions=2, number_of_features=3, shape=[4, 30]
                ),
            generate_array(
                number_of_predictions=2, number_of_features=3, shape=[4, 5, 6]
                ),
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

