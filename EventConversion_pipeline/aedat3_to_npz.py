#!/usr/bin/env python
# coding: utf-8

# ## aedat3.1 to npz

# In[17]:


import os
import numpy as np
import struct

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

# Assuming 'data' is your dataset loaded from the AEDAT file
data['t'] = data['t'].astype(np.int64)  # Convert to 32-bit integer if the range allows
data['x'] = data['x'].astype(np.int64)  # Convert to 16-bit integer if possible
data['y'] = data['y'].astype(np.int64)  # Same as above for 'y'
data['p'] = data['p'].astype(np.int8)   # Polarity often needs only 2 values (0, 1)


# Save data to NPZ file directly
npz_filename = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/2output_new.npz'
np.savez_compressed(npz_filename, t=data['t'], x=data['x'], y=data['y'], p=data['p'])

print(f'Data saved to {npz_filename}')


# ## npz to csv

# In[18]:


import numpy as np

# Load the NPZ file
npz_filename = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/2output_new.npz'  # Adjust this to the path of your NPZ file
data = np.load(npz_filename)

# Extract the data arrays
timestamps = data['t']
x_coords = data['x']
y_coords = data['y']
polarities = data['p']

# Create a CSV file and write the arrays
csv_filename = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/3output_new.csv'  # Name of the CSV file to create
with open(csv_filename, 'w') as csv_file:
    # Write header
    csv_file.write('t,x,y,p\n')
    
    # Write data rows
    for t, x, y, p in zip(timestamps, x_coords, y_coords, polarities):
        csv_file.write(f'{t},{x},{y},{p}\n')

print(f'Data saved to {csv_filename}')


# In[ ]:




