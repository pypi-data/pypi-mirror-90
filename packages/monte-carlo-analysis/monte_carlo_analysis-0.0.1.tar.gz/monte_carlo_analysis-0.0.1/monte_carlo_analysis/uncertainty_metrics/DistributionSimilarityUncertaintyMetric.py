"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-10-01

**Project** : monte_carlo_analysis

**Implement abstract class DistributionSimilarityUncertaintyMetric**

"""
from monte_carlo_analysis.uncertainty_metrics import UncertaintyMetric


class DistributionSimilarityUncertaintyMetric(UncertaintyMetric):
    def __init__(self):
        super(DistributionSimilarityUncertaintyMetric, self)
        self.transformation = np.vectorize(self.get_transformation())

    def get_transformation(self) -> callable:
        """
        Define the transformation applied to the distribution

        :return: Transformation to apply to the distribution
        """
        def transformation(distribution_1: np.array, distribution_2) -> float:
            pass
        return transformation

