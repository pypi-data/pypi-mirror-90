"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-09-29

**Project** : monte_carlo_analysis

**Test abstract class UncertaintyMetric**

"""
from monte_carlo_analysis.uncertainty_metrics import UncertaintyMetric


def test_uncertainty_metric_str() -> None:
    """
    Test to string method of UncertaintyMetric class
    """
    uncertainty_metric = UncertaintyMetric()
    assert str(uncertainty_metric) == "UncertaintyMetric"
