""" Make images for optimizing affines exercise
"""
import numpy as np

import nibabel as nib

subject = nib.load('ds114_sub009_highres_brain.nii')
template = nib.load('mni_icbm152_t1_tal_nlin_asym_09a.nii')
template_mask = nib.load('mni_icbm152_t1_tal_nlin_asym_09a_mask.nii')

subject_data = subject.get_data()
template_data = template.get_data()
template_mask = template_mask.get_data()
template_masked = template_data * template_mask

subject_resampled = subject_data[40:-40:2, ::2, ::2]
template_resampled = template_masked[::2, ::2, ::2]

template_pre_aff = np.diag([2, 2, 2, 1])
subject_pre_aff = template_pre_aff.copy()
subject_pre_aff[:3, 3] = [40, 0, 0]
nib.save(nib.Nifti1Image(subject_resampled,
                         subject.affine.dot(subject_pre_aff),
                         subject.header),
         'ds114_sub009_highres_brain_222.nii')
nib.save(nib.Nifti1Image(template_resampled,
                         template.affine.dot(template_pre_aff),
                         template.header),
         'mni_icbm152_t1_tal_nlin_asym_09a_masked_222.nii')
