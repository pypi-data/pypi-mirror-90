"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-11-20

**Project** : monte_carlo_analysis

**Implement Analysis abstract class**

"""

class Analysis(object):
    """
    Abstract class that implement the analysis
    """
    def __init__(self) -> None:
        super(Analysis, self)

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

