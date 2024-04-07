#!/usr/bin/env python
# coding: utf-8

# ## compiling c++ script with python

# In[11]:


import subprocess
import os

def compile_cpp_code(cpp_project_path):
    # Change the current working directory to the C++ project path
    os.chdir(cpp_project_path)

    # Create and enter the build directory
    build_path = os.path.join(cpp_project_path, 'build')
    os.makedirs(build_path, exist_ok=True)
    os.chdir(build_path)

    # Run CMake commands
    subprocess.run(['cmake', '..', '-DCMAKE_BUILD_TYPE=Release'], check=True)
    subprocess.run(['cmake', '--build', '.', '--config', 'Release'], check=True)

def main():
    # Path to your C++ projects
    cpp_project_paths = ['/cpp_samples/metavision_evt2_raw_file_encoder']

    # Compile each C++ project
    for path in cpp_project_paths:
        compile_cpp_code(path)

if __name__ == '__main__':
    main()


# In[ ]:




