from tkinter import *
import tkinter.messagebox
import visacommands

version_number = "PyCal v1.0"


class GUI:
    def __init__(self, master):
        # Sets root title and min window size
        self.master = master
        master.title(version_number)
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
        self.available_instruments = ["3478A",]
        self.instruments = StringVar(master)
        self.instruments.set("Select Instrument")
        self.instruments = OptionMenu(master, self.instruments, self.available_instruments,
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
        self.gpib_address.grid(column=2, row=0, padx=5, pady=5,  sticky=W)

        # Lists resources
        self.list_resources_button = Button(master, text="List Resources", command=self.list_resources)
        self.list_resources_button.grid(column=0, row=0, padx=5, pady=5, sticky=W)

        # Connects instrument to instrument
        self.connect_button = Button(master, text="Connect", command=self.connect)
        self.connect_button.grid(column=4, row=0, padx=5, pady=5, sticky=W)


    """
    Prints a list of available instruments to a new window
    """
    def list_resources(self):
        tkinter.messagebox.showinfo("Resource List", '\n'.join(visacommands.list_resources()))

    def get_version_number(self):
        tkinter.messagebox._show("About", version_number)

    def selected_address(self, value):
        return value

    def selected_port(self, value):
        return value

    def selected_instrument(self, value):
        return value

    def connect(self):
        # Use to open window to control instrument
        pass



# Runs the main root display
root = Tk()
pycal_gui = GUI(root)
root.mainloop()
