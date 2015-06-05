% Octave / MATLAB script to run SPM coregistration
VG = spm_vol('ds114_sub009_t2r1.nii,2');
VF = spm_vol('ds114_sub009_highres_moved.img');
spm_coreg(VG, VF)
