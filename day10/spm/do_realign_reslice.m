% Octave / MATLAB script to do realign / reslice
vols = spm_vol('ds114_sub009_t2r1.nii');
spm_realign(vols);
spm_reslice(vols);
