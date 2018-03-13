from tkinter import *
import visacommands


class GUI:
    def __init__(self, master):
        self.master = master
        master.title("PyCal v1.0")

        self.label = Label(master, text="PyCal v1.0")
        self.label.pack()

        self.greet_button = Button(master, text="List Resources", command=self.list_resources)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    """
    Prints a list of available instruments
    """
    def list_resources(self):
        print(visacommands.list_resources())


# Runs the tkinter display
root = Tk()
pycal_gui = GUI(root)
root.mainloop()
