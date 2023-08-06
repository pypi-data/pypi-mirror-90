"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-11-20

**Project** : monte_carlo_analysis

****

"""
from monte_carlo_analysis.analysis import Analysis
import re
import matplotlib
matplotlib.use('ps')
from matplotlib import rc
rc('text',usetex=True)
rc('text.latex',preamble='\\usepackage{color}')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
import glob
from pathlib import Path
from scipy.stats import gamma, beta
from scipy.stats import spearmanr
import scipy.stats as st


class MelbaAnalysis(Analysis):
    """Implement MelbaAnalysis

    :param df: Dataframe containing the following columns ['uncertainty_map_a', 'uncertainty_map_b' ...]
    :param metric: Metric to analyse
    """
    def __init__(
            self, df: pd.DataFrame, metric: str
        ):
        self.df = df
        self.metric = metric

    def get_statistical_test_a_b(
            self, uncertainty_map_a: str,
            uncertainty_map_b: str
            ) -> dict:
        """Get the statistical test of the uncertainty map a and b

        :param uncertainty_map_a: Name ot the uncertainty map a
        :param uncertainty_map_b: Name ot the uncertainty map b

        :return: The statistical test data of the uncertainty map a and b
        """
        # Get the number of samples where uncertainty metric a has a higher values
        # than uncertainty metric b
        k_a_b = (
                (self.df[uncertainty_map_a] - self.df[uncertainty_map_b]) > 0
                ).sum()
        N = self.df.shape[0]

        # Get the corresponding distribution
        I_min, I_max = beta.interval(0.95, 1 + k_a_b, 1 + N - k_a_b)

        # Compute the bound of the credible interval
        distribution = beta.pdf(
                np.linspace(0, 1, 201), 1 + k_a_b,
                1 + N - k_a_b
                )
        return {
                'k_a_b': k_a_b,
                'N': N,
                'I_min': I_min,
                'I_max': I_max,
                'distribution': distribution,
            }
        pass

    def get_statistical_tests(self) -> dict:
        """Plot the statistical tests

        :return: Return all the values of the statistical test in the form
        of an dictionnary
        """
        return {
                uncertainty_map_b: {
                    uncertainty_map_a: None if uncertainty_map_a == uncertainty_map_b \
                            else self.get_statistical_test_a_b(
                                uncertainty_map_a,
                                uncertainty_map_b
                                )
                            for uncertainty_map_a in self.df.columns
                            }
                for uncertainty_map_b in self.df.columns
            }

    def plot_statistical_test_a_b(
            self, uncertainty_map_a: str,
            uncertainty_map_b: str
            ) -> dict:
        """Plot the statistical test

        :param uncertainty_map_a: Name ot the uncertainty map a
        :param uncertainty_map_b: Name ot the uncertainty map b
        """
        # Clear the figure
        plt.clf()

        # Case uncertainty map a and b are the same
        if self.df.columns.tolist().index(
                uncertainty_map_a
                ) >= self.df.columns.tolist().index(
                        uncertainty_map_b
                        ):
            return plt.gcf()

        # Define x axis
        x = np.linspace(0, 1, 201)

        # Get the data
        data = self.get_statistical_test_a_b(
                uncertainty_map_a,
                uncertainty_map_b
                )

        # Plot title
        plt.subplots_adjust(top=0.75)
        plt.title(
                'A: {}\nB: {}'.format(
                    uncertainty_map_a.replace('_', ' '),
                    uncertainty_map_b.replace('_', ' ')
                    ), fontsize= 30
                )

        # Set ticks
        plt.tick_params(labelsize=30)
        plt.yticks([], [])

        # Plot distribution
        plt.plot(x, data['distribution'])

        plt.vlines(
            x[data['distribution'].argmax()], ymin=0,
            ymax=data['distribution'].max(),
            linestyles='dashed',
            color='b'
            )

        plt.fill_between(
            x[
                (x>data['I_min']) * (x < data['I_max'])
                ],
            data['distribution'][
                (x>data['I_min']) * (x < data['I_max'])
                ],
            alpha=0.5
        )

        # Plot expected from random
        plt.vlines(
            0.5, ymin=0, ymax=data['distribution'].max(),
            linestyles='dashed',
            color='r'
            )

        # Plot text
        x_text = 0 if data['k_a_b'] > data['N'] / 2 else 0.54
        y_text = 6 * data['distribution'].max() / 8
        plt.text(
            x_text, y_text,
            '${} = {}$'.format(
                'k_{A, B}', data['k_a_b'],
                ), fontsize=30,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            )
        return plt.gcf()

    def plot_statistical_tests(
            self
            ) -> dict:
        """Plot the statistical tests
        """
        return {
                uncertainty_map_b: {
                        uncertainty_map_a: self.plot_statistical_test_a_b(
                            uncertainty_map_a, uncertainty_map_b
                            )
                        for uncertainty_map_a in self.df.columns
                        }
                for uncertainty_map_b in self.df.columns
            }

    def generate_credible_interval_latex_table(
            self, caption: str = None, label: str = None
            ) -> str:
        """Display the 95% equally tailed uncertainty credible interval
        in a latex format

        :param caption: Caption of the latex table
        :param label: Label of the latex table
        """
        # Generate dataframe structure
        latex_dataframe = pd.DataFrame(
                {
                    column: [
                        ''
                        for _ in self.df.columns[:-1]
                        ]
                    for column in self.df.columns[1:]
                    }, index=self.df.columns[:-1]
                )

        # Fill dataframe
        data = self.get_statistical_tests()

        # Get uncertainty map list
        for j, uncertainty_map_a in enumerate(self.df.columns[:-1]):
            for i, uncertainty_map_b in  enumerate(self.df.columns[1:]):
                if not data[uncertainty_map_a][uncertainty_map_b] is None:
                    I_min = data[uncertainty_map_b][uncertainty_map_a]['I_min'].__round__(2)
                    I_max = data[uncertainty_map_b][uncertainty_map_a]['I_max'].__round__(2)
                    content = '[{}, {}]'.format(I_min, I_max)
                    if (I_min < .5 ) == (I_max < .5):
                        content = '$textbf{' + content + '}$'
                    else:
                        content = '$' + content + '$'
                    if i >= j:
                        latex_dataframe.loc[
                                uncertainty_map_a, uncertainty_map_b
                                ] = content

        # Set size
        column_format = (
                'p{' +\
                '{}\\textwidth'.format(
                    (1/(len(self.df.columns) + 2)).__round__(3)
                    ) +\
                '}'
                ) * (len(self.df.columns) + 1)

        # Generate tex code
        latex_code = latex_dataframe.to_latex(
                column_format=column_format
                )

        # Reformat
        latex_code = re.sub(
            r"\\[a-z]*rule",
            r"\\hline",
            latex_code
            ).replace(
                    '\\$', '$'
                    ).replace(
                            'textbf', '\\textbf'
                            ).replace(
                                    '\\{', '{'
                                    ).replace(
                                        '\\}', '}'
                                        )

        return latex_code

