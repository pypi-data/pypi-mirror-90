"""
**Author** : Robin Camarasa

**Institution** : Erasmus Medical Center

**Position** : PhD student

**Contact** : r.camarasa@erasmusmc.nl

**Date** : 2020-09-29

**Project** : monte_carlo_analysis

**Module that contains the uncertainty metrics**

"""
from .UncertaintyMetric import UncertaintyMetric

from .SingleDistributionUncertaintyMetric import SingleDistributionUncertaintyMetric
from .EntropySingleDistribution import EntropySingleDistribution
from .VarianceSingleDistribution import VarianceSingleDistribution

from .DistributionSimilarityUncertaintyMetric import DistributionSimilarityUncertaintyMetric
from .BhattacharyaCoefficentDistributionSimilarity import BhattacharyaCoefficentDistributionSimilarity
from .KullbackLeiblerDivergenceDistributionSimilarity import KullbackLeiblerDivergenceDistributionSimilarity
from .EarthMoverDistanceDistributionSimilarity import EarthMoverDistanceDistributionSimilarity

from .MultipleDistributionsUncertaintyMetric import MultipleDistributionsUncertaintyMetric
from .EntropyMultipleDistributions import EntropyMultipleDistributions
from .MutualInformationMultipleDistribution import MutualInformationMultipleDistributions
