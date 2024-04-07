#!/usr/bin/env python
# coding: utf-8

# ## EVT3 to avi

# In[2]:


import subprocess
import os

def convert_raw_to_avi(raw_file_path, conversion_script_path):
    """
    Convert a specified .raw file to an .avi file using a conversion script.
    
    Parameters:
    - raw_file_path: Path to the input .raw file.
    - conversion_script_path: Path to the conversion script.
    """
    # Check if the file ends with .raw
    if raw_file_path.endswith(".raw"):
        # Construct the output AVI file path
        avi_file_path = os.path.splitext(raw_file_path)[0] + ".avi"

        # Construct the command to run the conversion script
        command = f"python3 {conversion_script_path} -i {raw_file_path} -o {avi_file_path}"

        # Execute the command using subprocess
        subprocess.run(command, shell=True)
        print(f"Converted {raw_file_path} to {avi_file_path}")
    else:
        print(f"The file {raw_file_path} does not end with .raw")

# Specify the path to the .raw file and conversion script
raw_file_path = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/new/normal_clap2.raw'  # Update this path
conversion_script_path = "/home/aitsam/openeb/metavision_all/metavision/designer/core/samples/python/raw_to_video.py"

# Call the function to convert the specified raw file to AVI
convert_raw_to_avi(raw_file_path, conversion_script_path)


# In[ ]:




