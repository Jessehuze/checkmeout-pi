import requests

# scan ADMIN_ID to switch between checkin and checkout station
ADMIN_ID = 123
STORE_ID = 1

def set_kiosk_type():
    """
    PURPOSE: determines the kiosk type (checkin or checkout)
    RETURNS: "in" or "out"
    """
    # clear the terminal
    print chr(27) + "[2J"
    # print the header title
    print "#"*80
    print
    print "Admin Panel"
    print
    print "#"*80
    print

    # get input from user
    print "Checking in or checking out?"
    in_out = raw_input("in/out: ")
    while in_out not in ("in", "out"):
        in_out = raw_input("in/out: ")

    return in_out

def kiosk_display(in_out):
    """
    PURPOSE: Displays the kiosk header for kiosk type (in or out)
    """
    # clear the terminal
    print chr(27) + "[2J"

    print "#"*80
    print
    print "Welcome to the Check%s Kiosk!" % in_out
    print
    print "#"*80
    print

def scan_items():
    """
    PURPOSE: Scan items from keyboard input
    RETURNS: list of item numbers (formated as strings)
    """
    print "Scan items, type 'done' to quit"
    items = []
    itemID = raw_input("> ")
    while itemID != "done":
        #TODO: verify that item has not already been scanned
        items.append(itemID)
        itemID = raw_input("> ")

    return items

def send_request(in_out, userID, items):
    """
    PURPOSE: sends get request to server, checking items either in or out
    PARAMETERS: in_out: string, "in" or "out"
                userID: int, user ID
                items: list of strings, each string is an item ID
    """
    # get request (sends data to database)
    req_str = "http://api.checkmeout.dev/check%s?SID=%d&UID=%d&items=[%s]"
    r = requests.get(req_str % (in_out, STORE_ID, userID, ",".join(items)))

    # check response (get data from database)
    if r.status_code == 200:
        for key, value in r.json().items():
            print "%s: %r" % (key, value)

    else:
        print "ERROR: %d" % r.status_code

def main():
    """
    PURPOSE: loop kiosk progam endlessly
    """
    while True: # endless loop
        # set kiosk function (checkin or checkout)
        in_out = set_kiosk_type()

        while True:
            kiosk_display(in_out)
            userID = int(raw_input("Scan ID card to begin: "))
            # return to kiosk type menu if Admin ID is entered
            if userID == ADMIN_ID:
                break
            # scan items and send them to the database
            items = scan_items()
            send_request(in_out, userID, items)

if __name__ == "__main__":
    main()
