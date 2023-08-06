"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-09-29

**Project** : monte_carlo_analysis

**Implement abstract class Strategy**

"""
from monte_carlo_analysis.uncertainty_metrics import UncertaintyMetric
import numpy as np
from itertools import product


class Strategy(object):
    """
    Abstract class that implement the uncertainty_metric

    :param name: Name of the strategy
    """
    def __init__(
            self, uncertainty_metric: UncertaintyMetric
        ) -> None:
        super(Strategy, self)
        self.uncertainty_metric = uncertainty_metric

    def __call__(self, *arg, **kwarg):
        """
        Compute the strategy
        """
        pass

    def __str__(self) -> str:
        """
        To string method
        """
        return self.__class__.__name__

    def __call__(self, ensemble_output: np.array) -> np.array:
        """
        Compute the strategy

        :param ensemble_output: Ensemble error
        """
        counter = list(product(
            *(range(dim) for dim in list(ensemble_output.shape[2:]))
        ))
        return self.transformation(
                uncertainty_metric_transformation=self.uncertainty_metric.transformation,
                ensemble_output=ensemble_output, counter=counter
                )

    @staticmethod
    def transformation(
        uncertainty_metric, ensemble_output, counter
        ):
        pass
