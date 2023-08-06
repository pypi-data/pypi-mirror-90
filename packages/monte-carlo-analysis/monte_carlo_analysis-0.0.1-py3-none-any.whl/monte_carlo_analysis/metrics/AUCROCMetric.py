
"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-10-21

**Project** : monte_carlo_analysis

**Implement class AUCROCMetric**

"""
from monte_carlo_analysis.metrics import Metric
import numpy as np
from sklearn.metrics import roc_auc_score
from numba import jit


class AUCROCMetric(Metric):
    """
    Implement AUCROCMetric
    """
    def __init__(self):
        super(AUCROCMetric, self)

    def __call__(
            self, prediction: np.array,
            uncertainty_map: np.array,
            ground_truth: np.array
            ):
        """
        Compute the auc-roc metric
        """
        # Get the class prediction
        class_prediction = np.argmax(prediction.mean(axis=0), axis=0)
        class_ground_truth = np.argmax(ground_truth, axis=0)

        # Compute misclassification map
        misclassification_map = (class_ground_truth != class_prediction)

        return roc_auc_score(
                misclassification_map.ravel(), uncertainty_map.ravel()
                )
