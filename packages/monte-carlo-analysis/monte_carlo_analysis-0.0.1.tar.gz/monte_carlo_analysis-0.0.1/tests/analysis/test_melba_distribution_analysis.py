"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-11-26

**Project** : monte_carlo_analysis

**Test MelbaDistributionAnalysis class**

"""
import pandas as pd
import matplotlib
import numpy as np
import shutil
from monte_carlo_analysis.analysis import MelbaDistributionAnalysis
from monte_carlo_analysis.settings import TESTS_OUTPUT

UNCERTAINTY_MAPS = [
        'One vs all \n MI', 'One vs all \n Entropy',
        'Class-wise \n Variance', 'Class-wise \n Entropy'
        ]


CLASSES = [
        'Background', 'Vessel Wall', 'Lumen'
        ]

DATAFRAME = pd.DataFrame(
        {
            'metric 1': [np.random.rand() for i in range(100)],
            'metric 2': [np.random.rand() for i in range(100)],
            'metric 3': [np.random.rand() for i in range(100)],
            'uncertainty_map': [UNCERTAINTY_MAPS[i%4] for i in range(100)],
            'class': [CLASSES[i%3] for i in range(100)]
            }
        )


def test_plot():
    """
    Test plot method
    """
    # Test class-wise metric
    # Initialise analysis object
    melba_analysis = MelbaDistributionAnalysis(df=DATAFRAME)

    # Get figure
    plot = melba_analysis.plot('metric 1')

    # Clean output folder
    if TESTS_OUTPUT.exists():
        shutil.rmtree(
                TESTS_OUTPUT.resolve()
                )
    TESTS_OUTPUT.mkdir(parents=True, exist_ok=True)

    # Save figure
    plot.savefig(TESTS_OUTPUT / 'test_classwise_plot.png')

    assert type(plot) == matplotlib.figure.Figure

    # Test multi-class metric
    melba_analysis = MelbaDistributionAnalysis(
            df=DATAFRAME[
                ['metric 1', 'metric 2', 'metric 3', 'uncertainty_map']
                ]
            )

    # Get figure
    plot = melba_analysis.plot('metric 1')

    # Save figure
    plot.savefig(TESTS_OUTPUT / 'test_multiclass_plot.png')

    assert type(plot) == matplotlib.figure.Figure

