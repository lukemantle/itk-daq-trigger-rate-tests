'''
Read one scan and extract data
'''

import json
import numpy as np
import matplotlib.pyplot as plt

f = open('000101_std_digitalStatic/FELIG_00_OccupancyMap.json')
data = json.load(f)

Data = np.array(data.get('Data'))