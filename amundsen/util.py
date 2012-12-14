"""
util.py

Utility functions for Amundsen.
"""

from numpy import array
from numpy.random import sample


def weighted_sample(iterable, weights, n=None):
    if len(iterable) != len(weights):
        raise Exception('Length mismatch')
    count = len(iterable) if n is None else n
    # Normalize weights
    wt_sum = float(sum(weights))
    aliases = array(w / wt_sum for w in weights).cumsum()
    # Get indices to include in sample
    indices = aliases.searchsorted(sample(count))
    return array(iterable[i] for i in indices)
