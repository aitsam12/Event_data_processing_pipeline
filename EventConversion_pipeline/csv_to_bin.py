#!/usr/bin/env python
# coding: utf-8

# ## csv to bin

# In[1]:


import numpy as np
import csv

def save_csv_to_bin(csv_file: str, bin_file: str):
    """
    Convert a CSV file containing event data back into a binary (.bin) file format.
    
    Parameters:
    - csv_file: Path to the input CSV file containing event data.
    - bin_file: Path to the output binary file.
    """
    # Read events from CSV
    with open(csv_file, mode='r', newline='') as file:
        reader = csv.reader(file, delimiter=',')
        events = list(reader)
    
    # Convert events to binary format and write to file
    with open(bin_file, 'wb') as bin_f:
        for event in events:
            t, x, y, p = map(int, event)  # Assuming t, x, y, p are all integers
            # Reconstruct the binary data for each event
            # This example assumes the original binary structure and may need adjustments
            x_bin = (x & 0xFF) << 32
            y_bin = (y & 0xFF) << 24
            p_bin = (p & 0x1) << 23
            t_bin = t & 0x7FFFFF  # Assuming 22 bits for timestamp
            event_bin = (x_bin | y_bin | p_bin | t_bin).to_bytes(5, byteorder='big')
            
            # Write the binary event to the file
            bin_f.write(event_bin)

    print(f'Save [{csv_file}] to [{bin_file}].')

# Example usage
csv_file_path = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/new/image_0002.csv'  # Update with the actual path to your CSV file
bin_file_path = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/new/image_0002_converted.bin'  # Path for the output binary file

save_csv_to_bin(csv_file_path, bin_file_path)


# In[ ]:




