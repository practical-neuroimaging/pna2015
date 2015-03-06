% Get SPM global signal estimate for all volumes in bold 4D
file_volno = spm_select('ExtFPList', pwd, 'ds107_sub012_t1r2.nii', inf);
V = spm_vol(file_volno);
global_signals = ones([length(V), 1]);
for i = 1:length(V)
    global_signals(i) = spm_global(V(i));
end
% Save signal values to a text file
fid = fopen('global_signals.txt','w');
fprintf(fid,'%6.2f\n', global_signals);
fclose(fid);
