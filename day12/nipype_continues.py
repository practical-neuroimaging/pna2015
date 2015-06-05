""" Script to run SPM processing in nipype
"""

import nipype_settings

import nipype.interfaces.spm as spm

# Start at the slice-time corrected image
base_fname = 'afds114_sub009_t2r1.nii'
structural_fname = 'ds114_sub009_highres.nii'

# Realign
realign = spm.Realign()
realign.inputs.in_files = base_fname
# Do not write resliced files, do write mean image
realign.inputs.write_which = [0, 1]
realign.run()

# Coregistration
coreg = spm.Coregister()
# Coregister structural to mean image from realignment
coreg.inputs.target = 'mean' + base_fname
coreg.inputs.source = structural_fname
coreg.run()

# Normalization / resampling with normalization + realign params
seg_norm = spm.Normalize12()
seg_norm.inputs.image_to_align = structural_fname
seg_norm.inputs.apply_to_files = base_fname
seg_norm.run()

# Smoothing
smooth = spm.Smooth()
smooth.inputs.in_files = 'w' + base_fname
smooth.inputs.fwhm = [8, 8, 8]
smooth.run()
