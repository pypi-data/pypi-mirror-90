"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-10-21

**Project** : monte_carlo_analysis

**Test class BRATSMetric**

"""
import numpy as np
from monte_carlo_analysis.metrics import BRATSMetric
from monte_carlo_analysis.strategies import ClassWiseStrategy
from monte_carlo_analysis.uncertainty_metrics import VarianceSingleDistribution


def test_brats_metric() -> None:
    """
    Test to string method of BRATSMetric metric with the following data

    **Ground truth**
    [0, 1, 0, 1]
    [0, 1, 0, 1]
    [0, 1, 0, 1]

    **Class prediction**
    [1, 1, 0, 1]
    [1, 1, 0, 1]
    [1, 1, 0, 1]

    **Uncertainty map**
    [0.21, 0.21, 0, 0]
    [0.1204, 0.1204, 0, 0]
    [0.0564, 0.0564, 0, 0]
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
            25 * [np.array([[[1, 1, 0, 1],
                [1, 1, 0, 1],
                [1, 1, 0, 1]],

                [[0, 0, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0]]
                ])] +\
                        15 * [np.array([[[0, 0, 0, 1],
                            [1, 1, 0, 1],
                            [1, 1, 0, 1]],

                            [[1, 1, 1, 0],
                                [0, 0, 1, 0],
                                [0, 0, 1, 0]]
                            ])] +\
                        7 * [np.array([[[1, 1, 0, 1],
                            [0, 0, 0, 1],
                            [1, 1, 0, 1]],

                            [[0, 0, 1, 0],
                                [1, 1, 1, 0],
                                [0, 0, 1, 0]]
                            ])] +\
                        3 * [np.array([[[1, 1, 0, 1],
                            [1, 1, 0, 1],
                            [0, 0, 0, 1]],

                            [[0, 0, 1, 0],
                                [0, 0, 1, 0],
                                [1, 1, 1, 0]]
                            ])]
       )

    uncertainty_metric = ClassWiseStrategy(
        uncertainty_metric=VarianceSingleDistribution()
    )(prediction)
    expected_values = [0.86026936, 0.84513789]
    metric_values = BRATSMetric()(prediction, uncertainty_metric, ground_truth)

    assert len(expected_values) == len(metric_values)
    assert np.sum(
	(np.array(metric_values) - np.array(expected_values)) ** 2
	) < 0.0001

