#!/usr/bin/env python
# coding: utf-8

# ## aedat2 to npz

# In[6]:


import os
import time
import numpy as np
import multiprocessing
from concurrent.futures import ThreadPoolExecutor

# Assuming the functions 'load_events', 'np_savez', and other necessary functions are defined as in your initial code snippet
np_savez = np.savez_compressed  # Assuming you want to save the dataset compressed

y_mask = 0x7FC00000
y_shift = 22

x_mask = 0x003FF000
x_shift = 12

polarity_mask = 0x800
polarity_shift = 11

valid_mask = 0x80000000
valid_shift = 31


EVT_DVS = 0  # DVS event type
EVT_APS = 1  # APS event

def read_bits(arr, mask=None, shift=None):
    if mask is not None:
        arr = arr & mask
    if shift is not None:
        arr = arr >> shift
    return arr


def parse_raw_address(addr,
                      x_mask=x_mask,
                      x_shift=x_shift,
                      y_mask=y_mask,
                      y_shift=y_shift,
                      polarity_mask=polarity_mask,
                      polarity_shift=polarity_shift):
    polarity = read_bits(addr, polarity_mask, polarity_shift).astype(np.bool_)
    x = read_bits(addr, x_mask, x_shift)
    y = read_bits(addr, y_mask, y_shift)
    return x, y, polarity


def load_raw_events(fp,
                    bytes_skip=0,
                    bytes_trim=0,
                    filter_dvs=False,
                    times_first=False):
    p = skip_header(fp)
    fp.seek(p + bytes_skip)
    data = fp.read()
    if bytes_trim > 0:
        data = data[:-bytes_trim]
    data = np.fromstring(data, dtype='>u4')
    if len(data) % 2 != 0:
        print(data[:20:2])
        print('---')
        print(data[1:21:2])
        raise ValueError('odd number of data elements')
    raw_addr = data[::2]
    timestamp = data[1::2]
    if times_first:
        timestamp, raw_addr = raw_addr, timestamp
    if filter_dvs:
        valid = read_bits(raw_addr, valid_mask, valid_shift) == EVT_DVS
        timestamp = timestamp[valid]
        raw_addr = raw_addr[valid]
    return timestamp, raw_addr

def skip_header(fp):
    p = 0
    lt = fp.readline()
    ltd = lt.decode().strip()
    while ltd and ltd[0] == "#":
        p += len(lt)
        lt = fp.readline()
        try:
            ltd = lt.decode().strip()
        except UnicodeDecodeError:
            break
    return p

def load_events(
        fp,
        filter_dvs=False,
        # bytes_skip=0,
        # bytes_trim=0,
        # times_first=False,
        **kwargs):
    timestamp, addr = load_raw_events(
        fp,
        filter_dvs=filter_dvs,
        #   bytes_skip=bytes_skip,
        #   bytes_trim=bytes_trim,
        #   times_first=times_first
    )
    x, y, polarity = parse_raw_address(addr, **kwargs)
    return timestamp, x, y, polarity




def read_aedat_save_to_np(aedat_file: str, np_file: str):
    """
    Convert a single AEDAT file to an NPZ file.
    
    Parameters:
    - aedat_file: Path to the AEDAT file.
    - np_file: Path to the output NPZ file.
    """
    with open(aedat_file, 'rb') as fp:
        t, x, y, p = load_events(fp,
                                 x_mask=0xfE,
                                 x_shift=1,
                                 y_mask=0x7f00,
                                 y_shift=8,
                                 polarity_mask=1,
                                 polarity_shift=None)
        np_savez(np_file,
                 t=t,
                 x=127 - y,
                 y=127 - x,
                 p=1 - p.astype(int))
        print(f'Save [{aedat_file}] to [{np_file}].')

if __name__ == '__main__':
    aedat_file = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/new/aedat2_cifar10_automobile_1.aedat'  # Update with the actual path to your AEDAT file
    np_file = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/new/aedat2_cifar10_automobile_1.npz'  # Update with the desired path for the output NPZ file
    
    read_aedat_save_to_np(aedat_file, np_file)


# In[ ]:




