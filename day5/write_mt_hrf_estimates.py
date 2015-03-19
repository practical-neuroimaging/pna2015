""" Use nitime library to create "mt_fir.txt" file

With much thanks to Ariel Rokem.

http://nipy.org/nitime/examples/event_related_fmri.html
"""
import numpy as np

from matplotlib.mlab import csv2rec

# Import nitime routines
import nitime
import nitime.timeseries as ts
import nitime.analysis as nta

# Load the example data from nitime directories
import os
data_path = os.path.join(nitime.__path__[0], 'data')
data = csv2rec(os.path.join(data_path, 'event_related_fmri.csv'))

# Load the data into nitime formats
TR = 2.
t1 = ts.TimeSeries(data.bold, sampling_interval=TR)
t2 = ts.TimeSeries(data.events, sampling_interval=TR)

# Analyze
len_et = 15  # This is given in number of samples, not time!
E = nta.EventRelatedAnalyzer(t1, t2, len_et)
FIR = E.FIR

times = FIR.time / float(ts.time_unit_conversion['s'])
mt_fir = FIR.data.mean(axis=0)

np.savetxt('mt_hrf_estimates.txt', mt_fir)
