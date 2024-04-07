#!/usr/bin/env python
# coding: utf-8

# In[1]:


import subprocess
import os
import numpy as np
import struct


def load_aedat_v3_and_save_csv(aedat_file, csv_file):
    '''
    Load AEDAT v3 file and return data as a dictionary with keys 't', 'x', 'y', 'p'.
    Each key corresponds to a numpy.ndarray of timestamps, x coordinates, y coordinates, and polarity values respectively.
    '''
    with open(aedat_file, 'rb') as bin_f:
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

    # Save data to CSV without headers
    np.savetxt(csv_file, np.column_stack((txyp['t'], txyp['x'], txyp['y'], txyp['p'])), delimiter=',', fmt='%d', comments='')

    print(f'Data saved to {csv_file}')



def convert_csv_to_raw(csv_file, raw_output_file):
    """
    Convert a CSV file to a .raw file using the compiled C++ project.
    """
    # Construct the command to run your C++ executable
    executable_path = '/home/aitsam/openeb/pipeline/cpp_samples/metavision_evt3_raw_file_encoder/build/metavision_evt2_raw_file_encoder'  # Adjust this path to where your executable is located
    command = [executable_path, raw_output_file, csv_file]
    
    # Execute the command
    try:
        subprocess.run(command, check=True)
        print(f"Conversion to .raw completed successfully: {raw_output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion to .raw: {e}")

def main(aedat_file, csv_file, raw_output_file):
    # Step 1: Convert AEDAT to CSV
    load_aedat_v3_and_save_csv(aedat_file, csv_file)
    
    # Step 2: Convert CSV to .raw
    convert_csv_to_raw(csv_file, raw_output_file)

if __name__ == '__main__':
    # Define file paths
    aedat_file = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/user01_lab.aedat'  # Path to your AEDAT file
    csv_file = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/output_222.csv'  # Desired path for the intermediate CSV file
    raw_output_file = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/output_file222.raw'  # Desired path for the final .raw file
    
    # Run the main workflow
    main(aedat_file, csv_file, raw_output_file)


# In[ ]:




