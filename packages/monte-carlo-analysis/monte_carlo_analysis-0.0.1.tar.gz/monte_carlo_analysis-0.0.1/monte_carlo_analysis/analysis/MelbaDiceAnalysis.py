"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-11-27

**Project** : monte_carlo_analysis

**Implement MelbaDiceAnalysis class**

"""
import seaborn as sn
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np


class MelbaDiceAnalysis(object):
    """Implement MelbaDiceAnalysis class

    :param df: Dataframe following the next structure ['class_1', 'class_2', ...]
    :param bins: Bins of the histogram
    """
    def __init__(
            self, df, bins: tuple = np.linspace(0, 1, 50)
            ) -> None:
        self.df = df
        self.bins = bins

    def plot(self, output_class: str) -> matplotlib.figure.Figure:
        """Plot the histograms of the dice score
        per class

        :param output_class: Output class to plot
        :return: Matplotlib figure
        """
        # Clear figure
        plt.clf()

        # Generate figure
        sn.set(font_scale=1.8)

        sn.displot(
                self.df, x=output_class,
                bins=self.bins
                )

        # Plot text
        x_text = 0
        y_text = plt.ylim()[1]/2

        plt.text(
            x_text, y_text,
            '${} = {}$\n${} = {}$'.format(
                '\mu',
                self.df[output_class].mean().__round__(2),
                '\sigma',
                self.df[output_class].std().__round__(2)
                ), fontsize=18,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
            )


        # Return figure
        return plt.gcf()

