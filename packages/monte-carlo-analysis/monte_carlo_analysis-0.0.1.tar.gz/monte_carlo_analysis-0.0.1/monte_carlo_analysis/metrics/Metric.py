"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-09-29

**Project** : monte_carlo_analysis

**Implement abstract class Metric**

"""

class Metric(object):
    """
    Abstract class that implement the metric

    :param name: Name of the metric
    """
    def __init__(self) -> None:
        super(Metric, self)

    def __call__(self, *arg, **kwarg):
        """
        Compute the metrics
        """
        pass

    def __str__(self) -> str:
        """
        To string method
        """
        return self.__class__.__name__

