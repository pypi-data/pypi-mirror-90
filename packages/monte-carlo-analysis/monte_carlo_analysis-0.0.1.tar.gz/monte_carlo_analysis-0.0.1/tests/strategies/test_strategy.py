"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-09-29

**Project** : monte_carlo_analysis

**Test abstract class Strategy**

"""
from monte_carlo_analysis.strategies import Strategy
from monte_carlo_analysis.uncertainty_metrics import UncertaintyMetric


def test_strategy_str() -> None:
    """
    Test to string method of Strategy class
    """
    strategy = Strategy(UncertaintyMetric())
    assert str(strategy) == "Strategy"
