"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-11-26

**Project** : monte_carlo_dropout

**Implement MelbaDistributionAnalysis class**

"""
import seaborn as sn
import matplotlib
import matplotlib.pyplot as plt
from monte_carlo_analysis.analysis import Analysis
from matplotlib import rc
rc('text',usetex=False)


class MelbaDistributionAnalysis(Analysis):
    """Implement MelbaDistributionAnalysis class

    :param df: Dataframe following the following structure ['class', 'uncertainty_map', 'metric']
    or ['uncertainty_map_a', 'uncertainty_map_b' ...]
    """
    def __init__(self, df: list) -> None:
        self.df = df


    def plot(self, metric: str) -> None:
        """Plot the distribution of the metric

        :param metric: Name of the plotted class
        """
        # Set figure
        plt.clf()
        plt.figure(
                figsize=(12,4), constrained_layout=True,
                dpi=1000
                )
        sn.set(font_scale=1.5)

        if 'class' in self.df.columns:
            sn.boxplot(
                    hue="uncertainty_map", x=metric, y="class",
                    data=self.df, palette="Set3", ax=plt.gca(),
                    orient="h"
                    )
            plt.legend(bbox_to_anchor=(1.01, 1),borderaxespad=0)
        else:
            sn.boxplot(
                    y="uncertainty_map", x=metric,
                    data=self.df, palette="Set3", ax=plt.gca()
                    )

        # Improve layout
        plt.gca().set_ylabel('')
        plt.gca().set_xlabel('')
        plt.tight_layout()

        return plt.gcf()

