#!/usr/bin/env python
# coding: utf-8

# In[2]:


import subprocess
import os
import numpy as np
import csv


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


# First part: Convert AEDAT2 to CSV
def read_aedat_save_to_csv(aedat_file: str, csv_file: str):
    """
    Convert a single AEDAT file to a CSV file.
    """
    """
    Convert a single AEDAT file to a CSV file.
    
    Parameters:
    - aedat_file: Path to the AEDAT file.
    - csv_file: Path to the output CSV file.
    """
    with open(aedat_file, 'rb') as fp:
        t, x, y, p = load_events(fp,
                                 x_mask=0xfE,
                                 x_shift=1,
                                 y_mask=0x7f00,
                                 y_shift=8,
                                 polarity_mask=1,
                                 polarity_shift=None)
        
        # Convert polarity to the desired format
        p_converted = 1 - p.astype(int)
        
        # Prepare the data for CSV writing
        data_to_save = zip(t, 127 - y, 127 - x, p_converted)
        
        # Write the data to a CSV file
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Optionally write headers
            # writer.writerow(['t', 'x', 'y', 'p'])
            for row in data_to_save:
                writer.writerow(row)
                
        print(f'Save [{aedat_file}] to [{csv_file}].')

# Second part: Compile C++ code and convert CSV to EVT2
def compile_cpp_code(cpp_project_path):
    # Define the build directory path
    build_path = os.path.join(cpp_project_path, 'build')
    
    # Check if the build directory already exists
    if not os.path.exists(build_path):
        print(f"Compiling C++ project at {cpp_project_path}...")
        
        # Create and enter the build directory
        os.makedirs(build_path, exist_ok=True)
        os.chdir(build_path)

        # Run CMake commands
        subprocess.run(['cmake', '..', '-DCMAKE_BUILD_TYPE=Release'], check=True)
        subprocess.run(['cmake', '--build', '.', '--config', 'Release'], check=True)
    else:
        print("Build directory exists. Skipping compilation.")

def convert_csv_to_evt2(cpp_project_path, csv_file_path, evt2_output_path):
    """
    Run the compiled C++ executable to convert a CSV file to a .raw file.
    
    Parameters:
    - cpp_project_path: Path to the root directory of the C++ project.
    - csv_file_path: Path to the input CSV file.
    - raw_output_path: Path to the output .raw file.
    """
    # Compile the C++ project first
    compile_cpp_code(cpp_project_path)

    # Define the path to the executable
    executable_path = os.path.join(cpp_project_path, 'build', 'metavision_evt2_raw_file_encoder')

    # Define the command to run the executable
    command = [executable_path, raw_output_path, csv_file_path]
    
    # Run the command
    subprocess.run(command, check=True)
    print(f"Converted {csv_file_path} to {raw_output_path}")

if __name__ == '__main__':
    # Update these paths according to your files' locations
    aedat_file_path = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/new/aedat2_cifar10_automobile_1.aedat'
    intermediate_csv_file_path = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/new/camera__clalp.csv'
    raw_output_path = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/new/aedat2_re_cifar10_automobile_1.raw'
    cpp_project_path = '/home/aitsam/openeb/pipeline/cpp_samples/metavision_evt2_raw_file_encoder'

    # Step 1: Convert AEDAT2 to CSV
    read_aedat_save_to_csv(aedat_file_path, intermediate_csv_file_path)
    
    # Step 2: Convert CSV to EVT2
    convert_csv_to_evt2(cpp_project_path, intermediate_csv_file_path, raw_output_path)


# In[ ]:




