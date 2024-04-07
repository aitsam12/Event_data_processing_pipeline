#!/usr/bin/env python
# coding: utf-8

# ## npz to bin

# In[2]:


import numpy as np

def save_npz_to_bin(npz_file: str, bin_file: str):
    """
    Convert an NPZ file containing event data back into a binary (.bin) file format.
    
    Parameters:
    - npz_file: Path to the input NPZ file containing event data.
    - bin_file: Path to the output binary file.
    """
    # Load events from NPZ
    data = np.load(npz_file)
    t = data['t']
    x = data['x']
    y = data['y']
    p = data['p']

    # Convert events to binary format and write to file
    with open(bin_file, 'wb') as bin_f:
        for timestamp, xpos, ypos, polarity in zip(t, x, y, p):
            # Reconstruct the binary data for each event
            x_bin = (xpos & 0xFF) << 32
            y_bin = (ypos & 0xFF) << 24
            p_bin = (polarity & 0x1) << 23
            t_bin = timestamp & 0x7FFFFF  # Assuming 22 bits for timestamp
            
            # Convert the aggregate binary data to a Python integer before calling to_bytes
            event_bin = int(x_bin | y_bin | p_bin | t_bin)
            
            # Write the binary event to the file
            bin_f.write(event_bin.to_bytes(5, byteorder='big'))

    print(f'Save [{npz_file}] to [{bin_file}].')


# Example usage
npz_file_path = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/new/image_0002.npz'  # Update with the actual path to your NPZ file
bin_file_path = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/new/NPZ_image_0002_converted.bin'  # Path for the output binary file

save_npz_to_bin(npz_file_path, bin_file_path)


# In[ ]:




