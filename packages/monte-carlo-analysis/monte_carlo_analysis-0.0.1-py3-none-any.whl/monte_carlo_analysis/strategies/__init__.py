"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-09-29

**Project** : monte_carlo_analysis

**Module that contains the strategies**

"""
from .Strategy import Strategy
from .TopSingleDistributionStrategy import TopSingleDistributionStrategy
from .AverageSingleDistributionStrategy import AverageSingleDistributionStrategy
from .TopDistributionsSimilarityStrategy import TopDistributionsSimilarityStrategy
from .MultipleDistributionsStrategy import MultipleDistributionsStrategy

from .ClassWiseStrategy import ClassWiseStrategy
from .ClassWiseDistributionStrategy import ClassWiseDistributionStrategy
from .OneVersusAllStrategy import OneVersusAllStrategy

