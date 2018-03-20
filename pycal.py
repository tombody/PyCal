from tkinter import *
import tkinter.messagebox
import visacommands

# Global variables
VERSION_NUMBER = "PyCal v1.0"
SELECTED_PORT_FROM_LIST = ""
SELECTED_ADDRESS_FROM_LIST = ""
SELECTED_INSTRUMENT_FROM_LIST = ""
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
        self.available_addresses = list(range(25))
        self.GPIB_addresses = StringVar(master)
        self.GPIB_addresses.set("GPIB Address")
        self.gpib_address = OptionMenu(master, self.GPIB_addresses, *self.available_addresses,
                                       command=self.selected_address)
        self.gpib_address.grid(column=2, row=0, padx=5, pady=5, sticky=W)

        # Lists resources
        self.list_resources_button = Button(master, text="List Resources", command=self.list_resources)
        self.list_resources_button.grid(column=0, row=0, padx=5, pady=5, sticky=W)

        # Connects instrument to instrument
        self.connect_button = Button(master, text="Connect", command=lambda: [self.connect(), self.create_window()])
        self.connect_button.grid(column=4, row=0, padx=5, pady=5, sticky=W)

    def create_window(self):
        """
        Opens a new window that controls the selected instrument by opening its class
        """
        global SELECTED_INSTRUMENT_FROM_LIST
        self.new_window = Toplevel(self.master)

        # Runs the selected class. Insert new instruments here.
        if SELECTED_INSTRUMENT_FROM_LIST == "3478A":
            self.app = NotAvailable(self.new_window)
        elif SELECTED_INSTRUMENT_FROM_LIST == "34401A":
            self.app = Unit_34401A(self.new_window)
        elif SELECTED_INSTRUMENT_FROM_LIST == "5520A":
            self.app = NotAvailable(self.new_window)

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
        global SELECTED_ADDRESS_FROM_LIST
        SELECTED_ADDRESS_FROM_LIST = value
        return value

    @staticmethod
    def selected_port(value):
        global SELECTED_PORT_FROM_LIST
        SELECTED_PORT_FROM_LIST = value
        return value

    @staticmethod
    def selected_instrument(value):
        global SELECTED_INSTRUMENT_FROM_LIST
        SELECTED_INSTRUMENT_FROM_LIST = value
        return value

    @staticmethod
    def connect():
        global CONNECTED_INSTRUMENT
        CONNECTED_INSTRUMENT = f"GPIB{SELECTED_PORT_FROM_LIST}::{SELECTED_ADDRESS_FROM_LIST}::INSTR"
        # connected_instrument = "GPIB{0}::{1}::INSTR".format(selected_port_from_list, selected_address_from_list)
        visacommands.open_instrument(CONNECTED_INSTRUMENT)

# Instrument Classes

class NotAvailable(Toplevel):
    def __init__(self, master):
        self.master = master
        label = Label(master, text="Not yet available")
        label.pack()

class Unit_34401A(Toplevel):
    def __init__(self, master):
        self.master = master
        master.title(SELECTED_INSTRUMENT_FROM_LIST)

        # 34401A Functions list
        self.functions = [("DC-V",1),("AC-V",2),
                          ("Ω-2W",3),("Ω-4W",4),
                          ("Freq",5),("Period",6),
                          ("Cont",7),("Diode",8)]
        v = IntVar()
        for val, func in enumerate(self.functions):
            options = Radiobutton(master, text=func, width=15,
                                  variable=v, value=val, indicatoron=0)
            options.grid(row=0, column=val)

# Runs the main root display
if __name__ == "__main__":
    root = Tk()
    pycal = PyCal(root)
    root.mainloop()