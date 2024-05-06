'''
Make a log-log scatter plot of real trigger frequency (counts / scan time) vs.
configured trigger frequency.
Scans with  100% occupancy are shown in green.
Scans with <100% occupancy are shown in red.
'''

import numpy as np
import matplotlib.pyplot as plt
from modules.read_scans import *
import modules.hit_patterns as hitpats
from modules.hit_patterns import get_runs_of_hit_pattern


patterns = ['eight_clusters_per_abc', 'sixteen_clusters_per_abc',
          'thirtytwo_clusters_per_abc','sixtyfour_clusters_per_abc']

runs_pattern = []
for i in patterns:
  runs_pattern.append(get_runs_of_hit_pattern(i))

freqs_pattern = []
counts_pattern = []
times_pattern = []
real_freqs_pattern = []

for i in range(4):
  freqs, counts, times = np.array(get_data(runs_pattern[i], [get_trig_frequency,
                                                    get_trig_count,
                                                    get_scan_time]))
  real_freqs = counts/times
  freqs_pattern.append(freqs)
  counts_pattern.append(counts)
  times_pattern.append(times)
  real_freqs_pattern.append(real_freqs)

# Make plots
fig, ax = plt.subplots(figsize=(6,4),dpi=200)

alpha = 1
s8 = ax.scatter(freqs_pattern[0], real_freqs_pattern[0], color='red', alpha=alpha)

model = np.logspace(1.8, 5, 30)
s = ax.plot(model, model, color='black')
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim(50,400000)
ax.set_xlabel('trigger frequency, Hz')
ax.set_ylabel('actual frequency = counts/scan time')
ax.set_title('scans with eight_clusters_per_abc hit pattern on one Rx channel')