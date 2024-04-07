#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import csv
import subprocess
import os

def convert_npz_to_csv(npz_file_path, csv_file_path):
    """
    Convert an NPZ file to a CSV file without column names in the first row.
    """
    data = np.load(npz_file_path)
    x = data['x']
    y = data['y']
    p = data['p']
    t = data['t']
    
    combined_data = np.column_stack((x, y, p, t))
    
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(combined_data)

    print(f"Data saved to {csv_file_path}")

def compile_cpp_code(cpp_project_path):
    """
    Compile C++ project if needed.
    """
    build_path = os.path.join(cpp_project_path, 'build')
    
    if not os.path.exists(build_path):
        print(f"Compiling C++ project at {cpp_project_path}...")
        os.makedirs(build_path, exist_ok=True)
        os.chdir(build_path)
        subprocess.run(['cmake', '..', '-DCMAKE_BUILD_TYPE=Release'], check=True)
        subprocess.run(['cmake', '--build', '.', '--config', 'Release'], check=True)
    else:
        print("Build directory exists. Skipping compilation.")

def convert_csv_to_raw(cpp_project_path, csv_file_path, raw_output_path):
    """
    Convert a CSV file to a .raw file using a compiled C++ executable.
    """
    compile_cpp_code(cpp_project_path)
    executable_path = os.path.join(cpp_project_path, 'build', 'metavision_evt2_raw_file_encoder')
    command = [executable_path, raw_output_path, csv_file_path]
    subprocess.run(command, check=True)
    print(f"Converted {csv_file_path} to {raw_output_path}")

if __name__ == '__main__':
    # Update these paths according to your files' locations
    npz_file_path = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/new/camera__clalp.npz'
    intermediate_csv_file_path = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/new/camera__clalp_re.csv'
    raw_output_path = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/new/camera__clalp.raw'
    cpp_project_path = '/home/aitsam/openeb/pipeline/cpp_samples/metavision_evt3_raw_file_encoder'

    # Convert NPZ to CSV
    convert_npz_to_csv(npz_file_path, intermediate_csv_file_path)
    
    # Convert CSV to RAW
    convert_csv_to_raw(cpp_project_path, intermediate_csv_file_path, raw_output_path)


# In[ ]:




