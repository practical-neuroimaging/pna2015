"""
Test spm_funcs module

This test script prints out the mean of the SPM global values as calculated by
us, and the mean of the SPM global values as calculated by SPM.
"""
# Python 3 compatibility
from __future__ import print_function, division

import numpy as np

import spm_funcs

glob_vals = spm_funcs.get_spm_globals('ds107_sub012_t1r2.nii')
expected_values = np.loadtxt('global_signals.txt')

# These two values should be very similar
print(np.mean(glob_vals), np.mean(expected_values))
