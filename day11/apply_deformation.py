import numpy as np
import numpy.linalg as npl

from scipy.ndimage import map_coordinates

import nibabel as nib
from nibabel.affines import apply_affine

# tpms = nib.load('TPM.nii')
# tpm_shape = tpms.shape[:3]
# tpm_affine = tpms.affine
tpm_shape = (121, 145, 121, 6)
tpm_affine = np.array([[  -1.5,    0. ,    0. ,   90. ],
                       [   0. ,    1.5,    0. , -126. ],
                       [   0. ,    0. ,    1.5,  -72. ],
                       [   0. ,    0. ,    0. ,    1. ]])
img = nib.load('ds114_sub009_highres.nii')
distortion_img = nib.load('spm_normalize/y_ds114_sub009_highres.nii')


distortions = distortion_img.get_data()
distortions = np.squeeze(distortions).transpose(3, 0, 1, 2)

native_vox = apply_affine(npl.inv(img.affine), distortions.T).T

resampled_array = map_coordinates(img.dataobj, native_vox)

resampled_img = nib.Nifti1Image(resampled_array, tpm_affine)
nib.save(resampled_img, 'resampled.nii')
