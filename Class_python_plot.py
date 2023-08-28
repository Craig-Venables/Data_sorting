import matplotlib.pyplot as plt
import numpy as np

class plot_python_single_sweep():
    ''' for plotting graphs in python

    current_density_ps = | type: array
    current_density_ng = | type: array
    electric_field_ps = | type: array
    electric_field_ng = | type: array
    current_over_voltage_ps = | type: array
    current_over_voltage_ng = | type: array
    voltage_to_the_half_ps = | type: array
    voltage_to_the_half_ng = | type: array
    '''

    def __init__(self,v_data,c_data, abs_c_data,current_density_ps='', current_density_ng='',
                 electric_field_ps='',electric_field_ng='', current_over_voltage_ps='', current_over_voltage_ng='',
                 voltage_to_the_half_ps='',voltage_to_the_half_ng='', resistance_on_value='',resistance_off_value='',
                 voltage_on_value='',voltage_off_value='', filename='', device_number = '', section_name='',device_name='',
                 polymer_name='',np_materials='',full_path='',
                 on_off_ratio='')-> None:

        # data parsed through from instance class was ran
        self.v_data = v_data
        self.c_data = c_data
        self.abs_c_data = abs_c_data
        self.current_density_ps = current_density_ps
        self.current_density_ng = current_density_ng
        self.electric_field_ps = electric_field_ps
        self.electric_field_ng = electric_field_ng
        self.current_over_voltage_ps = current_over_voltage_ps
        self.current_over_voltage_ng = current_over_voltage_ng
        self.voltage_to_the_half_ps = voltage_to_the_half_ps
        self.voltage_to_the_half_ng = voltage_to_the_half_ng
        self.resistance_on_value = resistance_on_value
        self.resistance_off_value = resistance_off_value
        self.voltage_on_value = voltage_on_value
        self.voltage_off_value = voltage_off_value
        self.on_off_ratio = on_off_ratio
        self.filename = filename
        self.section_name = section_name
        self.device_name = device_name
        self.device_number = device_number
        self.full_path = full_path
        self.polymer_name=polymer_name
        self.np_materials = np_materials
        # fix these names


    def plot(self):
        '''
            plots iv and log iv graphs as subplots in its own window
            '''

        fig = plt.figure(figsize=(15, 6))

        # using the functions plot the graphs
        plt.subplot(1, 2, 1)
        self.plot_iv()

        plt.subplot(1, 2, 2)
        self.plot_logiv()
        plt.ioff()


        # add subplot title
        plt.suptitle(f'{self.polymer_name} -' +f'{self.device_name} -' + ' ' + f'{self.section_name} -' + ' ' + f'{self.filename}')

        # add label underneath plots for on-off ratio
        fig.text(0.5, 0.01, " ON/OFF Ratio @0.2v - " + f'{round(self.on_off_ratio,4)}', ha='center', fontsize=10)
        plt.pause(0.01)
        plt.show(block=False)
        plt.pause(0.01)

    # Functions for plotting the graphs
    def plot_iv(self):
        """
            Plots voltage against current using Matplotlib.

            Parameters:
            - voltage_data (list): List of voltage data points.
            - current_data (list): List of current data points.
            """
        # Calculate the length of the data
        data_len = len(self.v_data)
        # Determine the quarter length
        quarter_len = data_len // 4

        # Create a list of colors for each data point
        colors = []
        labels = []

        for i in range(data_len):
            if i < quarter_len:
                colors.append('r')  # Red for the first quarter
            elif i < 2 * quarter_len:
                colors.append('b')  # Blue for the second quarter
            elif i < 3 * quarter_len:
                colors.append('g')  # Green for the third quarter
            else:
                colors.append('c')  # Cyan for the fourth quarter

        #plt.scatter(self.v_data, self.c_data, c=colors, marker='o')
        # Plot the IV curve with colored points for each quarter
        plt.scatter(self.v_data[:quarter_len], self.c_data[:quarter_len], c='r', marker='o', label='Q1', s=10)
        plt.scatter(self.v_data[quarter_len:2*quarter_len], self.c_data[quarter_len:2*quarter_len], c='b', marker='o', label='Q2',s=10)
        plt.scatter(self.v_data[2*quarter_len:3*quarter_len], self.c_data[2*quarter_len:3*quarter_len], c='g', marker='o', label='Q3',s=10)
        plt.scatter(self.v_data[3*quarter_len:], self.c_data[3*quarter_len:], c='c', marker='o', label='Q4',s=10)

        plt.legend()

        # Add labels and a title
        plt.ylabel('Current')
        plt.xlabel('Voltage')
        plt.title('Voltage vs. Current Graph')

        section_length = len(self.v_data) // 10
        for i in range(10):
            start_idx = i * section_length
            end_idx = (i + 1) * section_length
            plt.arrow(self.v_data[end_idx - 1], self.c_data[end_idx - 1],
                      self.v_data[end_idx] - self.v_data[end_idx - 1],
                      self.c_data[end_idx] - self.c_data[end_idx - 1],
                      width=0.00000001, head_width=0.0000001, head_length=0.01, fc='red', ec='red')
        #length_includes_head = True)
        # Show the plot
        #plt.show()

    def plot_logiv(self):
        """
            Plots voltage against abs current using Matplotlib.

            Parameters:
            - voltage_data (list): List of voltage data points.
            - abs_current_data (list): List of current data points.
            """
        # Create a scatter plot of voltage against current
        plt.plot(self.v_data, self.abs_c_data, color='blue')

        # Add labels and a title
        plt.ylabel('abs Current')
        plt.yscale("log")
        plt.xlabel('Voltage')
        plt.title('Voltage vs. abs_Current Graph' )
        # plt.title('Voltage vs. abs_Current Graph' + \
        #           '\n' + f'{self.device_name}' + ' ' + f'{self.section_name}' + ' ' + f'{self.filename}')

        # Show the plot
        #plt.show()


    def plot_extrema(self):

        #plt.figure(figsize=(8, 6))

        # Calculate the length of the data
        data_len = len(self.v_data)

        # Determine the quarter length
        quarter_len = data_len // 4

        # Create a list of colors for each data point
        colors = []
        labels = []

        for i in range(data_len):
            if i < quarter_len:
                colors.append('r')  # Red for the first quarter
            elif i < 2 * quarter_len:
                colors.append('b')  # Blue for the second quarter
            elif i < 3 * quarter_len:
                colors.append('g')  # Green for the third quarter
            else:
                colors.append('c')  # Cyan for the fourth quarter

        #plt.scatter(self.v_data, self.c_data, c=colors, marker='o')
        # Plot the IV curve with colored points for each quarter
        plt.scatter(self.v_data[:quarter_len], self.c_data[:quarter_len], c='r', marker='o', label='Q1', s=10)
        plt.scatter(self.v_data[quarter_len:2*quarter_len], self.c_data[quarter_len:2*quarter_len], c='b', marker='o', label='Q2',s=10)
        plt.scatter(self.v_data[2*quarter_len:3*quarter_len], self.c_data[2*quarter_len:3*quarter_len], c='g', marker='o', label='Q3',s=10)
        plt.scatter(self.v_data[3*quarter_len:], self.c_data[3*quarter_len:], c='c', marker='o', label='Q4',s=10)

        plt.legend()


        # # Plot the IV curve with colored points for each quarter
        # plt.scatter(self.v_data[:quarter_len], self.c_data[:quarter_len], c='r', marker='o', label='Q1')
        # plt.scatter(self.v_data[quarter_len:2*quarter_len], self.c_data[quarter_len:2*quarter_len], c='b', marker='o', label='Q2')
        # plt.scatter(self.v_data[2*quarter_len:3*quarter_len], self.c_data[2*quarter_len:3*quarter_len], c='g', marker='o', label='Q3')
        # plt.scatter(self.v_data[3*quarter_len:], self.c_data[3*quarter_len:], c='c', marker='o', label='Q4')
        #
        # # Customize labels and title
        # plt.xlabel('Voltage (V)')
        # plt.ylabel('Current (A)')
        # plt.title('IV Curve of Memristor with Quarter-Based Color Mapping')


        # Show the plot
        #plt.grid(True)
        #plt.show()


        # max_voltage, max_voltage_value, max_current, max_current_value, \
        # min_voltage, min_voltage_value, min_current, min_current_value = self.find_extrema()
        #
        # plt.scatter([max_voltage, min_voltage], [max_current, min_current], color='red', marker='o', label='Extrema')
        # plt.xlabel('Voltage')
        # plt.ylabel('Current')
        # plt.title('Extreme Current-Voltage Points')
        # plt.legend()
        #
        # print(f"Max Voltage: {max_voltage}, Associated Current: {max_current_value}")
        # print(f"Min Voltage: {min_voltage}, Associated Current: {min_current_value}")


    # statistics for the whole device
    # def make_hist(self, data_in, x_label, ax):
    #     ax.hist(data_in)
    #     ax.set_xlabel(x_label)
    #     ax.set_ylabel('yes_and_no_sort')
    #     ax.grid()
    #
    # def plot_histograms(self):
    #     fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))
    #
    #     self.make_hist(self.resistance_on_values, 'Ron', axes[0, 0])
    #     self.make_hist(self.resistance_off_values, 'Roff', axes[0, 1])
    #     self.make_hist(self.voltage_off_values, 'Voff', axes[1, 0])
    #     self.make_hist(self.voltage_on_values, 'Von', axes[1, 1])
    #
    #     plt.tight_layout()
    #     plt.show()



    # cpp.plot_python_single_sweep(file_info.v_data, file_info.c_data, file_info.abs_current,
    #                              file_info.current_density_ps, file_info.current_density_ng,
    #                              file_info.electric_field_ps, file_info.electric_field_ng,
    #                              file_info.current_over_voltage_ps, file_info.current_over_voltage_ng,
    #                              file_info.voltage_to_the_half_ps, file_info.voltage_to_the_half_ng,
    #                              file_info.resistance_on_value, file_info.resistance_off_value,
    #                              file_info.voltage_on_value, file_info.voltage_off_value,
    #                              file_info.filename, section_name, device_name, device_number, full_path,
    #                              file_info.on_off_ratio)