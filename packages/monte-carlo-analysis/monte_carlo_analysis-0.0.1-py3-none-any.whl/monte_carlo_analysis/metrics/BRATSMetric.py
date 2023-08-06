"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-10-27

**Project** : monte_carlo_analysis

**Implement class BRATSMetric**

"""
from monte_carlo_analysis.metrics import Metric
import numpy as np
from sklearn.metrics import auc, confusion_matrix
from numba import jit


class BRATSMetric(Metric):
    """
    Implement BRATSMetric, This metric only work in binary context
    """
    def __init__(self, threshold=100, epsilon=10**(-9)):
        super(BRATSMetric, self)
        self.threshold = threshold
        self.epsilon = epsilon
        self.integration_range = np.linspace(0, 1, self.threshold)

    def __call__(
            self, prediction: np.array,
            uncertainty_map: np.array,
            ground_truth: np.array,
            ):
        """
        Compute the BRATS Metric
        """
        classwise_prediction = np.argmax(
                prediction.mean(axis=0), axis=0
                )


        # Uncertainty map
        uncertainty_map /= np.max(uncertainty_map)

        results = []

        # Loop over the class
        for class_ in range(prediction.shape[1]):

            # Get the class prediction
            class_prediction = classwise_prediction == class_
            class_ground_truth = ground_truth[class_]
            class_uncertainty_map = uncertainty_map[class_]

            # Compute tp, fn, fp and tn maps
            tp = class_prediction * class_ground_truth
            fp = class_prediction * (1 - class_ground_truth)
            fn =(1 - class_prediction) * class_ground_truth
            tn =(1 - class_prediction) * (1 - class_ground_truth)


            # Compute value for threshold = 1.00
            tp_1 = tp.sum()
            tn_1 = tn.sum()

            tpr = []
            tnr = []
            dice = []

            # Compute the values of threshold
            for threshold in self.integration_range.tolist():
                filtered_voxels = np.where(class_uncertainty_map < 1 - threshold)
                tp_, fn_, fp_, tn_ = tp[filtered_voxels].sum(), fn[filtered_voxels].sum(),\
                        fp[filtered_voxels].sum(), tn[filtered_voxels].sum()

                if tp_1 == 0:
                    tpr.append(1)
                else:
                    tpr.append((tp_1 - tp_)/(tp_1 + self.epsilon))
                if tn_1 == 0:
                    tnr.append(1)
                else:
                    tnr.append((tn_1 - tn_)/(tn_1 + self.epsilon))
                dice.append((2 * tp_) / (2 * tp_ + fp_ + fn_ + self.epsilon))

            # Transform to array and remove nan values
            tpr = np.array(tpr)
            tpr[-1] = 1
            tnr = np.array(tnr)
            tnr[-1] = 1
            dice = np.array(dice)
            dice[-1] = 1

            results.append(
                    (
                        2 - auc(self.integration_range, tpr) -\
                                auc(self.integration_range, tnr) +\
                        auc(self.integration_range, dice)
                    )/3
                )
        return results

