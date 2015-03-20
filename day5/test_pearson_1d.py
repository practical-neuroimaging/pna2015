"""
Test Pearson module, pearson_1d function

Run with::

    nosetests test_pearson_1d.py

This is a test module.

It is designed to be run the with the "nose" testing package (via the
"nosetests" script.

Nose will look for any functions with "test" in their names, and run them.
Nose reports any errors, or any failures.

A failure is where one of the test conditions run with an "assert" command
fails.  For example, if I did:

    assert_almost_equal(1, 2)

then this would "fail".

So we use the tests to check that the results of our function are (still) as we
expect.
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
