#!/usr/bin/env python
# coding: utf-8

# ## aedat3.1 to csv

# In[1]:


import os
import numpy as np
import struct
import csv

def load_aedat_v3(file_name):
    '''
    Load AEDAT v3 file and return data as a dictionary with keys 't', 'x', 'y', 'p'.
    Each key corresponds to a numpy.ndarray of timestamps, x coordinates, y coordinates, and polarity values respectively.
    '''
    with open(file_name, 'rb') as bin_f:
        # Skip ASCII header
        line = bin_f.readline()
        while line.startswith(b'#'):
            if line == b'#!END-HEADER\r\n':
                break
            else:
                line = bin_f.readline()

        txyp = {'t': [], 'x': [], 'y': [], 'p': []}
        while True:
            header = bin_f.read(28)
            if not header:
                break

            # Read and unpack header
            e_type, e_source, e_size, e_offset, e_tsoverflow, e_capacity, e_number, e_valid = struct.unpack('HHIIIIII', header)

            data_length = e_capacity * e_size
            data = bin_f.read(data_length)
            counter = 0

            if e_type == 1:  # Event type 1: Polarity event
                while counter < len(data):
                    aer_data, timestamp = struct.unpack('II', data[counter:counter + 8])
                    timestamp |= e_tsoverflow << 31
                    x, y, pol = (aer_data >> 17) & 0x7FFF, (aer_data >> 2) & 0x7FFF, (aer_data >> 1) & 1
                    txyp['x'].append(x)
                    txyp['y'].append(y)
                    txyp['t'].append(timestamp)
                    txyp['p'].append(pol)
                    counter += e_size

        for key in txyp:
            txyp[key] = np.asarray(txyp[key])
        return txyp

# Load AEDAT file
aedat_file = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/user01_lab.aedat'
data = load_aedat_v3(aedat_file)

# Save data to CSV
csv_filename = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/aedat_csv_file.csv'
np.savetxt(csv_filename, np.column_stack((data['t'], data['x'], data['y'], data['p'])), delimiter=',', header='t,x,y,p', comments='')
print(f'Data saved to {csv_filename}')


# In[ ]:




