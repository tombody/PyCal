from tkinter import *
import tkinter.messagebox
import pycal

pycal.Toplevel()

class Unit3478A():
    def __init__(self, master):
        # Lists resources
        self.list_resources_button = Button(master, text="List Resources")
        self.list_resources_button.grid(column=0, row=0, padx=5, pady=5, sticky=W)
        window = tkinter.Toplevel(master)
        # window.title(selected_instrument_from_list)
