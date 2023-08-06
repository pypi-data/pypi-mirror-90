"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-09-29

**Project** : monte_carlo_analysis

**Implement abstract class UncertaintyMetric**

"""

class UncertaintyMetric(object):
    """
    abstract class that implement the Uncertainty Metric

    :param name: name of the uncertainty metric
    """
    def __init__(self) -> None:
        super(UncertaintyMetric, self)

    def __call__(self, *arg, **kwarg):
        """
        compute the uncertainty metrics
        """
        pass

    def __str__(self) -> str:
        """
        to string method
        """
        return self.__class__.__name__

