"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-11-20

**Project** : monte_carlo_analysis

**Test MelbaAnalysis**

"""
import pandas as pd
import matplotlib
import numpy as np
import shutil
from monte_carlo_analysis.analysis import MelbaAnalysis
from monte_carlo_analysis.settings import TESTS_OUTPUT

DATAFRAME= pd.DataFrame(
        {
            'u_m_a': np.arange(1, 10)/20,
            'u_m_b': np.arange(1, 10)**2/150,
            'u_m_c': np.zeros((9,)),
            }
        )

def test_get_statistical_test_a_b():
    """
    Test get_statistical_test_a_b
    """
    melba_analysis = MelbaAnalysis(df=DATAFRAME, metric='Test')
    statistics_a_b = melba_analysis.get_statistical_test_a_b(
            'u_m_a', 'u_m_b'
            )
    assert set(statistics_a_b.keys()) == {
            'k_a_b', 'I_min', 'I_max', 'N',
            'distribution'
            }
    assert statistics_a_b['N'] == 9
    assert statistics_a_b['k_a_b'] == 7
    assert (statistics_a_b['I_min'] -  0.4439045376923585) ** 2 < 0.0001
    assert (statistics_a_b['I_max'] -  0.9332604888222655) ** 2 < 0.0001


def test_get_statistical_tests():
    """Test get_statistical_tests
    """
    melba_analysis = MelbaAnalysis(df=DATAFRAME, metric='Test')
    statistics = melba_analysis.get_statistical_tests()
    assert set(statistics.keys()) == {'u_m_a', 'u_m_b', 'u_m_c'}
    assert statistics['u_m_a']['u_m_a'] is None
    assert statistics['u_m_b']['u_m_a'].keys() == {
            'k_a_b', 'I_min', 'I_max', 'N',
            'distribution'
            }

def test_plot_statistical_test_a_b():
    """Test plot_statistical_test_a_b
    """
    melba_analysis = MelbaAnalysis(df=DATAFRAME, metric='Test')
    plot = melba_analysis.plot_statistical_test_a_b(
            'u_m_a', 'u_m_b'
            )

    # Clean output folder
    if TESTS_OUTPUT.exists():
        shutil.rmtree(
                TESTS_OUTPUT.resolve()
                )
    TESTS_OUTPUT.mkdir(parents=True, exist_ok=True)

    # Save figure
    plot.savefig(TESTS_OUTPUT / 'test_plot_statistical_test_a_b.png')

    assert type(plot) == matplotlib.figure.Figure

    melba_analysis = MelbaAnalysis(df=DATAFRAME, metric='Test')
    plot = melba_analysis.plot_statistical_test_a_b(
            'u_m_b', 'u_m_a'
            )

    # Save figure
    plot.savefig(TESTS_OUTPUT / 'test_plot_statistical_test_b_a.png')

    assert type(plot) == matplotlib.figure.Figure

    melba_analysis = MelbaAnalysis(df=DATAFRAME, metric='Test')
    plot = melba_analysis.plot_statistical_test_a_b(
            'u_m_a', 'u_m_a'
            )

    # Save figure
    plot.savefig(TESTS_OUTPUT / 'test_plot_statistical_test_a_a.png')

    assert type(plot) == matplotlib.figure.Figure

def test_plot_statistical_tests():
    """Test plot_statistical_tests
    """
    melba_analysis = MelbaAnalysis(df=DATAFRAME, metric='Test')
    plots = melba_analysis.plot_statistical_tests()

    assert set(plots.keys()) == {'u_m_a', 'u_m_b', 'u_m_c'}
    assert type(plots['u_m_b']['u_m_a']) == matplotlib.figure.Figure
    assert type(plots['u_m_b']['u_m_b']) == matplotlib.figure.Figure


def test_generate_credible_interval_latex_table():
    """Test generate_credible_interval_latex_table
    """
    melba_analysis = MelbaAnalysis(df=DATAFRAME, metric='Test')
    latex_code = melba_analysis.generate_credible_interval_latex_table()
    assert type(latex_code) == str

