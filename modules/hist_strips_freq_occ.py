import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import modules.hit_patterns as hitpats
from modules.read_scans import (get_data, get_scan_data, get_trig_count,
                                get_trig_frequency)

def make_hist_strips_freq_occ(pat, patname, runs, counts_text,
                              folder='figures/hist_strips_freq_occ/'):
  if (patname == 'eight_clusters_per_abc'):
    patnum = '8'
  if (patname == 'sixteen_clusters_per_abc'):
    patnum = '16'
  if (patname == 'thirtytwo_clusters_per_abc'):
    patnum = '32'
  if (patname == 'sixtyfour_clusters_per_abc'):
    patnum = '64'
  
  if (counts_text == '1000'):
    counts_short = '1k'
  if (counts_text == '10000'):
    counts_short = '10k'
  
  num_runs = np.shape(runs)[0]
  num_triggered = np.size(np.where(pat)[0])
  
  # Get data from runs
  data, freqs, counts = get_data(runs, [get_scan_data, get_trig_frequency,
                                        get_trig_count])
  occs = (data/counts[:,None,None])
  occs = occs[np.where(np.tile(pat, (num_runs, 1, 1)))]
  freqs_tile = np.ndarray.flatten(np.tile(freqs,(num_triggered,1)).T)
  strips_tile = np.ndarray.flatten(np.tile(np.arange(num_triggered),
                                           (num_runs,1)))
  
  # Set up bins
  strips_min = 0
  strips_max = num_triggered
  freq_min = np.min(freqs)
  freq_max = np.max(freqs) * 1.5
  bins = (np.linspace(strips_min, strips_max, num_triggered),
          np.concatenate((freqs,[freq_max])))
  
  # Make plot
  norm = mpl.colors.Normalize(0.001, 1, clip=True)
  fig, ax = plt.subplots(figsize=(6,4), dpi=400)
  h = ax.hist2d(strips_tile, freqs_tile, bins,
                weights=occs, norm=norm, cmap='magma')
  ax.set_yscale('log')
  # ax.set_title('1 Rx channel, sixteen_clusters_per_abc, 10000 counts')
  ax.set_title('1 Rx channel, ' + patname + ', ' + counts_text + ' counts')
  ax.set_xlabel('strip number (only enabled strips considered)')
  ax.set_ylabel('configured trigger frequency')
  fig.tight_layout()
  fig.colorbar(h[3], label='occupancy', location='right')
  plt.savefig(folder + 'hist_strips_freq_occ_' + patnum + '-per-abc_'
              + counts_short)