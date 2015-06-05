""" Script to make rotated volumes

We are going to rotate by:

* 0.1 radians around x, then
* 0.2 radians around y, then
* 0.3 radians around z.

This will involve:

1. Making a new empty volume
2. Making the *inverse* of the rotations above to give *itrans*
3. For each coordinate in the empty volume, apply itrans to get the
   corresponding coordinate in the original volume;
4. Resample at these coordinates

``scipy.ndimage`` will do steps 1, 3 and 4 for us, but we need to do step 2.
"""

import numpy.linalg as npl

from scipy.ndimage import affine_transform

import nibabel as nib
from nibabel.eulerangles import euler2mat

img = nib.load('ds107_sub012_t1r2.nii')
data = img.get_data()
vol0 = data[..., 0]

# The public volume
x_rot, y_rot, z_rot = 0.1, 0.2, 0.3

Mx = euler2mat(x=x_rot)
My = euler2mat(y=y_rot)
Mz = euler2mat(z=z_rot)

orig_to_new = Mz.dot(My).dot(Mx)
new_to_orig = npl.inv(orig_to_new)

rotated_vol0 = affine_transform(vol0, new_to_orig, order=1)

new_img = nib.Nifti1Image(rotated_vol0, img.affine, img.header)
nib.save(new_img, 'rotated_volume.nii')

# The secret volume
x_rot, y_rot, z_rot = 0.0, -0.1, 0.2

Mx = euler2mat(x=x_rot)
My = euler2mat(y=y_rot)
Mz = euler2mat(z=z_rot)

orig_to_new = Mz.dot(My).dot(Mx)
new_to_orig = npl.inv(orig_to_new)

rotated_vol0 = affine_transform(vol0, new_to_orig, order=1)

new_img = nib.Nifti1Image(rotated_vol0, img.affine, img.header)
nib.save(new_img, 'secret_rotated_volume.nii')
