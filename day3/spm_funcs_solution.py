"""
This will be your new module defining SPM-like functions

Here you want the get_spm_globals function from the earlier exercise, with
anything imports and other definitions that this function needs.

When you are done, you should be able to run the test_spm_funcs.py script and
see two very similar values printed to the terminal (see the script for what
these values are).  You run the script like this:

    python test_spm_funcs.py

"""
# Python 3 compatibility
from __future__ import print_function, division

import numpy as np

import nibabel as nib


def spm_global(vol):
    T = np.mean(vol) / 8
    return np.mean(vol[vol > T])


def get_spm_globals(fname):
    img = nib.load(fname)
    data = img.get_data()
    spm_vals = []
    for i in range(data.shape[-1]):
        vol = data[..., i]
        spm_vals.append(spm_global(vol))
    return spm_vals
