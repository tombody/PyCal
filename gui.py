from tkinter import *
import visacommands


class GUI:
    def __init__(self, master):
        self.master = master
        master.title("PyCal v1.0")

        # Setting up the main root frames
        self.top_frame = Frame(master)
        self.top_frame.pack()
        self.bottom_frame = Frame(master)
        self.bottom_frame.pack(side=BOTTOM)

        self.list_resources_button = Button(self.top_frame, text="List Resources", command=self.list_resources)
        self.list_resources_button.pack()

        self.close_button = Button(self.bottom_frame, text="Close", command=master.quit)
        self.close_button.pack()

    """
    Prints a list of available instruments to a new window
    """
    def list_resources(self):
        nw = Tk()
        nw.title = "Resources"
        resources = Label(nw, text=visacommands.list_resources())
        resources.pack()


# Runs the main root display
root = Tk()
pycal_gui = GUI(root)
root.mainloop()
