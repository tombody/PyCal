from tkinter import *
import visacommands

root = Tk()
menubar = Menu(root)


class GUI:
    def __init__(self, master):
        self.master = master
        master.title("PyCal v1.0")

        self.label = Label(master, text="Big text")
        self.label.pack()

        self.greet_button = Button(master, text="Identify unit", command=self.greet)
        self.greet_button.pack()

        self.address_menu = Menu(menubar, tearoff=0)
        self.address_menu.add_command(label="Create script", command=self.menuButton)

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def greet(self):
        print(visacommands.command)

    def menuButton(self):
        filewin = Toplevel(root)
        button = Button(filewin, text="Place Holder")
        button.pack()


root.config(menu=menubar)

pycal_gui = GUI(root)
root.mainloop()
