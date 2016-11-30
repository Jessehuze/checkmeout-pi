""" simple app to lean TK """

import Tkinter as tk
import RFID_reader as kiosk

class Application(tk.Frame):
    """ the main application, child of TK frame """
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=(tk.N + tk.S + tk.E + tk.W))
        self.create_widgets()
        self.items = tk.StringVar()
    
    def append_items(self, item="None"):
        self.items.set(self.items.get() + item)
        self.listbox_w.listvariable = self.items


    def create_widgets(self):
        """ creates all the 'widgets' or app features """
        # make the first row and col of the window stretchable
        top = self.winfo_toplevel()
        top.rowconfigure(1, weight=1)
        top.columnconfigure(1, weight=1)
        # make the first row and col of the app stretchable
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)

        # create text entry box
        self.entry_box = tk.Entry()
        self.entry_box.grid(row=0, column=1)

        # create a listbox
        list_str = tk.StringVar()
        list_str.set('ant bee cicada')
        self.listbox_w = tk.Listbox(
            background="gray",
            listvariable=list_str
        )
        self.listbox_w.grid(
            row=1, column=1,
            sticky=(tk.N + tk.S + tk.E + tk.W),
            pady=20, padx=20
        )
        # create a button that does not resize in a cell that does not resize
        self.quit_static = tk.Button(self, text='Quit', command=self.quit)
        self.quit_static.grid(row=0, column=0, sticky=(tk.N))
        self.quit_static = tk.Button(self, text='Add', command=self.quit)
        self.quit_static.grid(row=1, column=0, sticky=(tk.N))

app = Application()
# app.bind('<KP_0>', app.add_0)
app.bind('<Return>', app.append_items)
app.master.title('Sample application')
app.mainloop()
