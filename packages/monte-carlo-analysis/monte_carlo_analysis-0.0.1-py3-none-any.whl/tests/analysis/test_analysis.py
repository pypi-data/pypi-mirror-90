
"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-09-29

**Project** : monte_carlo_analysis

**Test abstract class Analysis**

"""
from monte_carlo_analysis.analysis import Analysis


def test_analysis_str() -> None:
    """
    Test to string method of Analysis class
    """
    analysis = Analysis()
    assert str(analysis) == "Analysis"
