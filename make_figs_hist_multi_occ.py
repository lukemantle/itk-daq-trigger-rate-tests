import numpy as np
import modules.hit_patterns as hitpats
from modules.hist_multi_occ import make_hist_multi_occ

pats = [hitpats.eight_clusters_per_abc, hitpats.sixteen_clusters_per_abc,
        hitpats.thirtytwo_clusters_per_abc, hitpats.sixtyfour_clusters_per_abc]
patnames = ['eight_clusters_per_abc', 'sixteen_clusters_per_abc',
            'thirtytwo_clusters_per_abc', 'sixtyfour_clusters_per_abc']


'''
runs_list is list of run numbers, arranged as shown below.
Each element in the list is an array of run numbers, which will together
form the data set for one plot.

  1 kHz    10 kHz
[[  ***  ,  ***  ],  eight_clusters_per_abc
 [  ***  ,  ***  ],  sixteen_clusters_per_abc
 [  ***  ,  ***  ],  thirtytwo_clusters_per_abc
 [  ***  ,  ***  ]]  sixtyfour_clusters_per_abc
'''

runs_list = [[np.arange(166,181), np.arange(181,192)],
             [np.arange(140,155), np.arange(155,166)],
             [np.arange(87,102), np.arange(102,113)],
             [np.concatenate((np.arange(113,125),np.arange(126,129))),
              np.arange(129,140)]]
false_true = [False, True]
counts = ['1000','10000']

# Loop through elements of runs_list to create plots
for pat in range(4):
  for count in range(2):
    for log in range(2):
      make_hist_multi_occ(pats[pat], patnames[pat], runs_list[pat][count],
                          false_true[log], counts[count])