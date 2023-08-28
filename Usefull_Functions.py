import os


def create_folder_if_not_exists(folder):
    folder_path = os.path.join(folder)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder created: {folder_path}")
    else:
        print(f"Folder already exists: {folder_path}")


def modify_filename(self, original_filename):
    # Customize your filename modification logic here
    # For example, you can add prefixes, suffixes, or change the extension
    modified_filename = f"{self.section_name} - {self.device_number} - " + original_filename
    return modified_filename

