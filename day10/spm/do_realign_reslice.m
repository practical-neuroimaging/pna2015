% Octave / MATLAB script to do realign / reslice
file_volno = spm_select('ExtFPList', pwd, 'ds114_sub009_t2r1.nii', inf);
spm_realign(file_volno)
spm_reslice(file_volno)
