from tkinter import *
import tkinter.messagebox
import visacommands
from procedures import ADTS405

# Global variables
VERSION_NUMBER = "PyCal v1.0.7"
selected_port = ""
selected_address = ""
selected_instrument = ""
connected_instrument = ""


class PyCal:
    def __init__(self, master):
        # Sets root title and min window size
        self.master = master
        master.title(VERSION_NUMBER)
        master.minsize(width=500, height=40)

        # Creates menu
        self.menu = Menu(master)
        master.config(menu=self.menu)

        # Creates file menu
        self.file_subMenu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="File", menu=self.file_subMenu)

        # Creates open procedure submenu
        self.open_procedure_menu = Menu(self.file_subMenu, tearoff=False)
        self.open_procedure_menu.add_command(label="Druck ADTS405", command=self.open_procedure_ADTS405)
        self.file_subMenu.add_cascade(label="Open Procedure", menu=self.open_procedure_menu)

        self.file_subMenu.add_separator()
        self.file_subMenu.add_command(label="Exit", command=master.quit)

        # Creates edit menu
        self.edit_subMenu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="Edit", menu=self.edit_subMenu)

        # Creates help menu
        self.help_submenu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="Help", menu=self.help_submenu)
        self.help_submenu.add_command(label="About", command=self.get_version_number)

        # Select GPIB port
        self.available_ports = list(range(4))
        self.gpib_ports = StringVar(master)
        self.gpib_ports.set("GPIB Port")
        self.gpib_ports_menu = OptionMenu(master, self.gpib_ports, *self.available_ports,
                                          command=self.selected_port)
        self.gpib_ports_menu.config(width=11)
        self.gpib_ports_menu.grid(column=1, row=0, padx=5, pady=5, sticky=W)

        # Select GPIB address
        self.available_addresses = list(range(30))
        self.gpib_addresses = StringVar(master)
        self.gpib_addresses.set("GPIB Address")
        self.gpib_address_menu = OptionMenu(master, self.gpib_addresses, *self.available_addresses,
                                            command=self.selected_address)
        self.gpib_address_menu.config(width=11)
        self.gpib_address_menu.grid(column=2, row=0, padx=5, pady=5, sticky=W)

        # Select Instrument
        self.available_instruments = visacommands.AVAILABLE_INSTRUMENTS
        self.instruments = StringVar(master)
        self.instruments.set("Select Instrument")
        self.instruments = OptionMenu(master, self.instruments, *self.available_instruments,
                                      command=self.selected_instrument)
        self.instruments.config(width=15)
        self.instruments.grid(column=3, row=0, padx=5, pady=5, sticky=W)

        # Lists resources
        self.list_resources_button = Button(master, text="List Resources", command=self.list_resources)
        self.list_resources_button.grid(column=0, row=0, padx=5, pady=5, sticky=W)

        # Connects instrument to instrument
        self.connect_button = Button(master, text="Connect", command=self.address_checker)
        self.connect_button.grid(column=4, row=0, padx=5, pady=5, sticky=W)

    # Checks if instrument is connected at an address
    def address_checker(self):
        self.resources = visacommands.list_resources()
        self.test_address = f"GPIB{selected_port}::{selected_address}::INSTR"
        if self.test_address in self.resources:
            self.connect()
            self.create_window()
        else:
            tkinter.messagebox.showinfo("Error",
                                        f"No instrument connected at address GPIB{selected_port}::{selected_address}.")

    def create_window(self):
        """
        Opens a new window that controls the selected instrument by opening its class
        """
        global selected_instrument
        new_window = Toplevel(self.master)

        # Runs the selected class. Insert new instruments here.
        if selected_instrument == "3478A":
            self.app = NotAvailable(new_window)
        elif selected_instrument == "34401A":
            self.app = Unit34401A(new_window)
        elif selected_instrument == "5520A":
            self.app = Unit5520A(new_window)

    @staticmethod
    def list_resources():
        """
        Prints a list of available instruments to a new window
        """
        instrument_dict = visacommands.unit_identifiers(visacommands.list_resources())
        instrument_list = ""
        for k, v in instrument_dict.items():
            instrument_list += str(k + " --- " + v + '\n')
        tkinter.messagebox.showinfo("Resource List", instrument_list)

    @staticmethod
    def get_version_number():
        """
        Gets current version
        """
        tkinter.messagebox.showinfo("About", VERSION_NUMBER)

    @staticmethod
    def selected_address(value):
        global selected_address
        selected_address = value
        return value

    @staticmethod
    def selected_port(value):
        global selected_port
        selected_port = value
        return value

    @staticmethod
    def selected_instrument(value):
        global selected_instrument
        selected_instrument = value
        return value

    @staticmethod
    def connect():
        global connected_instrument
        connected_instrument = f"GPIB{selected_port}::{selected_address}::INSTR"
        # connected_instrument = "GPIB{0}::{1}::INSTR".format(selected_port_from_list, selected_address_from_list)
        visacommands.open_instrument(connected_instrument)

    # Procedures
    def open_procedure_ADTS405(self):
        new_window = Toplevel(self.master)
        ProcedureADTS405(new_window)


class NotAvailable(Toplevel):
    def __init__(self, master):
        self.master = master
        label = Label(master, text="Not yet available")
        label.pack()


class Unit34401A(Toplevel):
    def __init__(self, master):
        self.master = master
        self.this_instrument = selected_instrument
        master.title(self.this_instrument)

        # Variable to ensure this window is always connected to this instrument
        self.connect_instrument = connected_instrument

        # 34401A Functions list
        self.function_names = ["DC-Volts", "AC-Volts", "DC-Current", "AC-Current", "Continuity",
                               "Resistance-2Wire", "Resistance-4Wire", "Freq", "Period", "Diode"]
        self.function_defs = [self.dcvolts, self.acvolts, self.dccurr, self.accurr, self.continuity,
                              self.twowire, self.fourwire, self.freq, self.period, self.diode]
        self.function_dict = dict(zip(self.function_names, self.function_defs))

        # Code for selecting the 34401A functions from the radio buttons
        self.selected_function = StringVar()
        col = 0
        for func in self.function_names:
            if col <= 4:
                row = 0
            elif col <= 9:
                row = 1
            else:
                row = 2
            options = Radiobutton(master, text=func, width=15,
                                  variable=self.selected_function, value=func,
                                  indicatoron=0, command=self.selector_34401A_function)
            options.grid(row=row, column=col%5)
            col += 1

        # The variable that gets displayed on screen
        self.display_value = StringVar()
        self.display_value.set("")

        #Variables for range and resolution
        self.range = "MAX"
        self.resolution = "MAX"

        # Code for screen display
        display = Label(master, textvariable=self.display_value, font=("Arial", 24),
                        relief="ridge", anchor=E, height=2)
        display.grid(row=2, column=1, columnspan=3, sticky="EW")

    # Opens up selected function pane
    def selector_34401A_function(self):
        """
        Calls selected function
        """
        if self.selected_function.get() in self.function_names:
            self.function_dict[self.selected_function.get()]()

    # 34401A function definitions. All call their respective 34401A functions.
    def dcvolts(self):
        command = f"MEAS:VOLT:DC? {self.range}, {self.resolution}"
        value = visacommands.query(self.connect_instrument, command)
        self.display_value.set(value)

    def acvolts(self):
        command = f"MEAS:VOLT:AC? {self.range}, {self.resolution}"
        value = visacommands.query(self.connect_instrument, command)
        self.display_value.set(value)

    def dccurr(self):
        command = f"MEAS:CURR:DC? {self.range}, {self.resolution}"
        value = visacommands.query(self.connect_instrument, command)
        self.display_value.set(value)

    def accurr(self):
        command = f"MEAS:CURR:AC? {self.range}, {self.resolution}"
        value = visacommands.query(self.connect_instrument, command)
        self.display_value.set(value)

    def continuity(self):
        command = "MEAS:CONT?"
        value = visacommands.query(self.connect_instrument, command)
        self.display_value.set(value)

    def twowire(self):
        command = f"MEAS:RES? {self.range}, {self.resolution}"
        value = visacommands.query(self.connect_instrument, command)
        self.display_value.set(value)

    def fourwire(self):
        command = f"MEAS:FRES? {self.range}, {self.resolution}"
        value = visacommands.query(self.connect_instrument, command)
        self.display_value.set(value)

    def freq(self):
        command = f"MEAS:FREQ? {self.range}, {self.resolution}"
        value = visacommands.query(self.connect_instrument, command)
        self.display_value.set(value)

    def period(self):
        command = f"MEAS:PER? {self.range}, {self.resolution}"
        value = visacommands.query(self.connect_instrument, command)
        self.display_value.set(value)

    def diode(self):
        command = "MEAS:DIOD?"
        value = visacommands.query(self.connect_instrument, command)
        self.display_value.set(value)


class Unit5520A(Toplevel):
    def __init__(self, master):
        self.master = master
        self.this_instrument = selected_instrument
        master.title(self.this_instrument)

        # Instrument Variables
        self.prefix_first_value = " "
        self.prefix_second_value = " "
        self.unit_first_value = " "
        self.unit_second_value = " "
        self.input_value_tracker = "0"

        # Variable to ensure this window is always connected to this instrument
        self.connected_instrument = connected_instrument

        # Button binds
        master.bind("<Return>", self.set_command)   # Enter button
        master.bind("<Prior>", self.multiplier)     # Page up
        master.bind("<Next>", self.divider)         # Page down

        # Enter Button
        self.enter_button = Button(master, text="Enter", width=8,
                                     command=self.set_command)
        self.enter_button.grid(row=1, column=4, padx=5, pady=5)

        # Operate Button
        self.operate_button = Button(master, text="Operate", width=8,
                                     command=lambda: visacommands.write
                                     (self.connected_instrument, "*CLS; OPER;"))
        self.operate_button.grid(row=2, column=4, padx=5, pady=5,)

        # Standby Button
        self.standby_button = Button(master, text="Standby", width=8,
                                     command=lambda: visacommands.write
                                     (self.connected_instrument, "*CLS; STBY;"))
        self.standby_button.grid(row=3, column=4, padx=5, pady=5,)

        # Reset Button
        self.reset_button = Button(master, text="Reset", width=8, command=self.reset)
        self.reset_button.grid(row=4, column=4, padx=5, pady=5)

        # Value boxes
        self.value_title = Label(master, text="Value")
        self.value_title.grid(row=0, column=1)

        self.input_value_1 = DoubleVar()
        self.input_value_1.set(0)
        self.input_value_box1 = Entry(master, text=self.input_value_1, justify=RIGHT, width=15)
        self.input_value_box1.grid(row=1, column=1, columnspan=1, padx=5, pady=5, sticky=W)

        self.input_value_2 = DoubleVar()
        self.input_value_2.set(0)
        self.input_value_box2 = Entry(master, text=self.input_value_2, justify=RIGHT, width=15)
        self.input_value_box2.grid(row=2, column=1, columnspan=1, padx=5, pady=5, sticky=W)

        # Prefix dropdown boxes
        self.prefix_title = Label(master, text="Prefix")
        self.prefix_title.grid(row=0, column=2)

        self.prefix_1 = StringVar(master)
        self.prefix_1.set(" ")
        self.prefix_box1 = OptionMenu(master, self.prefix_1, *visacommands.PREFIX_LIST,
                                      command=self.prefix_first)
        self.prefix_box1.config(width=2)
        self.prefix_box1.grid(row=1, column=2, padx=5, pady=5, sticky=W)

        self.prefix_2 = StringVar(master)
        self.prefix_2.set(" ")
        self.prefix_box2 = OptionMenu(master, self.prefix_2, *visacommands.PREFIX_LIST,
                                      command=self.prefix_second)
        self.prefix_box2.config(width=2)
        self.prefix_box2.grid(row=2, column=2, padx=5, pady=5, sticky=W)

        # Unit dropdown boxes
        self.unit_title = Label(master, text="Unit")
        self.unit_title.grid(row=0, column=3)

        self.unit_1 = StringVar(master)
        self.unit_1.set(" ")
        self.unit_box1 = OptionMenu(master, self.unit_1, *visacommands.UNITS_LIST_1.keys(),
                                    command=self.unit_first)
        self.unit_box1.config(width=3)
        self.unit_box1.grid(row=1, column=3,  padx=5, pady=5, sticky=W)

        self.unit_2 = StringVar(master)
        self.unit_2.set(" ")
        self.unit_box2 = OptionMenu(master, self.unit_2, *visacommands.UNITS_LIST_2.keys(),
                                    command=self.unit_second)
        self.unit_box2.config(width=3)
        self.unit_box2.grid(row=2, column=3, padx=5, pady=5, sticky=W)

        # Multiplier/Divider buttons
        self.multiplier_button = Button(master, text="x10", width=4,
                                        command=self.multiplier)
        self.multiplier_button.grid(row=1, column=0, padx=5, pady=5, sticky=W)

        # Divider button
        self.divider_button = Button(master, text="÷10", width=4,
                                     command=self.divider)
        self.divider_button.grid(row=2, column=0, padx=5, pady=5, sticky=W)

        # Lcomp Button
        self.lcomp_button = Button(master, text="L-Comp", width=8,
                                   command= lambda: visacommands.write(self.connected_instrument, "LCOMP"))
        self.lcomp_button.grid(row=1, column=5, padx=5, pady=5)

        # Resets instrument on startup
        self.reset()

    def set_command(self, event=None):
        """
        Sets the calibrator values
        """
        input_1 = self.input_value_box1.get()
        input_2 = self.input_value_box2.get()

        prefix_1 = self.prefix_first_value
        prefix_2 = self.prefix_second_value

        unit_1 = self.unit_first_value
        unit_2 = self.unit_second_value

        command = f"OUT {input_1}{prefix_1}{unit_1}"
        command_2 = f"{input_2}{prefix_2}{unit_2}"

        # If first value is filled out and the second is empty or hasn't changed
        if not input_1 == 0 and (input_2 == 0 or input_2 == self.input_value_tracker):
            command = f"{command};"
            visacommands.write(self.connected_instrument, command)

        # If both values are filled in and value_2 hasn't changed
        elif not input_1 == 0 and not input_2 == 0:
            command = f"{command},{command_2};"
            visacommands.write(self.connected_instrument, command)

        # Variable to track if input_value_2 has changed
        self.input_value_tracker = self.input_value_box2.get()

    def reset(self):
        """
        Resets the calibrator and sets all values to defaults
        """
        # Resets calibrator
        visacommands.write(self.connected_instrument, "*RST")

        # Resets inputs, prefixes and units
        self.input_value_1.set(0)
        self.input_value_2.set(0)
        self.prefix_1.set(" ")
        self.prefix_2.set(" ")
        self.unit_1.set(" ")
        self.unit_2.set(" ")

    def multiplier(self, event=None):
        """
        Used for the multiplier button. Multiplies the input value by 10.
        Disabled for current.
        """
        if not self.unit_first_value == "A":
            value = self.input_value_1.get()
            value *= 10
            self.input_value_1.set(value)

    def divider(self, event=None):
        """
        Used for the divider button. Dividers the input value by 10.
        Disabled for current.
        """
        if not self.unit_first_value == "A":
            value = self.input_value_1.get()
            value /= 10
            self.input_value_1.set(value)

    # Input and dro down menu functions

    def prefix_first(self, value):
        self.prefix_first_value = visacommands.PREFIX_LIST[value]
        return value

    def prefix_second(self, value):
        self.prefix_second_value = visacommands.PREFIX_LIST[value]
        return value

    def unit_first(self, value):
        self.unit_first_value = visacommands.UNITS_LIST_1[value]
        return value

    def unit_second(self, value):
        self.unit_second_value = visacommands.UNITS_LIST_2[value]
        return value


class ProcedureADTS405(Toplevel):
    def __init__(self, master):
        self.master = master
        master.title("ADTS405")

        # Select GPIB port
        self.available_ports = list(range(4))
        self.gpib_ports = StringVar(master)
        self.gpib_ports.set("GPIB Port")
        self.gpib_ports_menu = OptionMenu(master, self.gpib_ports, *self.available_ports)
        self.gpib_ports_menu.config(width=11)
        self.gpib_ports_menu.grid(column=1, row=1, padx=5, pady=5, sticky=W)

        # Select GPIB address
        self.available_addresses = list(range(30))
        self.gpib_addresses = StringVar(master)
        self.gpib_addresses.set("GPIB Address")
        self.gpib_address_menu = OptionMenu(master, self.gpib_addresses, *self.available_addresses, command=self.test)
        self.gpib_address_menu.config(width=11)
        self.gpib_address_menu.grid(column=2, row=1, padx=5, pady=5, sticky=W)







# Runs the main root display
if __name__ == "__main__":
    root = Tk()
    pycal = PyCal(root)
    root.mainloop()
