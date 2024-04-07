#!/usr/bin/env python
# coding: utf-8

# ## csv to evt2

# In[2]:


import subprocess
import os

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


def convert_csv_to_raw(cpp_project_path, csv_file_path, raw_output_path):
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
    cpp_project_path = '/home/aitsam/openeb/pipeline/cpp_samples/metavision_evt2_raw_file_encoder'  # Update this path
    csv_file_path = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/new/camera__clalp.csv'  # Update this path
    raw_output_path = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/new/camera__clalp.raw'  # Update this path

    convert_csv_to_raw(cpp_project_path, csv_file_path, raw_output_path)



# In[ ]:




