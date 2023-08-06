"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-11-27

**Project** : monte_carlo_analysis

**Test MelbaDiceAnalysis**

"""
from monte_carlo_analysis.settings import TESTS_OUTPUT
from monte_carlo_analysis.analysis import MelbaDiceAnalysis
import matplotlib
import pandas as pd
import numpy as np
import shutil


def test_plot() -> None:
    """Test plot method of MelbaDiceAnalysis
    """
    df = pd.DataFrame(
            {
                'Background': np.random.rand(144),
                'Vessel Wall': np.random.rand(144),
                'Lumen': np.random.rand(144)
                }
            )

    # Initialise the analysis class
    melba_dice_analysis = MelbaDiceAnalysis(
            df=df
            )

    plot = melba_dice_analysis.plot(output_class='Lumen')

    # Clean output folder
    if TESTS_OUTPUT.exists():
        shutil.rmtree(
                TESTS_OUTPUT.resolve()
                )
    TESTS_OUTPUT.mkdir(parents=True, exist_ok=True)

    # Save figure
    plot.savefig(TESTS_OUTPUT / 'test_classwise_plot.png')

    assert type(plot) == matplotlib.figure.Figure


