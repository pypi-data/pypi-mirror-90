"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-09-29

**Project** : monte_carlo_analysis

**Test abstract class Metric**

"""
from monte_carlo_analysis.metrics import Metric


def test_metric_str() -> None:
    """
    Test to string method of Metric class
    """
    metric = Metric()
    assert str(metric) == "Metric"
