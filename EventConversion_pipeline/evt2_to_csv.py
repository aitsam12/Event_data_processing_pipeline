#!/usr/bin/env python
# coding: utf-8

# ## EVT2 to csv

# In[1]:


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

        
def convert_raw_to_csv(executable_path, raw_file_path, csv_output_path):
    """
    Run the compiled C++ executable to convert a .raw file to a .csv file.
    """
    command = [executable_path, raw_file_path, csv_output_path]
    subprocess.run(command, check=True)
    print(f"Converted {raw_file_path} to {csv_output_path}")

    
    
def main(raw_file_path, cpp_project_path, csv_output_path):
    # Compile the C++ project if needed
    compile_cpp_code(cpp_project_path)

    # Path to the compiled executable
    executable_name = "metavision_evt2_raw_file_decoder"  # Update as necessary
    executable_path = os.path.join(cpp_project_path, "build", executable_name)

    # Convert .raw to .csv using the C++ executable
    convert_raw_to_csv(executable_path, raw_file_path, csv_output_path)

if __name__ == '__main__':
    raw_file_path = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/new/c_camera00000414_240119_163346.raw'
    cpp_project_path = '/home/aitsam/openeb/pipeline/cpp_samples/metavision_evt2_raw_file_decoder'  # Update this path
    csv_output_path = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/new/cd_output.csv'
    
    main(raw_file_path, cpp_project_path, csv_output_path)


# In[ ]:




