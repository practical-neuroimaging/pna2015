""" Script to run SPM processing on ds114 task2

Should be run from directory containing subject directories ('sub001', etc)
"""

from os.path import split as psplit, join as pjoin, abspath, exists, dirname

import numpy as np
import numpy.linalg as npl

import nibabel as nib

from stimuli import events2neural
from spm_funcs import spm_hrf

# Import our own configuration for nipype
import nipype_settings

import nipype.interfaces.spm as spm

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

def prefix_path(prefix, path):
    dirname, fname = psplit(path)
    return pjoin(dirname, prefix + fname)


def degz(path):
    return path[:-3] if path.endswith('.gz') else path


def process_subject(func_fname, anat_fname):
    # Drop dummy volumes
    img = nib.load(func_fname);
    dropped_img = nib.Nifti1Image(img.get_data()[..., n_dummies:],
                                img.affine,
                                img.header)
    fixed_fname = prefix_path('f', degz(func_fname))
    nib.save(dropped_img, fixed_fname)

    # Ungz anatomical
    if anat_fname.endswith('.gz'):
        anat_img = nib.load(anat_fname)
        anat_fname = degz(anat_fname)
        nib.save(anat_img, anat_fname)

    # Slice time correction
    num_slices = img.shape[2]
    time_for_one_slice = TR / num_slices
    TA = TR - time_for_one_slice
    st = spm.SliceTiming()
    st.inputs.in_files = fixed_fname
    st.inputs.num_slices = num_slices
    st.inputs.time_repetition = TR
    st.inputs.time_acquisition = TA
    st.inputs.slice_order = order_func(num_slices)
    st.inputs.ref_slice = ref_slice
    st.run()
    fixed_stimed = prefix_path('a', fixed_fname)

    # Realign
    realign = spm.Realign()
    realign.inputs.in_files = fixed_stimed
    # Do not write resliced files, do write mean image
    realign.inputs.write_which = write_which
    realign.run()

    # Coregistration
    coreg = spm.Coregister()
    # Coregister structural to mean image from realignment
    coreg.inputs.target = prefix_path('mean', fixed_stimed)
    coreg.inputs.source = anat_fname
    coreg.run()

    # Normalization / resampling with normalization + realign params
    seg_norm = spm.Normalize12()
    seg_norm.inputs.image_to_align = anat_fname
    seg_norm.inputs.apply_to_files = fixed_stimed
    seg_norm.inputs.write_bounding_box = bounding_box
    seg_norm.inputs.write_voxel_sizes = voxel_sizes
    seg_norm.run()


def get_scans(subj_dir):
    subj_dir = abspath(subj_dir)
    func_fname = pjoin(subj_dir,
                       'BOLD',
                       'task002_run001',
                       'bold.nii.gz')
    anat_fname = pjoin(subj_dir,
                       'anatomy',
                       'highres001.nii.gz')
    return func_fname, anat_fname


def pre_process(subjects):
    for subject in subjects:
        func_fname, anat_fname = get_scans(subject)
        assert exists(func_fname)
        assert exists(anat_fname)
        process_subject(func_fname, anat_fname)


def get_cond(subj_dir):
    subj_dir = abspath(subj_dir)
    return pjoin(subj_dir,
                 'model',
                 'model001',
                 'onsets',
                 'task002_run001',
                 'cond001.txt')


def run_model(func_fname, cond_file, TR, n_dropped, sigma_thresh):
    img = nib.load(func_fname)
    data = img.get_data()
    n_vols = data.shape[-1]
    vol_shape = data.shape[:3]
    n_voxels = np.prod(vol_shape)
    data_2d = np.reshape(data, (-1, n_vols)).T
    neural = events2neural(cond_file, TR, n_vols + n_dropped)[n_dropped:]
    times = np.arange(0, 24, TR)
    hrf = spm_hrf(times)
    hemo = np.convolve(neural, hrf)[:n_vols]
    X = np.ones((n_vols, 3))
    X[:, 0] = hemo
    X[:, 1] = np.linspace(-1, 1, n_vols)
    betas = npl.pinv(X).dot(data_2d)
    fitted = X.dot(betas)
    residuals = data_2d - fitted
    df = n_vols - npl.matrix_rank(X)
    MRSS = (residuals ** 2).sum(axis=0) / df
    # Mask out voxels with tiny variance
    mask = MRSS > sigma_thresh
    c = np.array([1, 0, 0])
    design_variance = c.dot(npl.pinv(X.T.dot(X)).dot(c))
    con_1d = c.dot(betas)[mask]
    var_1d = np.sqrt(MRSS[mask] * design_variance)
    t_1d = con_1d / var_1d
    con_data = np.zeros(n_voxels)
    con_data[mask] = con_1d
    t_data = np.zeros(n_voxels)
    t_data[mask] = t_1d
    pth = dirname(func_fname)
    con_img = nib.Nifti1Image(con_data.reshape(vol_shape),
                              img.affine,
                              img.header)
    nib.save(con_img, pjoin(pth, 'con_task2.nii'))
    t_img = nib.Nifti1Image(t_data.reshape(vol_shape),
                            img.affine,
                            img.header)
    nib.save(t_img, pjoin(pth, 't_task2.nii'))


def run_models(subjects):
    for subject in subjects:
        func_fname, anat_fname = get_scans(subject)
        proc_func_fname = degz(prefix_path('waf', func_fname))
        assert exists(proc_func_fname)
        cond_fname = get_cond(subject)
        assert exists(cond_fname)
        run_model(proc_func_fname, cond_fname, TR, n_dummies, 0.01)


def pool_cons(subjects):
    imgs = []
    for subject in subjects:
        func_fname, anat_fname = get_scans(subject)
        pth = dirname(func_fname)
        imgs.append(pjoin(pth, 'con_task2.nii'))
    cons = nib.funcs.concat_images(imgs)
    nib.save(cons, 'all_con_task2.nii')


SUBJECTS = [
    'sub001',
    'sub002',
    'sub003',
    'sub004',
    'sub005',
    'sub006',
    'sub007',
    'sub008',
    'sub009',
    'sub010']


def main():
    pre_process(SUBJECTS)
    run_models(SUBJECTS)
    pool_cons(SUBJECTS)


if __name__ == '__main__':
    main()
