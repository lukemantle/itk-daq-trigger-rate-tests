import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from modules.read_scans import (get_data, get_scan_data, get_trig_count,
                                get_trig_frequency)

def make_hist_multi_occ(pat, patname, runs, log, counts_text,
                        folder='figures/hist_multi_occ/'):
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
  num_enabled = np.size(np.where(pat)[0])
  
  # Get data from runs
  data, freqs, counts = get_data(runs, [get_scan_data, get_trig_frequency,
                                        get_trig_count])
  occs = (data/counts[:,None,None])
  occs = occs[np.where(np.tile(pat, (num_runs, 1, 1)))]
  freqs_tile = np.ndarray.flatten(np.tile(freqs,(num_enabled,1)).T)
  
  # Set up bins
  occ_min = 0
  occ_max = 1
  freq_max = np.max(freqs) * 1.5
  bins = (np.linspace(occ_min, occ_max, 60), np.concatenate((freqs,[freq_max])))
  weights = np.ones(np.shape(occs))/num_enabled
   
  # Make plot
  z_max = 1
  
  if log:
    norm = mpl.colors.LogNorm(0.001, z_max, clip=True)
    logtitle = ', log'
    logtext = '_log'
  else:
    norm = mpl.colors.Normalize(0, z_max, clip=True)
    logtitle = ''
    logtext = ''
  
  fig, ax = plt.subplots(figsize=(6,4), dpi=200)
  h = ax.hist2d(occs, freqs_tile, bins, weights=weights, norm=norm, cmap='magma')
  ax.set_yscale('log')
  ax.set_title('1 Rx channel, ' + patname + ', '
               + counts_text + ' counts' + logtext)
  ax.set_xlabel('occupancy')
  ax.set_ylabel('configured trigger frequency')
  fig.tight_layout()
  fig.colorbar(h[3], label='fraction of enabled strips', location='right')
  plt.savefig(folder + 'hist_multi_occ_' + patnum + '-per-abc_'
              + counts_short + logtext)