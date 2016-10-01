import requests

# scan ADMIN_ID to switch between checkin and checkout station
ADMIN_ID = 123
STORE_ID = 1

def set_kiosk_type():
    """
    determines the kiosk type (checkin or checkout)
    """
    # clear the terminal
    print chr(27) + "[2J"

    print "#"*80
    print
    print "Admin Panel"
    print
    print "#"*80
    print

    print "Checking in or checking out?"
    in_out = raw_input("in/out: ")
    while in_out not in ("in", "out"):
        in_out = raw_input("in/out: ")

    return in_out

def kiosk_display(in_out):
    """
    Displays the kiosk header for kiosk type (in or out)
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
    print "Scan items, type 'done' to quit"
    items = []
    itemID = raw_input("> ")
    while itemID != "done":
        items.append(itemID)
        itemID = raw_input("> ")

    return items

def send_request(in_out, userID, items):
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
    while True: # endless loop
        in_out = set_kiosk_type()
        while True:
            kiosk_display(in_out)
            userID = int(raw_input("Scan ID card to begin: "))
            if userID == ADMIN_ID:
                break
            items = scan_items()
            send_request(in_out, userID, items)

if __name__ == "__main__":
    main()
