'''
Numpy arrays matching hit patterns of the same name
'''

import numpy as np

shape = (1280,2)

eight_clusters_per_abc = np.zeros(shape)
eight_clusters_per_abc[15::32,:] += 1

sixteen_clusters_per_abc = np.zeros(shape)
sixteen_clusters_per_abc[15::16,:] += 1

thirtytwo_clusters_per_abc = np.zeros(shape)
thirtytwo_clusters_per_abc[7::8,:] += 1

sixtyfour_clusters_per_abc = np.zeros(shape)
sixtyfour_clusters_per_abc[3::4,:] += 1


def dizzy(n):
  key = np.concatenate((np.ones(n),np.zeros(n)))
  left = np.tile(key,int(640/n))
  right = 1-left
  return np.array([left,right]).T

def dizzy_inv(n):
  return 1-dizzy(n)

dizzy_32 = dizzy(32)
dizzy_16 = dizzy(16)
dizzy_8 = dizzy(8)
dizzy_4 = dizzy(4)
dizzy_2 = dizzy(2)

'''
Given a hit pattern (string), looks in hit_pattern_log.txt and returns an array
of all the run numbers with that hit pattern
'''
def get_runs_of_hit_pattern(hit_pattern):
  f = np.loadtxt('modules/hit_pattern_log.txt', dtype='str', delimiter=',')
  return f[:,0][np.where(f[:,1] == hit_pattern)]

# examples
test = get_runs_of_hit_pattern('dizzy_32')