'''
Read single scan (given scan number in run_num) and extract scan data (Data),
duration of scan in seconds (scan_time), trigger count (trig_count), and
configured trigger frequency (trig_frequency).
'''


import json
import numpy as np
import matplotlib.pyplot as plt

run_num = str(86)
dir_name = (6-len(run_num))*'0' + run_num + '_std_digitalStatic'

f_data = open(dir_name + '/FELIG_00_OccupancyMap.json')
data = json.load(f_data)
Data = np.array(data.get('Data'))
f_data.close()



f_log = open(dir_name + '/scanLog.json')
log_data = json.load(f_log)
f_log.close()

scan_time = log_data['stopwatch']['scan']/1000



f_config = open(dir_name + '/std_digitalStatic.json')
config_data = json.load(f_config)
f_config.close()

trig_count = config_data['scan']['loops'][0]['config']['trig_count']
trig_frequency = config_data['scan']['loops'][0]['config']['trig_frequency']