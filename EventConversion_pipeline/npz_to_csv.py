#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import csv

def convert_npz_to_csv(npz_file_path, csv_file_path):
    """
    Convert an NPZ file back to a CSV file with columns (x, y, p, t), without column names in the first row.

    Parameters:
    - npz_file_path: Path to the input NPZ file.
    - csv_file_path: Path for the output CSV file.
    """
    # Load data from NPZ
    data = np.load(npz_file_path)
    x = data['x']
    y = data['y']
    p = data['p']
    t = data['t']
    
    # Combine arrays into one structured array
    combined_data = np.column_stack((x, y, p, t))
    
    # Write data to CSV
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        
        # Write the data rows
        writer.writerows(combined_data)

    print(f"Data saved to {csv_file_path}")

if __name__ == '__main__':
    # Update these paths according to your files' locations
    npz_file_path = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/new/camera__clalp.npz'
    csv_file_path = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/new/camera__clalp_re.csv'

    convert_npz_to_csv(npz_file_path, csv_file_path)


# In[ ]:




