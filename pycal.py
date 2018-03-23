from tkinter import *
import tkinter.messagebox
import visacommands

# Global variables
VERSION_NUMBER = "PyCal v1.01"
SELECTED_PORT = ""
SELECTED_ADDRESS = ""
SELECTED_INSTRUMENT = ""
CONNECTED_INSTRUMENT = ""


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
        self.file_subMenu.add_command(label="Save")
        self.file_subMenu.add_separator()
        self.file_subMenu.add_command(label="Exit", command=master.quit)

        # Creates edit menu
        self.edit_subMenu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="Edit", menu=self.edit_subMenu)

        # Creates help menu
        self.help_submenu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="Help", menu=self.help_submenu)
        self.help_submenu.add_command(label="About", command=self.get_version_number)

        # Select Instrument
        self.available_instruments = visacommands.AVAILABLE_INSTRUMENTS
        self.instruments = StringVar(master)
        self.instruments.set("Select Instrument")
        self.instruments = OptionMenu(master, self.instruments, *self.available_instruments,
                                      command=self.selected_instrument)
        self.instruments.grid(column=3, row=0, padx=5, pady=5, sticky=W)

        # Select GPIB port
        self.available_ports = list(range(4))
        self.GPIB_ports = StringVar(master)
        self.GPIB_ports.set("GPIB Port")
        self.gpib_ports = OptionMenu(master, self.GPIB_ports, *self.available_ports,
                                     command=self.selected_port)
        self.gpib_ports.grid(column=1, row=0, padx=5, pady=5, sticky=W)

        # Select GPIB address
        self.available_addresses = list(range(30))
        self.GPIB_addresses = StringVar(master)
        self.GPIB_addresses.set("GPIB Address")
        self.gpib_address = OptionMenu(master, self.GPIB_addresses, *self.available_addresses,
                                       command=self.selected_address)
        self.gpib_address.grid(column=2, row=0, padx=5, pady=5, sticky=W)

        # Lists resources
        self.list_resources_button = Button(master, text="List Resources", command=self.list_resources)
        self.list_resources_button.grid(column=0, row=0, padx=5, pady=5, sticky=W)

        # Connects instrument to instrument
        self.connect_button = Button(master, text="Connect", command=self.address_checker)
        self.connect_button.grid(column=4, row=0, padx=5, pady=5, sticky=W)

    # Checks if instrument is connected at an address
    def address_checker(self):
        self.resources = visacommands.list_resources()
        self.test_address = f"GPIB{SELECTED_PORT}::{SELECTED_ADDRESS}::INSTR"
        if self.test_address in self.resources:
            self.connect()
            self.create_window()
        else:
            tkinter.messagebox.showinfo("Error", f"No instrument connected at address GPIB{SELECTED_PORT}::{SELECTED_ADDRESS}.")

    def create_window(self):
        """
        Opens a new window that controls the selected instrument by opening its class
        """
        global SELECTED_INSTRUMENT
        self.new_window = Toplevel(self.master)

        # Runs the selected class. Insert new instruments here.
        if SELECTED_INSTRUMENT == "3478A":
            self.app = NotAvailable(self.new_window)
        elif SELECTED_INSTRUMENT == "34401A":
            self.app = Unit34401A(self.new_window)
        elif SELECTED_INSTRUMENT == "5520A":
            self.app = Unit5520A(self.new_window)

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
        global SELECTED_ADDRESS
        SELECTED_ADDRESS = value
        return value

    @staticmethod
    def selected_port(value):
        global SELECTED_PORT
        SELECTED_PORT = value
        return value

    @staticmethod
    def selected_instrument(value):
        global SELECTED_INSTRUMENT
        SELECTED_INSTRUMENT = value
        return value

    @staticmethod
    def connect():
        global CONNECTED_INSTRUMENT
        CONNECTED_INSTRUMENT = f"GPIB{SELECTED_PORT}::{SELECTED_ADDRESS}::INSTR"
        # connected_instrument = "GPIB{0}::{1}::INSTR".format(selected_port_from_list, selected_address_from_list)
        visacommands.open_instrument(CONNECTED_INSTRUMENT)

# Instrument Classes


class NotAvailable(Toplevel):
    def __init__(self, master):
        self.master = master
        label = Label(master, text="Not yet available")
        label.pack()


class Unit34401A(Toplevel):
    def __init__(self, master):
        self.master = master
        self.this_instrument = SELECTED_INSTRUMENT
        master.title(self.this_instrument)

        # Variable to ensure this window is always connected to this instrument
        self.connect_instrument = CONNECTED_INSTRUMENT

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
        display = Label(master, textvariable=self.display_value, font=("Arial", 24), compound=RIGHT,
                        relief="ridge", anchor=E, height=2)
        display.grid(row=3, column=1, columnspan=3,
                     ipadx=5, ipady=3, sticky="EW")

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
        self.this_instrument = SELECTED_INSTRUMENT
        master.title(self.this_instrument)

        # Variable to ensure this window is always connected to this instrument
        self.connect_instrument = CONNECTED_INSTRUMENT



# Runs the main root display
if __name__ == "__main__":
    root = Tk()
    pycal = PyCal(root)
    root.mainloop()
