#!/usr/bin/env python
# coding: utf-8

# ## EVT3 to H5

# In[2]:


import subprocess
import os

def convert_raw_to_h5(raw_file_path, generate_h5_script):
    """
    Convert a specified .raw file to an .h5 file using a given script.
    
    Parameters:
    - raw_file_path: Path to the input .raw file.
    - generate_h5_script: Path to the script that generates the .h5 file.
    """
    # Ensure the file ends with .raw
    if raw_file_path.endswith(".raw"):
        # Determine the output folder from the raw file path
        output_folder = os.path.dirname(raw_file_path)

        # Construct the command to generate the .h5 file
        command = f"python3 {generate_h5_script} {raw_file_path} -o {output_folder}"

        # Execute the command using subprocess
        subprocess.run(command, shell=True)
        print(f"Generated .h5 file for {raw_file_path}")
    else:
        print(f"The file {raw_file_path} is not a .raw file")

# Define the path to your .raw file and the script for generating .h5 files
raw_file_path = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/new/normal_clap2.raw'  # Update this with the actual path to your .raw file
generate_h5_script = "/home/aitsam/openeb/metavision_all/metavision/sdk/ml/python_samples/generate_hdf5/generate_hdf5.py"  # Update this with the actual path to the script

# Call the function to convert the specified raw file to .h5
convert_raw_to_h5(raw_file_path, generate_h5_script)


# In[ ]:




