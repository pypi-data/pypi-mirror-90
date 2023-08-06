"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-12-09

**Project** : monte_carlo_analysis

**Implement class AUCPRClassWiseMetric**

"""
from monte_carlo_analysis.metrics import Metric
import numpy as np
from sklearn.metrics import average_precision_score
from numba import jit


class AUCPRClassWiseMetric(Metric):
    """
    Implement AUCPRClassWiseMetric
    """
    def __init__(self):
        super(AUCPRClassWiseMetric, self)

    def __call__(
            self, prediction: np.array,
            uncertainty_map: np.array,
            ground_truth: np.array
            ):
        """
        Compute the auc-pr metric
        """
        # Get the number of classes
        nb_classes = prediction.shape[1]

        # Get the class prediction
        class_prediction = np.argmax(prediction.mean(axis=0), axis=0)
        class_ground_truth = np.argmax(ground_truth, axis=0)

        # Compute misclassification map
        results = []
        for i in range(nb_classes):
            class_ground_truth_ = (class_ground_truth == i)
            class_prediction_ = (class_prediction == i)
            misclassification_map = (class_ground_truth_ != class_prediction_)
            results.append(
                    average_precision_score(
                        misclassification_map.ravel(), uncertainty_map[i].ravel()
                        )
                    )
        return results
