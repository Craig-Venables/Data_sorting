import numpy as np
import matplotlib.pyplot as plt


def absolute_val(col):
    return [abs(x) for x in col]


class Single_sweep_info:
    """
    Class for all functions for data manipulation file reading and equations, this class
    calculates all the necessary arrays of equations for use later

    filepath_for_single_sweep = Filepath of file used | type: str
    filename = filename currently under use | type: str
    distance = Distance between electrodes default 100E-9 | type: int
    area = Area between electrodes default 100E-6 | type: int

    This class outputs:

    current_density_ps = | type: array
    current_density_ng = | type: array
    electric_field_ps = | type: array
    electric_field_ng = | type: array
    current_over_voltage_ps = | type: array
    current_over_voltage_ng = | type: array
    voltage_to_the_half_ps = | type: array
    voltage_to_the_half_ng = | type: array
    resistance = | type: array
    log_resistance = | type: array
    time = | type: array
    resistance_on_value = single value output | type: val
    resistance_off_value = single value output | type: val
    voltage_on_value = single value output | type: val
    voltage_off_value = single value output | type: val


    """

    # This class represents all the functions used for sorting the data.
    def __init__(self, filepath_for_single_sweep="", filename="", distance=100E-9, area=100E-6) -> None:

        # defining the initial names within the class
        self.distance = distance
        self.area = area
        self.filepath = filepath_for_single_sweep
        self.filename = filename

        # split the data and calculate all needed arrays of voltages and currents

        self.v_data, self.c_data = self.split_iv_sweep()

        self.v_data_ps, self.c_data_ps = self.filter_positive_values()
        self.v_data_ng, self.c_data_ng = self.filter_negative_values()

        # calculate all equations needed

        self.current_density_ps = self.current_density_eq(self.v_data_ps, self.c_data_ps)
        self.current_density_ng = self.current_density_eq(self.v_data_ng, self.c_data_ng)
        self.electric_field_ps = self.electric_field_eq(self.v_data_ps)
        self.electric_field_ng = self.electric_field_eq(self.v_data_ng)
        self.current_over_voltage_ps = self.current_over_voltage_eq(self.v_data_ps, self.c_data_ps)
        self.current_over_voltage_ng = self.current_over_voltage_eq(self.v_data_ng, self.c_data_ng)
        self.voltage_to_the_half_ps = self.voltage_to_the_half_eq(self.v_data_ps)
        self.voltage_to_the_half_ng = self.voltage_to_the_half_eq(self.v_data_ng)
        self.resistance = self.resistance()
        self.log_resistance = self.log_resistance()
        self.abs_current = absolute_val(self.c_data)

        # self.yes_and_no_sort()

        # makes a time array that is evenly spread out for the data, from t=0 to t=length of your experiment
        self.time = np.linspace(0, 33, len(self.v_data))

        # for statistics on the device
        self.resistance_on_value, self.resistance_off_value, self.voltage_on_value, self.voltage_off_value = self.statistics()

        # checks for divide by zero error!
        self.on_off_ratio = self.weird_division(self.resistance_off_value, self.resistance_on_value)

        # data for saving in a text file for later use
        self.save_data()

        # print (self.on_off_ratio)

    def weird_division(self, n, d):
        return n / d if d else 0

    def save_data(self):
        data = list(zip(self.v_data, self.c_data, self.abs_current, self.resistance, self.log_resistance,
                        self.current_density_ps, self.current_density_ng, self.electric_field_ps,
                        self.electric_field_ng, self.current_over_voltage_ps, self.current_over_voltage_ng,
                        self.voltage_to_the_half_ps,
                        self.voltage_to_the_half_ng))
        header = "voltage", "current", "abs_current", "resistance", "log_resistance", "abs_current", "current_density_ps" \
            , "current_density_ng", "electric_field_ps", "electric_field_ng", "current_over_voltage_ps", \
            "current_over_voltage_ng", "voltage_to_the_half_ps", "voltage_to_the_half_ng"
        formatted_data = ""

        # Set the column width for formatting
        column_width = 15

        # Set the number of significant figures to round to
        significant_figures = 4

        # Format the header row with adjusted column width
        formatted_header = "\t".join(item.ljust(column_width) for item in header)
        formatted_data += formatted_header + "\n"

        # Iterate through each row and format the data

        for row in data:
            rounded_row = [round(item, significant_figures) for item in row]
            formatted_row = "\t".join(str(item).ljust(column_width) for item in rounded_row)
            formatted_data += formatted_row + "\n"

            # self.save_data = formatted_data
        return formatted_data

    def filereader(self):
        with open(self.filepath, "r") as f:  # open the file as read only
            fread = f.readlines()
            fread.pop(0)
            return fread

    def split_iv_sweep(self):
        # print(f"{filepath_for_single_sweep}")
        B = self.filereader()
        # B = fm.directory(self.filepath_for_single_sweep).filereader()
        Data = []
        for i, line in enumerate(B):
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
        # if len(v_data_array) == 0:
        #     return "error no data"
        return v_data_array, c_data_array

    # calculating the positive and negative values for a given array of voltage and current data
    def filter_positive_values(self):
        ''' Takes the data given too it within the class (current and voltage arrays)
        and returns only the positive values in place of zeros if they are negative '''
        result_voltage_ps = []
        result_current_ps = []

        for v, c in zip(self.v_data, self.c_data):
            if v >= 0:
                result_voltage_ps.append(v)
                result_current_ps.append(c)
            else:
                result_voltage_ps.append(0)
                result_current_ps.append(0)

        return result_voltage_ps, result_current_ps

    def filter_negative_values(self):
        ''' Takes the data given too it within the class (current and voltage arrays)
        and returns only the negative values in place of zeros if they are positive
        takes arrays '''
        result_voltage_ng = []
        result_current_ng = []
        for v, c in zip(self.v_data, self.c_data):
            if v <= 0:
                result_voltage_ng.append(v)
                result_current_ng.append(c)
            else:
                result_voltage_ng.append(0)
                result_current_ng.append(0)

        return absolute_val(result_voltage_ng), absolute_val(result_current_ng)

    def zero_devision_check(self, x, y):
        try:
            return x / y
        except ZeroDivisionError:
            return 0

    # equations for all data within this class

    def resistance(self):
        resistance = []
        for i in range(len(self.v_data)):
            resistance.append(self.zero_devision_check(self.v_data[i], self.c_data[i]))
        return resistance

    # there is an error ocurring here C:\Users\Craig-Desktop\PycharmProjects\new yes_and_no_sort\Class_single_sweep.py:157: RuntimeWarning: invalid value encountered in log
    # result = np.log(self.resistance[i]) im unsure why

    def log_resistance(self):
        log_resistance = []
        for i in range(len(self.resistance)):
            # checks for 0 value and if there is a zero value it returns 0 instead of loging it
            if self.resistance[i] != 0:
                result = np.log(self.resistance[i])
                log_resistance.append(result)
            else:
                result = 0  # or any other suitable value
                log_resistance.append(result)
        return log_resistance

    def current_density_eq(self, v_data, c_data):
        current_density = []
        for voltage, current in zip(v_data, c_data):
            if voltage == 0 or current == 0:
                current_density.append(0)
                # for checking for divide by zero error
                continue
            new_num = (self.distance / ((voltage / current) * self.area ** 2)) * (voltage / self.distance)
            current_density.append(new_num)
        return current_density

    def electric_field_eq(self, v_data):
        electric_field = []
        for voltage in v_data:
            if voltage == 0:
                electric_field.append(0)
                continue
            new_num = voltage / self.distance
            electric_field.append(new_num)
        return electric_field

    def current_over_voltage_eq(self, v_data, c_data):
        # v_data & c_data cant be refered to as self as this needs
        # positive or negative values only
        current_over_voltage = []
        for voltage, current in zip(v_data, c_data):
            if voltage == 0 or current == 0:
                current_over_voltage.append(0)
                # for checking for divide by zero error
                continue
            new_num = current / voltage
            current_over_voltage.append(new_num)
        return current_over_voltage

    def voltage_to_the_half_eq(self, v_data):
        voltage_to_the_half = []
        for voltage in v_data:
            new_num = voltage ** 1 / 2
            voltage_to_the_half.append(new_num)
        return voltage_to_the_half

    # Statistics for file

    def statistics(self):
        """
        calculates r on off and v on off values for an individual device
        """
        resistance_on_value = []
        resistance_off_value = []
        voltage_on_value = []
        voltage_off_value = []
        # if this breaks maybe add max v / x number
        thresh = 0.2

        # voltage and current magnitude
        voltage_mag = []
        current_mag = []
        if not len(self.v_data) < 10:
            for value in range(len(self.v_data)):
                if -thresh < self.v_data[value] < thresh:
                    voltage_mag.append(self.v_data[value])
                    current_mag.append(self.c_data[value])

            res_mag = []  # same here but for the resistances
            for j in range(len(voltage_mag)):
                if voltage_mag[j] != 0:
                    res_mag.append(voltage_mag[j] / current_mag[j])


            if not len(self.v_data) < 10:
                roff = min(res_mag)
                ron = max(res_mag)
            else:
                roff = 0
                ron = 0


            resistance_off_value = roff
            resistance_on_value = ron

            grads = []
            for j in range(len(self.v_data)):
                if j != len(self.v_data) - 1:
                    if self.v_data[j + 1] - self.v_data[j] != 0:
                        grads.append((self.c_data[j + 1] - self.c_data[j]) / (self.v_data[
                                                                                  j + 1] - self.v_data[j]))

            max_grad = max(grads[:(int(len(grads) / 2))])
            min_grad = min(grads)

            for j in range(len(grads)):
                if grads[j] == max_grad:
                    voltage_off = self.v_data[j]
                if grads[j] == min_grad:
                    voltage_on = self.v_data[j]

            voltage_on_value = voltage_on
            voltage_off_value = voltage_off
        else:
            return 0, 0, 0, 0

        # print (resistance_on_value, resistance_off_value, voltage_on_value , voltage_off_value)
        return resistance_on_value, resistance_off_value, voltage_on_value, voltage_off_value
