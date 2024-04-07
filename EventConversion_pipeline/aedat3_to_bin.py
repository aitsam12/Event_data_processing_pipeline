#!/usr/bin/env python
# coding: utf-8

# ## aedat to bin

# In[4]:


import csv
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

def save_csv_to_bin(csv_file: str, bin_file: str):
    with open(csv_file, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip the header
        
        with open(bin_file, 'wb') as bin_f:
            for t, x, y, p in reader:
                # First convert strings to floats, then to integers
                x_int, y_int, p_int, t_int = map(lambda v: int(float(v)), [x, y, p, t])

                
                # Assuming a similar format to ATIS for the binary data
                # Adjust the shifting and masking according to your specific needs
                x_bin = (x_int & 0x7FFF) << 17
                y_bin = (y_int & 0x7FFF) << 2
                p_bin = p_int << 1
                event_bin = x_bin | y_bin | p_bin | (1 << 0)  # Last bit set as valid flag
                
                # Timestamp needs to be handled separately
                t_bytes = t_int.to_bytes(4, byteorder='big')
                event_bytes = event_bin.to_bytes(4, byteorder='big')
                
                # Write the event and timestamp to the binary file
                bin_f.write(event_bytes + t_bytes)

    print(f'Save [{csv_file}] to [{bin_file}].')


    
# Load AEDAT file
aedat_file = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/user01_lab.aedat'
data = load_aedat_v3(aedat_file)

# Save data to CSV
csv_filename = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/aedat_csv_file.csv'
np.savetxt(csv_filename, np.column_stack((data['t'], data['x'], data['y'], data['p'])), delimiter=',', header='t,x,y,p', comments='')
print(f'Data saved to {csv_filename}')    

# Define the path for the output binary file
bin_filename = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/aedat_bin_file.bin'

# Convert the CSV to a binary file
save_csv_to_bin(csv_filename, bin_filename)


# In[ ]:





# In[ ]:




