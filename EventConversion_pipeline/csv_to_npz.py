#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np

def convert_csv_to_npz(csv_file_path, npz_file_path):
    """
    Convert a CSV file with columns (x, y, p, t) to an NPZ file.

    Parameters:
    - csv_file_path: Path to the input CSV file.
    - npz_file_path: Path for the output NPZ file.
    """
    # Load data from CSV
    data = np.loadtxt(csv_file_path, delimiter=',', skiprows=1)  # Adjust skiprows if your CSV has a header

    # Assuming the CSV columns are ordered as x, y, p, t
    x = data[:, 0]
    y = data[:, 1]
    p = data[:, 2]
    t = data[:, 3]
    
    # Save arrays to NPZ
    np.savez(npz_file_path, x=x, y=y, p=p, t=t)
    print(f"Data saved to {npz_file_path}")

if __name__ == '__main__':
    # Update these paths according to your files' locations
    csv_file_path = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/new/camera__clalp.csv'
    npz_file_path = '/media/aitsam/46F516C5276E2490/DATASETS_pipeline/DVSgesture/extract/checking/new/camera__clalp.npz'

    convert_csv_to_npz(csv_file_path, npz_file_path)


# In[ ]:




