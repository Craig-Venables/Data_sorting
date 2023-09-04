import Class_single_sweep as css
import os
import Class_yes_no as cyn
import Class_python_plot as cpp

ignore_files = ('.dll', '.sys', '.bat', '.cmd', '.msi', '.reg', '.ppt', '.pptx', '.mp3',
                '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a', '.mp4', '.avi', '.mkv',
                '.mov', '.wmv', '.flv', '.webm', '.zip', '.rar', '.7z', '.tar', '.gz',
                '.bz2', '.xz', '.html', '.htm', '.css', '.js', '.php', '.asp', '.jsp',
                '.json', '.xml', '.yaml', '.yml', '.toml', '.psd', '.ai', '.eps', '.indd',
                '.ico', '.cur', '.ani', '.opju', '.Wdf', '.ogwu', '.exe', '.ini', '.opju',
                '.Wdf', '.exe', '.jpg', '.png', '.csv', '.pdf', '.doc', '.docx')

exceptions = ["Exported Graphs png (iv_log)", "Exported Graphs png (Transport)"]


def get_file_names(directory_path):
    ''' extract all the names of devices from the filepath given'''
    # Extract folder names from the full path
    folder_names = os.path.dirname(directory_path)
    # extract parent folder name i.e section name
    parent_folder_name = os.path.basename(os.path.dirname(directory_path))
    device_number = parent_folder_name
    # extract grandparent folder name i.e device name
    grandparent_folder_name = os.path.basename(os.path.dirname(os.path.dirname(directory_path)))
    section_name = grandparent_folder_name
    # extract great-grandparent name ie polymer
    great_grandparent_folder_name = os.path.basename(
        os.path.dirname(os.path.dirname(os.path.dirname(directory_path))))
    device_name = great_grandparent_folder_name
    great_great_grandparent_folder_name = os.path.basename(os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(directory_path)))))
    polymer_name = great_great_grandparent_folder_name
    great_great_great_grandparent_folder_name = os.path.basename(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(directory_path))))))
    np_material_or_stock = great_great_great_grandparent_folder_name


class Device_info():
    ''' calculate statistics on the device

    this takes all the data of the single device from each of the data sweeps and stores it in an array for use later.

    device_file_path = filepath for the device folder | type: str

    :returns
        all device information
    '''

    def __init__(self, device_file_path="", ) -> None:

        # give just filepath to the class, and it should do everything inside this class
        self.directory_path = device_file_path
        print(device_file_path)

        # empty arrays for later use, these will store all the data from each of the weeps for use later
        # this is all the info gained from the device
        self.resistance_on_values = []
        self.resistance_off_values = []
        self.voltage_on_values = []
        self.voltage_off_values = []
        self.resistance_arrays = []
        self.log_resistance_arrays = []
        self.times_arrays = []
        self.v_data_array = []
        self.c_data_array = []
        self.abs_c_data_array = []
        self.current_density_ps_arrays = []
        self.current_density_ng_arrays = []
        self.electric_field_ps_arrays = []
        self.electric_field_ng_arrays = []
        self.current_over_voltage_ps_arrays = []
        self.current_over_voltage_ng_arrays = []
        self.voltage_to_the_half_ps_arrays = []
        self.voltage_to_the_half_ng_arrays = []
        self.on_off_ratio_arrays = []

        # filenames
        self.file_names = []
        self.device_number = []
        self.sections = []
        self.devices = []
        self.file_paths = []
        self.polymer = []
        self.np_material_or_stock = []
        self.full_path = []

        # give a list of files in device directory

        self.file_list = os.listdir(self.directory_path)

    def yes_and_no_sort(self):

        for filename in self.file_list:
            print("Processing:", filename)
            try:
                if not any(filename.endswith(ext) for ext in ignore_files):
                    if os.path.isfile(os.path.join(self.directory_path, filename)):
                        if check_for_no_data(os.path.join(self.directory_path, filename)) is None:
                            print(f"{filename} device has no data")
                            print("")

                            # self.get_file_names(self.directory_path)

                            # Extract folder names from the full path
                            folder_names = os.path.dirname(self.directory_path)
                            # extract parent folder name i.e section name
                            parent_folder_name = os.path.basename(os.path.dirname(self.directory_path))
                            device_number = parent_folder_name
                            # extract grandparent folder name i.e device name
                            grandparent_folder_name = os.path.basename(
                                os.path.dirname(os.path.dirname(self.directory_path)))
                            section_name = grandparent_folder_name
                            # extract great-grandparent name ie polymer
                            great_grandparent_folder_name = os.path.basename(
                                os.path.dirname(os.path.dirname(os.path.dirname(self.directory_path))))
                            device_name = great_grandparent_folder_name
                            great_great_grandparent_folder_name = os.path.basename(os.path.dirname(
                                os.path.dirname(os.path.dirname(os.path.dirname(self.directory_path)))))
                            polymer_name = great_great_grandparent_folder_name
                            great_great_great_grandparent_folder_name = os.path.basename(
                                os.path.dirname(os.path.dirname(
                                    os.path.dirname(os.path.dirname(os.path.dirname(self.directory_path))))))
                            np_material_or_stock = great_great_great_grandparent_folder_name

                            cyn.yes_no(1000, filename=filename, device_number=device_number, section_name=section_name,
                                       device_name=device_name, polymer_name=polymer_name,
                                       np_material_or_stock=np_material_or_stock, full_path=self.directory_path)

                        # for normal devices with data
                        v_data, c_data, abs_c_data, current_density_ps, current_density_ng, \
                            electric_field_ps, electric_field_ng, current_over_voltage_ps, \
                            current_over_voltage_ng, voltage_to_the_half_ps, voltage_to_the_half_ng, \
                            resistance_on_value, resistance_off_value, voltage_on_value, voltage_off_value, resistance, \
                            log_resistance, times, on_off_ratio, filename, device_number, section_name, device_name, \
                            polymer_name, np_material_or_stock, full_path, save_data = self.pull_into_for_single_sweep(
                            filename)


                        cyn.yes_no(v_data, c_data, abs_c_data, resistance_on_value, resistance_off_value,
                                   voltage_on_value, voltage_off_value, resistance, log_resistance, times,
                                   on_off_ratio, filename, device_number, section_name, device_name, polymer_name,
                                   np_material_or_stock, full_path, save_data)

            except Exception as e:
                print("it broke")
                print(f"Error processing {filename}: {e}")

    def pull_info_for_folder(self, filename):
        for filename in self.file_list:

            if not filename.endswith(ignore_files):
                if os.path.isfile(os.path.join(self.directory_path, filename)):
                    # join file names with directory string
                    full_path = os.path.join(self.directory_path, filename)

                    # Extract folder names from the full path
                    folder_names = os.path.dirname(full_path)
                    # extract parent folder name i.e section name
                    parent_folder_name = os.path.basename(os.path.dirname(full_path))
                    device_number = parent_folder_name
                    # extract grandparent folder name i.e device name
                    grandparent_folder_name = os.path.basename(os.path.dirname(os.path.dirname(full_path)))
                    section_name = grandparent_folder_name
                    # extract great-grandparent name ie polymer
                    great_grandparent_folder_name = os.path.basename(
                        os.path.dirname(os.path.dirname(os.path.dirname(full_path))))
                    device_name = great_grandparent_folder_name
                    great_great_grandparent_folder_name = os.path.basename(os.path.dirname(
                        os.path.dirname(os.path.dirname(os.path.dirname(full_path)))))
                    polymer_name = great_great_grandparent_folder_name
                    great_great_great_grandparent_folder_name = os.path.basename(os.path.dirname(os.path.dirname(
                        os.path.dirname(os.path.dirname(os.path.dirname(full_path))))))
                    np_material_or_stock = great_great_great_grandparent_folder_name

                    self.file_names.append(filename)
                    self.device_number.append(device_number)
                    self.sections.append(section_name)
                    self.devices.append(device_name)

                    self.full_path.append(full_path)
                    self.polymer.append(polymer_name)
                    self.np_material_or_stock.append(np_material_or_stock)
                    # calls the class single sweep info
                    file_info = css.Single_sweep_info(full_path, filename)

                    # parses all the needed information from the single_sweep_info class putting them into arrays for use later
                    # current voltage data
                    self.v_data_array.append(file_info.v_data)
                    self.c_data_array.append(file_info.c_data)
                    self.abs_c_data_array.append(file_info.abs_current)

                    # transport data
                    self.current_density_ps_arrays.append(file_info.current_density_ps)
                    self.current_density_ng_arrays.append(file_info.current_density_ng)
                    self.electric_field_ps_arrays.append(file_info.electric_field_ps)
                    self.electric_field_ng_arrays.append(file_info.electric_field_ng)
                    self.current_over_voltage_ps_arrays.append(file_info.current_over_voltage_ps)
                    self.current_over_voltage_ng_arrays.append(file_info.current_over_voltage_ng)
                    self.voltage_to_the_half_ps_arrays.append(file_info.voltage_to_the_half_ps)
                    self.voltage_to_the_half_ng_arrays.append(file_info.voltage_to_the_half_ng)

                    self.resistance_on_values.append(file_info.resistance_on_value)
                    self.resistance_off_values.append(file_info.resistance_off_value)
                    self.voltage_on_values.append(file_info.voltage_on_value)
                    self.voltage_off_values.append(file_info.voltage_off_value)

                    self.resistance_arrays.append(file_info.resistance)
                    self.log_resistance_arrays.append(file_info.log_resistance)
                    self.times_arrays.append(file_info.time)
                    self.on_off_ratio_arrays.append(file_info.on_off_ratio)

    def pull_into_for_single_sweep(self, filename):

        full_path = os.path.join(self.directory_path, filename)

        # Extract folder names from the full path
        folder_names = os.path.dirname(full_path)
        # extract parent folder name i.e section name
        parent_folder_name = os.path.basename(os.path.dirname(full_path))
        device_number = parent_folder_name
        # extract grandparent folder name i.e device name
        grandparent_folder_name = os.path.basename(os.path.dirname(os.path.dirname(full_path)))
        section_name = grandparent_folder_name
        # extract great-grandparent name ie polymer
        great_grandparent_folder_name = os.path.basename(
            os.path.dirname(os.path.dirname(os.path.dirname(full_path))))
        device_name = great_grandparent_folder_name
        great_great_grandparent_folder_name = os.path.basename(os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(full_path)))))
        polymer_name = great_great_grandparent_folder_name
        great_great_great_grandparent_folder_name = os.path.basename(os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(full_path))))))
        material_or_stock = great_great_great_grandparent_folder_name

        # calls the class single sweep info
        file_info = css.Single_sweep_info(full_path, filename)
        # parses all the needed information from the single_sweep_info class putting them into arrays for use later
        # current voltage data
        v_data = file_info.v_data
        c_data = file_info.c_data

        abs_c_data = file_info.abs_current
        # transport data
        current_density_ps = file_info.current_density_ps
        current_density_ng = file_info.current_density_ng
        electric_field_ps = file_info.electric_field_ps
        electric_field_ng = file_info.electric_field_ng
        current_over_voltage_ps = file_info.current_over_voltage_ps
        current_over_voltage_ng = file_info.current_over_voltage_ng
        voltage_to_the_half_ps = file_info.voltage_to_the_half_ps
        voltage_to_the_half_ng = file_info.voltage_to_the_half_ng

        resistance_on = file_info.resistance_on_value
        resistance_off = file_info.resistance_off_value
        voltage_on = file_info.voltage_on_value
        voltage_off = file_info.voltage_off_value

        resistance = file_info.resistance
        log_resistance = file_info.log_resistance
        times = file_info.time
        on_off_ratio = file_info.on_off_ratio

        save_data = file_info.save_data()

        return (v_data, c_data, abs_c_data, current_density_ps, current_density_ng,
                electric_field_ps, electric_field_ng, current_over_voltage_ps, current_over_voltage_ng
                , voltage_to_the_half_ps, voltage_to_the_half_ng, resistance_on, resistance_off,
                voltage_on, voltage_off, resistance, log_resistance, times, on_off_ratio, filename, device_number,
                section_name, device_name, polymer_name, material_or_stock, full_path, save_data)


def check_for_no_data(filepath):
    # print(f"{filepath_for_single_sweep}")
    with open(filepath, "r") as f:  # open the file as read only
        fread = f.readlines()
        fread.pop(0)
    # B = self.filereader()
    # B = fm.directory(self.filepath_for_single_sweep).filereader()
    Data = []
    for i, line in enumerate(fread):
        C = (line.split('\t'))
        D = []
        for value in C:
            if value != '':
                D.append(float(value))
        Data.append(D)
    v_data_array = []
    c_data_array = []
    for value in Data:
        if value:
            v_data_array.append(value[0])
            c_data_array.append(value[1])
    if len(v_data_array) == 0 or len(v_data_array) < 10:
        print('not enough data', filepath)
        return None
    return v_data_array, c_data_array
