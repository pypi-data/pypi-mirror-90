"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-12-09

**Project** : monte_carlo_analysis

**Test class AUCPRClassWiseMetric**

"""
import numpy as np
from monte_carlo_analysis.metrics import AUCPRClassWiseMetric
from monte_carlo_analysis.strategies import ClassWiseStrategy
from monte_carlo_analysis.uncertainty_metrics import VarianceSingleDistribution


def test_auc_pr_class_wise_metric() -> None:
    """
    Test to string method of AUCPRClassWiseMetric metric with the following data

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

    uncertainty_metric = ClassWiseStrategy(
        uncertainty_metric=VarianceSingleDistribution()
    )(prediction)
    expected_values = [0.2777777777777778 ,  0.2777777777777778]

    output = AUCPRClassWiseMetric()(
            prediction, uncertainty_metric,
            ground_truth
            )
    assert len(output)==2
    assert (np.array(expected_values) - np.array(output)).sum() ** 2 < 0.000000001

