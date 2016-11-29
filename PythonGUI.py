from Tkinter import *
from ScrolledText import *
import ttk
import Tkinter as tk
import tkMessageBox
import tkFont
from PIL import ImageTk,Image

num1 = 150
side_num = 0

def addToList(*args):
    try:
    	global num1
    	global side_num
    	value = fileName.get()
    	if side_num == 0:
    		label2 = main_canvas.create_text(100, num1, font=("Work Sans", 20),  tags="item_labels", text=value, anchor="w")
    	elif side_num == 1:
    		label2 = main_canvas.create_text(1600, num1, font=("Work Sans", 20),  tags="item_labels", text=value, anchor="e")
    	num1 = num1 + 40
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
		homeButtonOut.place(x=1200, y=800, width=380, height=130)
		fileName_entry.place(x=-530, y=-900, width=500, height=40)
		main_canvas.create_image(1300, 175, image=small_logo, tags="small_logo")
		promptOut = main_canvas.create_text(1350, 500, font=("Purisa", 30),  tags="promptOut", text="Scan your items and press\n"
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
		homeButtonIn.place(x=50, y=800, width=380, height=130)
		fileName_entry.place(x=-600, y=-900, width=500, height=40)
		main_canvas.create_image(400, 175, image=small_logo, tags="small_logo")
		promptIn = main_canvas.create_text(350, 500, font=("Purisa", 30),  tags="promptIn", text="Scan your items and press\n"
		 																			+ "'check in' when you're\n"
		 																			+ "finished.")
	except ValueError:
		pass

def goHomefromOut(*args):
    try:
    	global num1
    	num1 = 150
    	main_canvas.delete("small_logo")
    	main_canvas.delete("promptOut")
    	main_canvas.delete("item_labels")
    	homeButtonOut.place(x=-446, y=-116)
    	main_canvas.create_image(850, 300, image=main_logo, tags="logo")
    	checkOutButton.place(x=660, y=800, width=380, height=130)
    	checkInButton.place(x=660, y=600, width=380, height=130)
    	fileName_entry.place(x=-500, y=-20, width=300, height=30)
    	fileName_entry.delete(0,END)
    except ValueError:
    	pass

def goHomefromIn(*args):
    try:
    	global num1
    	num1 = 150
    	main_canvas.delete("small_logo")
    	main_canvas.delete("promptIn")
    	main_canvas.delete("item_labels")
    	homeButtonIn.place(x=-446, y=-116)
    	main_canvas.create_image(850, 300, image=main_logo, tags="logo")
    	checkOutButton.place(x=660, y=800, width=380, height=130)
    	checkInButton.place(x=660, y=600, width=380, height=130)
    	fileName_entry.place(x=-500, y=-20, width=300, height=30)
    	fileName_entry.delete(0,END)
    except ValueError:
    	pass

root = tk.Tk()
root.title("CheckMeOut (Kiosk 1)")
root.geometry('1700x1000')

frame = Frame(root)
frame.pack()

main_canvas = Canvas(frame, bg="black", width=1700, height=1000)
main_canvas.pack()

# creates the image for the background and adds it to the canvas
background_image = ImageTk.PhotoImage(file="background.gif")
main_canvas.create_image(850, 500, image=background_image)

#creates the image for the main logo and adds it to the canvas
main_logo = ImageTk.PhotoImage(file="main_logo.png")
main_canvas.create_image(850, 300, image=main_logo, tags="logo")


small_logo = ImageTk.PhotoImage(file="small_logo.png")
#main_canvas.create_image(975, 100, image=small_logo, tags="small_logo")

# Initializes variable fileName
fileName = StringVar()

# Sets fileName to entered data
fileName_entry = Entry(root, textvariable=fileName)
fileName_entry.configure(bg = '#d79600')


#text = fileName

# Check Out button
checkOutButton = Button(root, text="Check Out", command=checkout, highlightthickness=0,bd=0, activebackground='white')
checkOutButton.pack()
checkOutButton.place(x=660, y=800, width=380, height=130)
checkOutImg = PhotoImage(file = 'checkout_button.png')
checkOutButton.configure(image = checkOutImg, bg='white')

# Check In button
checkInButton = Button(root, text="Check In", command=checkin, highlightthickness=0,bd=0, activebackground='white')
checkInButton.pack()
checkInButton.place(x=660, y=600, width=380, height=130)
checkInImg = PhotoImage(file = 'checkin_button.png')
checkInButton.configure(image = checkInImg, bg='white')

# Home button from Check In
homeButtonIn = Button(root, text="Home", command=goHomefromIn, highlightthickness=0,bd=0, activebackground='white')
homeImageIn = PhotoImage(file = 'checkin_button.png')
homeButtonIn.configure(image = homeImageIn, bg='white')

#Home button from Check Out
homeButtonOut = Button(root, text="Home", command=goHomefromOut, highlightthickness=0,bd=0, activebackground='white')
homeImageOut = PhotoImage(file = 'checkout_button.png')
homeButtonOut.configure(image = homeImageOut, bg='white')

fileName_entry.focus()
root.bind('<Return>', addToList)

root.mainloop()



#--- Colors used in porject ---

#orange #d79600
#blue #51b5e4
#transblakc: rgba(0,0,0,.78)
#white #fff
