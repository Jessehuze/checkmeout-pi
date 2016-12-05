import Tkinter as tk
from PIL import ImageTk
from sys import platform
import functionality as func

# disable certain linting warnings
# pylint: disable=W0312,C0103,C0301,W0603

num1 = 50
side_num = 2
validID = False
name = ""

#### FUNCTIONS ############################################################

def addToList(*args):
	""" called each time the enter key is pressed, parses keyboad input """
	global num1, validID, name
	global side_num
	value = fileName.get()
	success = True

	if side_num == 0: # left side (checkout)
		(item_name, success) = func.verify_item(value)
		label2 = main_canvas.create_text(30, num1, font=("Work Sans", 18), tags="item_labels", text=item_name, anchor="w")

	elif side_num == 1: # right side (checkin)
		(item_name, success) = func.verify_item(value)
		label2 = main_canvas.create_text(770, num1, font=("Work Sans", 18), tags="item_labels", text=item_name, anchor="e")

	elif side_num == 2: # hidden off-screen right
		label2 = main_canvas.create_text(900, num1, font=("Work Sans", 18), tags="item_labels", text=value, anchor="w")

	elif side_num == -1: # hidden off-screen right, read in as userID
		label2 = main_canvas.create_text(900, num1, font=("Work Sans", 18), tags="item_labels", text=value, anchor="w")

		if value:
			(name, validID) = func.verify_user(value)
			if validID:
				checkout()
			else:
				goHomefromLogin()
				# DALTON: show error message: "Invalid User ID"
	num1 = num1 + 30
	fileName_entry.delete(0, tk.END)

	return success

def login(*args):
	""" after selecting checkout, display prompt user for user ID """
	try:
		global side_num
		side_num = -1
		checkInButton.place(x=-446, y=-116)
		checkOutButton.place(x=-446, y=-116)
		fileName_entry.place(x=-600, y=-900, width=500, height=40)
		loginPrompt = main_canvas.create_text(400, 320, font=("Purisa", 27), tags="loginPrompt", text="Scan your ID card to login.")

	except ValueError:
		pass

def checkout(*args):
	""" checkout items screen, display buttons and info for checkOUT function """
	try:
		global side_num, num1, name
		num1 = 50
		side_num = 0
		func.set_kiosk_type("out")

		# hide unessissary buttons
		checkInButton.place(x=-446, y=-116)
		checkOutButton.place(x=-446, y=-116)
		loginToCheckoutButton.place(x=-446, y=-116)
		# delete unessissary logos
		main_canvas.delete("logo")
		main_canvas.delete("loginPrompt")
		# place complete checkout button
		homeButtonOut.place(x=520, y=383, width=225, height=77)
		# place text/logos
		fileName_entry.place(x=-530, y=-900, width=500, height=40)
		main_canvas.create_image(620, 60, image=small_logo, tags="small_logo")
		username = main_canvas.create_text(790, 180, font=("Purisa", 15), tags="username", text=" Welcome, " + name + "...", anchor="e")
		promptOut = main_canvas.create_text(630, 280, font=("Purisa", 15), tags="promptOut", text="Scan your items and press\n"
		 																			+ "'check out' when you're\n"
		 																			+ "finished.")
	except ValueError:
		pass

def checkin(*args):
	""" checkin items screen, display buttons and info for checkIN function """
	global side_num
	side_num = 1
	func.set_kiosk_type("in")

	# hide unessissary buttons/logos
	checkInButton.place(x=-446, y=-116)
	checkOutButton.place(x=-446, y=-116)
	main_canvas.delete("logo")
	# place needed buttons, logos, text
	homeButtonIn.place(x=55, y=383, width=225, height=77)
	fileName_entry.place(x=-600, y=-900, width=500, height=40)
	main_canvas.create_image(185, 60, image=small_logo, tags="small_logo")
	promptIn = main_canvas.create_text(165, 210, font=("Purisa", 15), tags="promptIn", text="Scan your items and press\n"
																				+ "'check in' when you're\n"
																				+ "finished.")

def goHomefromLogin():
	""" transision back to homescreen, hide login diplay, place homescreen display """
	main_canvas.delete("logo")
	main_canvas.delete("loginPrompt")
	loginToCheckoutButton.place(x=-446, y=-116)
	goHomefromOut()


def goHomefromOut(*args):
	""" transision back to homescreen, hide checkout diplay, place homescreen display """
	global num1, side_num
	side_num = 2
	num1 = 50

	# TREVOR: send checkout items to database, refresh reservations list, return response
	func.send_request()
	func.sync_database()
	# DALTON: implement method of displaying alert if checkout should fail

	# hide items from checkout display
	main_canvas.delete("small_logo")
	main_canvas.delete("promptOut")
	main_canvas.delete("item_labels")
	main_canvas.delete("username")
	homeButtonOut.place(x=-446, y=-116)
	# place items from homescreen diplay
	main_canvas.create_image(400, 125, image=main_logo, tags="logo")
	checkOutButton.place(x=288, y=380, width=225, height=77)
	checkInButton.place(x=288, y=280, width=225, height=77)
	fileName_entry.place(x=-500, y=-20, width=300, height=30)
	fileName_entry.delete(0, tk.END)

def goHomefromIn(*args):
	""" transision back to homescreen, hide checkin diplay, place homescreen display """
	try:
		global num1, side_num
		side_num = 2
		num1 = 50

		# TREVOR: send checkin items to database, refresh reservations list, return response
		func.send_request()
		func.sync_database()
		# DALTON: implement method of displaying alert if checkin should fail

		# hide items from checkin display
		main_canvas.delete("small_logo")
		main_canvas.delete("promptIn")
		main_canvas.delete("item_labels")
		homeButtonIn.place(x=-446, y=-116)
		# place items from homescreen diplay
		main_canvas.create_image(400, 125, image=main_logo, tags="logo")
		checkOutButton.place(x=288, y=380, width=225, height=77)
		checkInButton.place(x=288, y=280, width=225, height=77)
		fileName_entry.place(x=-500, y=-20, width=300, height=30)
		fileName_entry.delete(0, tk.END)
	except ValueError:
		pass


#### MAIN ######################################################################

# SYNC FROM DATABASE
func.sync_database(update_all=True)

# initialize the window
root = tk.Tk()
root.title("CheckMeOut (Kiosk 1)")
root.geometry('800x480')

# apply display toggles
if platform == "darwin" or platform == "win32":
    # running on windows or mac, show cursor
	CURSOR = ''
else:
	# linux (pi), fullscreen and hide cursor
	root.attributes("-fullscreen", True)
	CURSOR = 'none'

# initialize the frame, main canvas
frame = tk.Frame(root)
frame.config(cursor=CURSOR)
frame.pack()

main_canvas = tk.Canvas(frame, bg="white", width=800, height=480)
main_canvas.pack()

# creates the image for the background and adds it to the canvas
background_image = ImageTk.PhotoImage(file="KioskBackground.gif")
main_canvas.create_image(400, 240, image=background_image)

#creates the image for the main logo and adds it to the canvas
main_logo = ImageTk.PhotoImage(file="KioskMainLogo.png")
main_canvas.create_image(400, 125, image=main_logo, tags="logo")

small_logo = ImageTk.PhotoImage(file="KioskSmallLogo.png")

# Initializes variable fileName (to be used to store keyboard input)
fileName = tk.StringVar()

# Sets fileName to entered data
fileName_entry = tk.Entry(root, textvariable=fileName)
fileName_entry.configure(bg='#d79600')

# Check Out button
checkOutButton = tk.Button(root, text="Check Out", command=login, highlightthickness=0, bd=0, activebackground='white', cursor=CURSOR)
checkOutButton.pack()
checkOutButton.place(x=288, y=380, width=225, height=77)
checkOutImg = ImageTk.PhotoImage(file='KioskCheckOut.png')
checkOutButton.configure(image=checkOutImg, bg='white')

# Check In button
checkInButton = tk.Button(root, text="Check In", command=checkin, highlightthickness=0, bd=0, activebackground='white', cursor=CURSOR)
checkInButton.pack()
checkInButton.place(x=288, y=280, width=225, height=77)
checkInImg = ImageTk.PhotoImage(file='KioskCheckIn.png')
checkInButton.configure(image=checkInImg, bg='white')

# Home button from Check In
homeButtonIn = tk.Button(root, text="Home", command=goHomefromIn, highlightthickness=0, bd=0, activebackground='white', cursor=CURSOR)
homeImageIn = ImageTk.PhotoImage(file='KioskCheckIn.png')
homeButtonIn.configure(image=homeImageIn, bg='white')

# Home button from Check Out
homeButtonOut = tk.Button(root, text="Home", command=goHomefromOut, highlightthickness=0, bd=0, activebackground='white', cursor=CURSOR)
homeImageOut = ImageTk.PhotoImage(file='KioskCheckOut.png')
homeButtonOut.configure(image=homeImageOut, bg='white')

# Checkout Button from Login
loginToCheckoutButton = tk.Button(root, text="Check Out", command=checkout, highlightthickness=0, bd=0, activebackground='white', cursor=CURSOR)
checkOutImgFromLogin = ImageTk.PhotoImage(file='KioskCheckOut.png')
loginToCheckoutButton.configure(image=checkOutImgFromLogin, bg='white')

fileName_entry.focus()
# root.focus_set()
root.bind('<Return>', addToList)
root.bind("<Escape>", lambda e: e.widget.quit())

root.mainloop()



#--- Colors used in porject ---

#orange #d79600
#blue #51b5e4
#transblakc: rgba(0,0,0,.78)
#white #fff
