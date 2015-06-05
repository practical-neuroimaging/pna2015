""" Do equivalent of SPM reorient on ds107 image
"""

import nibabel as nib

with open('ds114_sub009_highres.nii', 'rb') as fobj:
    hdr = nib.Nifti1Header.from_fileobj(fobj)

rot = nib.eulerangles.euler2mat(z=0.3)
trans = [-10, -12, -15]
moving = nib.affines.from_matvec(rot, trans)
affine = moving.dot(hdr.get_best_affine())
hdr.set_sform(affine)
hdr.set_qform(affine)
hdr['magic'] = b'ni1'

with open('ds114_sub009_highres_moved.hdr', 'wb') as fobj:
    hdr.write_to(fobj)
