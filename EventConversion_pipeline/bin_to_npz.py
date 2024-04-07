#!/usr/bin/env python
# coding: utf-8

# ## bin to npz

# In[2]:


import numpy as np
from typing import Dict

# Assume load_ATIS_bin and load_origin_data are defined here as provided



# Define a function to load ATIS binary data
def load_ATIS_bin(file_name: str) -> Dict:
    '''
    :param file_name: path of the ATIS binary file
    :type file_name: str
    :return: a dict whose keys are ``['t', 'x', 'y', 'p']`` and values are ``numpy.ndarray``
    :rtype: Dict
    This function is written by referring to https://github.com/jackd/events-tfds .
    Each ATIS binary example is a separate binary file consisting of a list of events. Each event occupies 40 bits as described below:
    bit 39 - 32: Xaddress (in pixels)
    bit 31 - 24: Yaddress (in pixels)
    bit 23: Polarity (0 for OFF, 1 for ON)
    bit 22 - 0: Timestamp (in microseconds)
    '''
    with open(file_name, 'rb') as bin_f:
        # `& 128` is to get the highest bit of an 8-bit binary number
        # `& 127` is to get the remaining 7 bits
        raw_data = np.uint32(np.fromfile(bin_f, dtype=np.uint8))
        x = raw_data[0::5]
        y = raw_data[1::5]
        rd_2__5 = raw_data[2::5]
        p = (rd_2__5 & 128) >> 7
        t = ((rd_2__5 & 127) << 16) | (raw_data[3::5] << 8) | (raw_data[4::5])
    return {'t': t, 'x': x, 'y': y, 'p': p}


# Define a function to load origin data from binary files
def load_origin_data(file_name: str) -> Dict:
    '''
    :param file_name: path of the events file
    :type file_name: str
    :return: a dict whose keys are ``['t', 'x', 'y', 'p']`` and values are ``numpy.ndarray``
    :rtype: Dict

    This function defines how to read the origin binary data.
    '''
    return load_ATIS_bin(file_name)




def read_bin_save_to_np(bin_file: str, np_file: str):
    """
    Load binary event data and save it to a compressed NPZ file.
    
    Parameters:
    - bin_file: Path to the binary file containing event data.
    - np_file: Path to the output NPZ file.
    """
    events = load_origin_data(bin_file)
    np.savez_compressed(np_file,
                        t=events['t'],
                        x=events['x'],
                        y=events['y'],
                        p=events['p'])
    print(f'Save [{bin_file}] to [{np_file}].')

# Example usage
##bin_file_path = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/new/image_0002.bin'  # Update with the actual path
##npz_file_path = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/new/image_0002.npz'  # Update with the desired path
bin_file_path = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/new/111aedat2_cifar10_automobile_1.bin'  # Update with the actual path
npz_file_path = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/new/111222aedat2_cifar10_automobile_1.npz'  # Update with the desired path

read_bin_save_to_np(bin_file_path, npz_file_path)


# In[ ]:




