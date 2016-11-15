from Tkinter import *
from ScrolledText import *
import ttk

def addToList(*args):
    try:
    	value = fileName.get()
    	textPad.insert(INSERT, value)
    	textPad.insert(INSERT, "\n")
    	fileName_entry.delete(0,END)
    except ValueError:
    	pass

def checkout(*args):
    try:
    	textPad.delete(1.0,END)
    	checkout_label = ttk.Label(mainframe, text="Thank you! Have a nice day!")
    	checkout_label.grid(column=1, row=4)
    except ValueError:
    	pass


root = Tk()
root.title("CheckMeOut (Kiosk 1)")

fileName = StringVar()

mainframe = Frame(root, width=20, height=20)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.configure(bg="#51b5e4")
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

textPad = ScrolledText(mainframe, width=50, height=20)
textPad.configure(bg = '#d79600')
textPad.grid(column=0, row=3, sticky=W)

fileName_entry = Entry(mainframe, width=25, textvariable=fileName)
fileName_entry.configure(bg = '#d79600')
fileName_entry.grid(column=0, row=1, sticky=(W, E))

text = fileName

button1 = Button(mainframe, text="Add Item", command=addToList)
button1.grid(column=1, row=1, sticky=W)
button1.configure(font=('Sans','12','bold'),background = 'sea green', foreground = 'white')

button2 = Button(mainframe, text="Checkout", command=checkout)
button2.grid(column=1, row=2, sticky=W)
button2.configure(font=('Sans','12','bold'),background = 'blue', foreground = 'white')

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

fileName_entry.focus()
root.bind('<Return>', addToList)

root.mainloop()



#--- Colors used in porject ---

#orange #d79600
#blue #51b5e4
#transblakc: rgba(0,0,0,.78)
#white #fff