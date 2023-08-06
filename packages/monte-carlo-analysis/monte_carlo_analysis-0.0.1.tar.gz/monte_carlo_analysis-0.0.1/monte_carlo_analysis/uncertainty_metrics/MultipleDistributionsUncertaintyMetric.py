"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-10-14

**Project** : monte_carlo_analysis

**Implement abstract class MultipleDistributionsUncertaintyMetric**

"""
from monte_carlo_analysis.uncertainty_metrics import UncertaintyMetric


class MultipleDistributionsUncertaintyMetric(UncertaintyMetric):
    def __init__(self):
        super(MultipleDistributionsUncertaintyMetric, self)
        self.transformation = np.vectorize(self.get_transformation())

    def get_transformation(self) -> callable:
        """
        Define the transformation applied to the distribution

        :return: Transformation to apply to the distribution
        """
        def transformation(distributions: np.array) -> float:
            pass
        return transformation

