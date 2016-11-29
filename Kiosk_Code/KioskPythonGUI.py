from Tkinter import *
from ScrolledText import *
import ttk
import Tkinter as tk
import tkMessageBox
import tkFont
from PIL import ImageTk,Image

num1 = 50
side_num = 0

def addToList(*args):
    try:
    	global num1
    	global side_num
    	value = fileName.get()
    	if side_num == 0:
    		label2 = main_canvas.create_text(30, num1, font=("Work Sans", 18),  tags="item_labels", text=value, anchor="w")
    	elif side_num == 1:
    		label2 = main_canvas.create_text(770, num1, font=("Work Sans", 18),  tags="item_labels", text=value, anchor="e")
    	num1 = num1 + 30
    	fileName_entry.delete(0,END)
    except ValueError:
    	pass

def checkout(*args):
	try:
		global side_num
		side_num = 0
		checkInButton.place(x=-446, y=-116)
		checkOutButton.place(x=-446, y=-116)
		main_canvas.delete("logo")
		homeButtonOut.place(x=520, y=383, width=225, height=77)
		fileName_entry.place(x=-530, y=-900, width=500, height=40)
		main_canvas.create_image(620, 60, image=small_logo, tags="small_logo")
		promptOut = main_canvas.create_text(630, 210, font=("Purisa", 15),  tags="promptOut", text="Scan your items and press\n"
		 																			+ "'check out' when you're\n"
		 																			+ "finished.")
	except ValueError:
		pass

def checkin(*args):
	try:
		global side_num
		side_num = 1
		checkInButton.place(x=-446, y=-116)
		checkOutButton.place(x=-446, y=-116)
		main_canvas.delete("logo")
		homeButtonIn.place(x=55, y=383, width=225, height=77)
		fileName_entry.place(x=-600, y=-900, width=500, height=40)
		main_canvas.create_image(185, 60, image=small_logo, tags="small_logo")
		promptIn = main_canvas.create_text(165, 210, font=("Purisa", 15),  tags="promptIn", text="Scan your items and press\n"
		 																			+ "'check in' when you're\n"
		 																			+ "finished.")
	except ValueError:
		pass

def goHomefromOut(*args):
    try:
    	global num1
    	num1 = 50
    	main_canvas.delete("small_logo")
    	main_canvas.delete("promptOut")
    	main_canvas.delete("item_labels")
    	homeButtonOut.place(x=-446, y=-116)
    	main_canvas.create_image(400, 125, image=main_logo, tags="logo")
    	checkOutButton.place(x=288, y=380, width=225, height=77)
    	checkInButton.place(x=288, y=280, width=225, height=77)
    	fileName_entry.place(x=-500, y=-20, width=300, height=30)
    	fileName_entry.delete(0,END)
    except ValueError:
    	pass

def goHomefromIn(*args):
    try:
    	global num1
    	num1 = 50
    	main_canvas.delete("small_logo")
    	main_canvas.delete("promptIn")
    	main_canvas.delete("item_labels")
    	homeButtonIn.place(x=-446, y=-116)
    	main_canvas.create_image(400, 125, image=main_logo, tags="logo")
    	checkOutButton.place(x=288, y=380, width=225, height=77)
    	checkInButton.place(x=288, y=280, width=225, height=77)
    	fileName_entry.place(x=-500, y=-20, width=300, height=30)
    	fileName_entry.delete(0,END)
    except ValueError:
    	pass

root = tk.Tk()
root.title("CheckMeOut (Kiosk 1)")
root.geometry('800x480')
root.attributes("-fullscreen", True)

frame = Frame(root)
frame.config(cursor = 'none')
frame.pack()

main_canvas = Canvas(frame, bg="white", width=800, height=480)
main_canvas.pack()

# creates the image for the background and adds it to the canvas
background_image = ImageTk.PhotoImage(file="KioskBackground.gif")
main_canvas.create_image(400, 240, image=background_image)

#creates the image for the main logo and adds it to the canvas
main_logo = ImageTk.PhotoImage(file="KioskMainLogo.png")
main_canvas.create_image(400, 125, image=main_logo, tags="logo")

small_logo = ImageTk.PhotoImage(file="KioskSmallLogo.png")

# Initializes variable fileName
fileName = StringVar()

# Sets fileName to entered data
fileName_entry = Entry(root, textvariable=fileName)
fileName_entry.configure(bg = '#d79600')

# Check Out button
checkOutButton = Button(root, text="Check Out", command=checkout, highlightthickness=0,bd=0, activebackground='white', cursor = 'none')
checkOutButton.pack()
checkOutButton.place(x=288, y=380, width=225, height=77)
checkOutImg = PhotoImage(file = 'KioskCheckOut.png')
checkOutButton.configure(image = checkOutImg, bg='white')

# Check In button
checkInButton = Button(root, text="Check In", command=checkin, highlightthickness=0,bd=0, activebackground='white', cursor = 'none')
checkInButton.pack()
checkInButton.place(x=288, y=280, width=225, height=77)
checkInImg = PhotoImage(file = 'KioskCheckIn.png')
checkInButton.configure(image = checkInImg, bg='white')

# Home button from Check In
homeButtonIn = Button(root, text="Home", command=goHomefromIn, highlightthickness=0,bd=0, activebackground='white', cursor = 'none')
homeImageIn = PhotoImage(file = 'KioskCheckIn.png')
homeButtonIn.configure(image = homeImageIn, bg='white')

#Home button from Check Out
homeButtonOut = Button(root, text="Home", command=goHomefromOut, highlightthickness=0,bd=0, activebackground='white', cursor = 'none')
homeImageOut = PhotoImage(file = 'KioskCheckOut.png')
homeButtonOut.configure(image = homeImageOut, bg='white')

fileName_entry.focus()
#root.focus_set()
root.bind('<Return>', addToList)
root.bind("<Escape>", lambda e: e.widget.quit())

root.mainloop()



#--- Colors used in porject ---

#orange #d79600
#blue #51b5e4
#transblakc: rgba(0,0,0,.78)
#white #fff