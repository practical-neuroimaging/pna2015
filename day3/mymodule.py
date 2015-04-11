""" This is mymodule

It has useful functions in it.
"""

# Don't forget to import the other modules used by the code in this module
import numpy as np

import nibabel as nib

def vol_means(image_fname):
    img = nib.load(image_fname, mmap=False)
    data = img.get_data()
    means = []
    for i in range(data.shape[-1]):
        vol = data[..., i]
        means.append(np.mean(vol))
    return means
