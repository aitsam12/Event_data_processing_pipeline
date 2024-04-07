#!/usr/bin/env python
# coding: utf-8

# ## evt2 to npz

# In[2]:


import subprocess
import os
import numpy as np

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

def convert_raw_to_csv(executable_path, raw_file_path, csv_output_path):
    """
    Run the compiled C++ executable to convert a .raw file to a .csv file.
    """
    command = [executable_path, raw_file_path, csv_output_path]
    subprocess.run(command, check=True)
    print(f"Converted {raw_file_path} to {csv_output_path}")

def convert_csv_to_npz(csv_file_path, npz_file_path):
    """
    Convert a CSV file with columns (x, y, p, t) to an NPZ file.
    """
    # Load data from CSV
    data = np.loadtxt(csv_file_path, delimiter=',', skiprows=1)
    x = data[:, 0]
    y = data[:, 1]
    p = data[:, 2]
    t = data[:, 3]
    
    # Save arrays to NPZ
    np.savez(npz_file_path, x=x, y=y, p=p, t=t)
    print(f"Data saved to {npz_file_path}")

def main(raw_file_path, cpp_project_path, csv_output_path, npz_file_path):
    # Compile the C++ project if needed
    compile_cpp_code(cpp_project_path)

    # Path to the compiled executable
    executable_name = "metavision_evt2_raw_file_decoder"  # Update as necessary
    executable_path = os.path.join(cpp_project_path, "build", executable_name)

    # Convert .raw to .csv using the C++ executable
    convert_raw_to_csv(executable_path, raw_file_path, csv_output_path)
    
    # Convert the resulting CSV to NPZ
    convert_csv_to_npz(csv_output_path, npz_file_path)

    

    

if __name__ == '__main__':
    raw_file_path = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/new/c_camera00000414_240119_163346.raw'
    cpp_project_path = '/home/aitsam/openeb/pipeline/cpp_samples/metavision_evt2_raw_file_decoder'  # Update this path
    csv_output_path = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/new/zzcd_output2.csv'
    npz_file_path = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/new/zzfinal_output.npz'  # Path for the output NPZ file
    
    
    main(raw_file_path, cpp_project_path, csv_output_path, npz_file_path)
    


# In[ ]:




