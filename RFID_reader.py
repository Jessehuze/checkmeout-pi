"""
PURPOSE: accept input from an external RFID reader and communicate the scanned items with
         the database in order to check items in and out. This code is meant to run on a
         rasberry pi with connected RFID reader.
"""
import sys
import time
import requests

# scan ADMIN_ID to switch between checkin and checkout station
ADMIN_ID = 123
STORE_ID = 1
# color terminal output
HEADER = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


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


def scan_items(items, reservations, in_out):
    """
    PURPOSE: Scan items from keyboard input
    PARAMETERS: items: dict of items in database
                reservations: dict of reservations in database
                in_out: string, "in" or "out"
    RETURNS: list of item numbers (formated as integers)
    """
    print "Scan items, type 'done' to finish"
    scanned_items = []

    while True:
        tag_id = raw_input("> ")
        # loop until user is done
        if tag_id == "done":
            break
        # ensure tag_id is an integer
        try:
            tag_id = int(tag_id)
        except ValueError:
            print "tag ID: %r is of an invalid format, must be integer. Enter 'done' to finish" % tag_id
            continue
        # ensure tag_id is a valid tag_id
        if tag_id not in items.keys():
            print "Invalid tag ID: %r" % tag_id
            print "Valid tag IDs: %r" % items.keys()
            continue
        # ensure item has not already been checked in this cycle
        if tag_id in scanned_items:
            print "Item '%s' has already been scanned" % items[tag_id]["name"]
            continue
        # ensure item is available to check in
        if in_out == "in":
            if tag_id not in reservations.keys():
                print "Item '%s' could not be checked in because it is not currently checked out" % items[tag_id]["name"]
                continue
        # ensure item is available to check out
        elif in_out == "out":
            if tag_id in reservations.keys():
                print "Item '%s' could not be checked out because it is not currently checked in" % items[tag_id]["name"]
                continue
        else:
            raise ValueError("invalid value for in_out: %s" % in_out)

        # item is availible to check in or out
        print "Checked %s %s" % (in_out, items[tag_id]["name"])
        scanned_items.append(tag_id)

    return scanned_items


def send_request(in_out, user_id, items):
    """
    PURPOSE: sends get request to server, checking items either in or out
    PARAMETERS: in_out: string, "in" or "out"
                user_id: int, user ID
                items: list of strings, each string is an item ID
    """
    results = {"success": [], "fail": []}

    # get request (sends data to database)
    req_str = "http://api.checkmeout.us.to/kiosk/check%s?SID=%d&UID=%d&items=[%s]"
    # req_str = "http://api.checkmeout.dev/kiosk/check%s?SID=%d&UID=%d&items=[%s]"
    response = requests.get(req_str % (in_out, STORE_ID, user_id, ",".join(map(str, items))))

    # check response (get data from database)
    if response.status_code == 200:
        response = response.json()
        # print response
        try:
            print "\nITEMS SUCCEEDED:"

            # response differes based on checking operation
            # TODO: ask about bug:
            #   checking IN response: [... {'items_updated': []}, ...]
            #   checking OUT response: [... {'items_saved': []}, ...]
            if in_out == "in":
                success_key = "items_updated"
            else:
                success_key = "items_saved"

            for item in response[success_key]:
                print item["item_name"]
                results["success"].append(item["item_tag"])
                # print GREEN + item["item_name"] + ENDC # pretty colors
            print "\nITEMS FAILED:"
            for item in response["items_failed"]:
                if "item_name" in item.keys():
                    # valid tag_id but invalid check operation
                    print "%r beacuse %s" % (item["item_name"], item["reason"])
                    results["fail"].append(item["item_tag"])
                    # print "%s%s%s beacuse %s" % (RED, item["item_name"], ENDC, item["reason"]) # pretty colors
                else:
                    # invalid tag_id
                    print "%r beacuse %s" % ("Unknown item", item["reason"])
                    results["fail"].append(item["item_tag"])
                    # print "%s%s%s beacuse %s" % (RED, "'Unknown item'", ENDC, item["reason"]) # pretty colors
        except KeyError:
            print "ENCOUNTERED ERROR PARSING RESPONSE FOR CHECK%s" % in_out
            print response
            exit(1)

        # print "\nRESULT:"
        # for key, value in response.json().items():
        #     print "%s: %r" % (key, value)
    else:
        print "ERROR: %d" % response.status_code


def get_items_from_db():
    """
    PURPOSE: query the database for all the items and return them as a dict
    RETURNS: a dict with the tag_id as the key
    """
    item_dict = {}

    response = requests.get("http://api.checkmeout.us.to/kiosk/item")
    # response = requests.get("http://api.checkmeout.dev/kiosk/item")
    # check response (get data from database)
    if response.status_code == 200:
        for item in response.json()["data"]:
            item_dict[item["tag_id"]] = item
    else:
        raise ValueError("Error getting items from DB")

    return item_dict


def get_reservations_from_db(items):
    """
    PURPOSE: query the database for all the reservations and return them as a dict
    RETURNS: a dict with the tag_id as the key
    """
    reservation_dict = {}

    response = requests.get("http://api.checkmeout.us.to/kiosk/reservation")
    # response = requests.get("http://api.checkmeout.dev/kiosk/reservation")
    # check response (get data from database)
    if response.status_code == 200:
        for reservation in response.json()["data"]:
            if reservation["checkin_time"]:
                # reservation is complete (checked back in), no need to store it
                continue
            else:
                # find the tag_id coorisponding to the item_id of the reservation
                tag_id = None
                for tag_id in items:
                    if items[tag_id]["id"] == reservation["item_id"]:
                        break
                else:
                    raise ValueError("item_id: %d did not match any item_id in items" % reservation["item_id"])
                reservation_dict[tag_id] = reservation
    else:
        raise ValueError("Error getting reservations from DB")

    return reservation_dict


def main():
    """
    PURPOSE: loop kiosk progam endlessly
    """
    items = get_items_from_db()
    reservations = get_reservations_from_db(items)

    while True: # endless loop
        # set kiosk function (checkin or checkout)
        in_out = set_kiosk_type()

        while True:
            kiosk_display(in_out)
            while True:
                try:
                    # TODO: validate user_id
                    user_id = int(raw_input("Scan ID card to begin: "))
                    break
                except ValueError:
                    print "please enter a valid ID"
            # return to kiosk type menu if Admin ID is entered
            if user_id == ADMIN_ID:
                break
            # scan items and send them to the database
            scanned_items = scan_items(items, reservations, in_out)
            if scanned_items:
                send_request(in_out, user_id, scanned_items)
                reservations = get_reservations_from_db(items)
            else:
                print "No items to check %s" % in_out

            # wait x seconds until asking for new user ID
            print "\nContinue... ",
            sys.stdout.flush()  # must flush output because no newline
            continue_delay = 3 # seconds
            for sec in xrange(continue_delay):
                print "%d... " % (continue_delay - sec),
                sys.stdout.flush() # must flush output because no newline
                time.sleep(1)


if __name__ == "__main__":
    main()

