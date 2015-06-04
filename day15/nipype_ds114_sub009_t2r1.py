""" Script to run SPM processing in nipype
"""

import nibabel as nib

# Import our own configuration for nipype
import nipype_settings

import nipype.interfaces.spm as spm

# Start at the original image
base_fname = 'ds114_sub009_t2r1.nii'
structural_fname = 'ds114_sub009_highres.nii'

# Analysis parameters
TR = 2.5
ref_slice = 1  # 1-based indexing
n_dummies = 4
# Realign write_which
write_which = [0, 1]
# Normalize write parameters
bounding_box = [[-78., -112., -46.], [78., 76., 86.]]
voxel_sizes = [3, 3, 3]

def ascending_interleaved(num_slices):
    """ Return acquisition ordering given number of slices

    Note 1-based indexing for MATLAB.

    Return type must be a list for nipype to use it in the SPM interface
    without error.
    """
    odd = range(1, num_slices + 1, 2)
    even = range(2, num_slices + 1, 2)
    return list(odd) + list(even)

order_func = ascending_interleaved

# Drop dummy volumes
img = nib.load(base_fname);
dropped_img = nib.Nifti1Image(img.get_data()[..., n_dummies:],
                              img.affine,
                              img.header)
nib.save(dropped_img, 'f' + base_fname)

# Slice time correction
num_slices = img.shape[2]
time_for_one_slice = TR / num_slices
TA = TR - time_for_one_slice
st = spm.SliceTiming()
st.inputs.in_files = 'f' + base_fname
st.inputs.num_slices = num_slices
st.inputs.time_repetition = TR
st.inputs.time_acquisition = TA
st.inputs.slice_order = order_func(num_slices)
st.inputs.ref_slice = ref_slice
st.run()

# Realign
realign = spm.Realign()
realign.inputs.in_files = 'af' + base_fname
# Do not write resliced files, do write mean image
realign.inputs.write_which = write_which
realign.run()

# Coregistration
coreg = spm.Coregister()
# Coregister structural to mean image from realignment
coreg.inputs.target = 'meanaf' + base_fname
coreg.inputs.source = structural_fname
coreg.run()

# Normalization / resampling with normalization + realign params
seg_norm = spm.Normalize12()
seg_norm.inputs.image_to_align = structural_fname
seg_norm.inputs.apply_to_files = 'af' + base_fname
seg_norm.inputs.write_bounding_box = bounding_box
seg_norm.inputs.write_voxel_sizes = voxel_sizes
seg_norm.run()
