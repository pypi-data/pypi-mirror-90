"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-10-21

**Project** : monte_carlo_analysis

**Test class AUCPRMetric**

"""
import numpy as np
from monte_carlo_analysis.metrics import AUCPRMetric
from monte_carlo_analysis.strategies import AverageSingleDistributionStrategy
from monte_carlo_analysis.uncertainty_metrics import VarianceSingleDistribution


def test_auc_pr_metric() -> None:
    """
    Test to string method of AUCPRMetric metric with the following data

    **Misclassification map**
    [1, 0, 0, 0]
    [1, 0, 0, 0]
    [1, 0, 0, 0]

    **Uncertainty map**
    [O.16, O.16, O.16, 0]
    [0, 0, 0, 0]
    [0, 0, 0, 0]
    """
    ground_truth = np.array(
            [[[0, 1, 0, 1],
                [0, 1, 0, 1],
                [0, 1, 0, 1]],

                [[1, 0, 1, 0],
                    [1, 0, 1, 0],
                    [1, 0, 1, 0]]
                ]
       )

    prediction = np.array(
            40 * [np.array([[[1, 1, 0, 1],
                [1, 1, 0, 1],
                [1, 1, 0, 1]],

                [[0, 0, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0]]
                ])] +\
                        10 * [np.array([[[0, 0, 1, 1],
                            [1, 1, 0, 1],
                            [1, 1, 0, 1]],

                            [[1, 1, 0, 0],
                                [0, 0, 1, 0],
                                [0, 0, 1, 0]]
                            ])]

       )

    uncertainty_metric = AverageSingleDistributionStrategy(
        uncertainty_metric=VarianceSingleDistribution()
    )(prediction)
    expected_value = 0.2777777777777778

    assert (
            AUCPRMetric()(prediction, uncertainty_metric, ground_truth) - expected_value
            ) ** 2 < 0.0001

