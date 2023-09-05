import os
import Class_device as cd


directory_path = (
    r'C:\Users\Craig-Desktop\OneDrive - The University of Nottingham\Documents\Phd\2) Data\1) Devices\1) Memristors')

def process_directories(directory_path):
    # List of folder names to skip
    exceptions = ["Exported Graphs png (iv_log)", "Exported Graphs png (Transport)"]

    # Walk through the directory and its subdirectories
    for root, dirs, _ in os.walk(directory_path):
        # Create a copy of the list of directories to avoid modifying it while iterating
        dirs_copy = dirs.copy()
        for d in dirs_copy:
            directory_path = os.path.join(root, d)

            if d in exceptions:
                # Skip processing the exception directory
                dirs.remove(d)
            else:
                dir_contents = os.listdir(directory_path)
                print ("Main",dir_contents)
                if any(os.path.isfile(os.path.join(directory_path, item)) for item in dir_contents):
                    # Perform your desired action on the directory here
                    # check_for_no_data (directory_path)
                    print(directory_path)

                    # Calls the class "Class_device" to gain the info from the device
                    di = cd.Device_info(directory_path)
                    # Calls the yes and no sort to sort the data
                    # this also calls the yes_no class and the python plot class
                    di.yes_and_no_sort()
                    #di.pull_info_for_folder()
                    #print(di.v_data_array)

                else:
                    # Handle the case where there are no files in the directory
                    print(f"No files found in {directory_path}")
                    continue


process_directories(directory_path)
print('finished')
