import json
import numpy as np
import matplotlib.pyplot as plt
import modules.hit_patterns as hitpats

    
'''
Extract one or more pieces of data from each scan in a list of scans. Calls
get_data_one_func for each function.

run_nums      list of numbers correponding to the scans
functions     list of functions, each of which takes the argument dir_name
              and returns a piece of data
scan_config   name of the scan config file (without .json ending) used in all
              the runs (this is used to find trig_count, trig_freq, etc. in
              the scan config file)
**kwargs      dictionary containing arguments other than dir_name to be given
              to the functions. For example, if function_1 takes no extra
              parameters and function_2 takes two extra parameters, then
              **kwargs should be
              {'function_2':[param_1,param_2]}
'''
def get_data(run_nums, functions, scan_config = 'std_digitalStatic',
             **kwargs):
  out = []
  for fun in functions:
    if np.all(kwargs.get(fun.__name__) == None):
      fun_out = get_data_one_func(run_nums, fun)
    else:
      fun_out = get_data_one_func(run_nums, fun, *kwargs[fun.__name__])
    out.append(fun_out)
  return out

'''
Extract one piece of data from each scan in a list of scans.

run_nums      list of numbers correponding to the scans
functions     list of functions, each of which takes the argument dir_name
              and returns a piece of data
scan_config   name of the scan config file (without .json ending) used in all
              the runs (this is used to find trig_count, trig_freq, etc. in
              the scan config file)
**args        (possibly empty) tuple of arguments other than dir_name required
              by function
'''
def get_data_one_func(run_nums, function, *args,
                      scan_config = 'std_digitalStatic'):
  out = []
  for run in run_nums:
    run = str(run)
    dir_name = (6-len(run))*'0' + run + '_' + scan_config
    out.append(function(dir_name, *args))
  return np.array(out)


'''
For each scan in a list of scans, returns True iff occupancy is 100%

run_nums      list of numbers corresponding to the scans
hit_pattern   name of hit pattern (from modules.hit_patterns) corresponding to
              the emulator's hit pattern used in all the scans
scan_config   name of the scan config file (without .json ending) used in all
              the runs (this is used to find trig_count, trig_freq, etc. in
              the scan config file)
'''
def is_full_occupancy(run_nums, hit_pattern,
                      scan_config = 'std_digitalStatic'):
  out = []
  for run in run_nums:
    run = str(run)
    dir_name = (6-len(run))*'0' + run + '_' + scan_config
    data = get_scan_data(dir_name)
    trig_count = get_trig_count(dir_name)
    out.append(np.all(data == trig_count * hit_pattern))
  return out



### Functions that can be used in read_scans

def get_scan_data(dir_name):
  f = open(dir_name + '/FELIG_00_OccupancyMap.json')
  scan_data = json.load(f)
  f.close()
  Data = np.array(scan_data.get('Data'))
  return Data

def get_trig_count(dir_name):
  f = open(dir_name + '/std_digitalStatic.json')
  config_data = json.load(f)
  f.close()
  trig_count = config_data['scan']['loops'][0]['config']['trig_count']
  return trig_count

def get_trig_frequency(dir_name):
  f = open(dir_name + '/std_digitalStatic.json')
  config_data = json.load(f)
  f.close()
  trig_frequency = config_data['scan']['loops'][0]['config']['trig_frequency']
  return trig_frequency

def get_scan_time(dir_name):
  f = open(dir_name + '/scanLog.json')
  log_data = json.load(f)
  f.close()
  scan_time = log_data['stopwatch']['scan']/1000
  return scan_time


# These functions use the ones above

def get_avg_occupancy(dir_name, hit_pattern):
  data = get_scan_data(dir_name)
  counts = get_trig_count(dir_name)
  occs = (data/counts)[np.where(hit_pattern)]
  return np.mean(occs)

### Examples

test_get_occ = get_data_one_func([71,72,73],get_avg_occupancy,
                                 hitpats.eight_clusters_per_abc)
test_get_data= get_data([71,72,73],[get_scan_time,get_avg_occupancy],
                        **{'get_avg_occupancy':
                           [hitpats.eight_clusters_per_abc]})