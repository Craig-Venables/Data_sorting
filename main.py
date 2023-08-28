import os
import shutil
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import zscore
import Class_device as cd
import Class_single_sweep as css
from Class_Basic_GUI import SimpleGUI
import tkinter as tk
import threading

#C:\Users\Craig-Desktop\Desktop\yes_and_no_sort file fot data sorting\origional data location
directory_path = (r'C:\Users\Craig-Desktop\OneDrive - The University of Nottingham\Documents\Phd\2) Data\1) Devices\1) Memristors')

#output_folder = (r'C:\Users\Craig-Desktop\Desktop\test folder\memristors - projects')




def process_directories(directory_path):
    # List of folder names to skip
    exceptions = ["Exported Graphs png (iv_log)", "Exported Graphs png (Transport)"]

    # Walk through the directory and its subdirectories
    for root, dirs, _ in os.walk(directory_path):
        # Create a copy of the list of directories to avoid modifying it while iterating
        dirs_copy = dirs.copy()
        #print(dirs_copy)
        for d in dirs_copy:
            directory_path = os.path.join(root, d)

            if d in exceptions:
                # Skip processing the exception directory
                dirs.remove(d)
            else:
                dir_contents = os.listdir(directory_path)
                if any(os.path.isfile(os.path.join(directory_path, item)) for item in dir_contents):
                    # Perform your desired action on the directory here
                    #check_for_no_data (directory_path)
                    print(directory_path)

                    # Collects all the device info and data
                    di = cd.Device_info(directory_path)
                    #
                    di.yes_and_no_sort()

                else:
                    # Handle the case where there are no files in the directory
                    print(f"No files found in {directory_path}")
                    continue


process_directories(directory_path)


print ('finished')

