"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-10-14

**Project** : monte_carlo_analysis

**Test class EntropyMultipleDistributions**

"""
from monte_carlo_analysis.uncertainty_metrics import EntropyMultipleDistributions
import numpy as np


def test_entropy_multiple_distributions_transformation() -> None:
    """
    Test the behaviour of the entropy multiple distributions
    for different histogram bin size.
    """
    # Define the distributions
    mc_outputs = [
        np.transpose(np.array(
            [
                [0.2, 0.4, 0.1, 0.25],
                [0.7, 0.5, 0.9, 0.75],
                [0.1, 0.1, 0, 0],
                ]
            )),
        np.transpose(np.array(
            [
                [0.2, 0.4, 0.1, 1],
                [0.8, 0.6, 0.9, 0],
                [0, 0, 0, 0],
                ]
            ))
    ]

    values = [0.7327336307337404, 0.6818546087307834]
    for value_, mc_output_ in zip(values, mc_outputs):
        entropy_multiple_distributions = EntropyMultipleDistributions()
        assert (
            entropy_multiple_distributions.transformation(mc_output_) - value_
        ) ** 2 < 0.0001

