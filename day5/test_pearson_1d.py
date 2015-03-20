"""
Test Pearson module, pearson_1d function

Run with::

    nosetests test_pearson_1d.py
"""
# Python 3 compatibility
from __future__ import print_function, division

import numpy as np

import pearson

from numpy.testing import assert_almost_equal


def test_pearson_1d():
    # Test pearson_1d routine
    x = np.random.rand(22)
    y = np.random.rand(22)
    # Does routine give same answer as np.corrcoef?
    expected = np.corrcoef(x, y)[0, 1]
    actual = pearson.pearson_1d(x, y)
    # Did you, gentle user, forget to return the value?
    if actual is None:
        raise RuntimeError("function returned None")
    assert_almost_equal(expected, actual)
