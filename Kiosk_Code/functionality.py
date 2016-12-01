""" provides funtionality for the GUI to interface with database """
import sys
import time
import requests

# global variables
STORE_ID = 1
KIOSK_TYPE = None
USER_ID = None
ITEMS = {}
RESERVATIONS = {}
CHECKED_ITEMS = []

# pylint: disable=W0603

def set_kiosk_type(in_out):
    """ sets the kiosk type to either in or out """
    global KIOSK_TYPE
    KIOSK_TYPE = in_out


def set_user_id(user_id):
    """ validates user id and returns name """
    # TODO: implement user id validation
    global USER_ID
    USER_ID = user_id
    return ("Unkown user", True)


def verify_item(tag_id):
    """ verfiy that an item can be checked in or out, return name and status """
    # ensure tag_id is an integer
    try:
        tag_id = int(tag_id)
    except ValueError:
        return ("Invalid item", False)

    # ensure tag_id is a valid tag_id
    if tag_id not in ITEMS.keys():
        return ("Invalid item", False)

    # ensure item has not already been checked in this cycle
    if tag_id in CHECKED_ITEMS:
        return("Item already scanned", False)
    # ensure item is available to check in
    if KIOSK_TYPE == "in":
        if tag_id not in RESERVATIONS.keys():
            return ("Item is already checked in", False)
    # ensure item is available to check out
    elif KIOSK_TYPE == "out":
        if tag_id in RESERVATIONS.keys():
            return ("Item is already checked out", False)
    else:
        raise ValueError("invalid value for KIOSK_TYPE: %s" % KIOSK_TYPE)

    # item is availible to check in or out
    CHECKED_ITEMS.append(tag_id)
    return (ITEMS[tag_id]["name"], True)


def send_request():
    """ PURPOSE: sends get request to server, checking items either in or out """
    results = {"success": [], "fail": []}
    global USER_ID
    if not USER_ID:
        USER_ID = 0
    else:
        USER_ID = int(USER_ID)
    if not CHECKED_ITEMS:
        return ("No items to check", True)

    # get request (sends data to database)
    req_str = "http://api.checkmeout.us.to/kiosk/check%s?SID=%d&UID=%d&items=[%s]"
    response = requests.get(req_str % (KIOSK_TYPE, STORE_ID, USER_ID, ",".join(map(str, CHECKED_ITEMS))))

    # check response (get data from database)
    if response.status_code == 200:
        response = response.json()
        try:
            # response differes based on checking operation
            #   checking IN response: [... {'items_updated': []}, ...]
            #   checking OUT response: [... {'items_saved': []}, ...]
            if KIOSK_TYPE == "in":
                success_key = "items_updated"
            else:
                success_key = "items_saved"

            for item in response[success_key]:
                results["success"].append(item["item_tag"])
            for item in response["items_failed"]:
                if "item_name" in item.keys():
                    # valid tag_id but invalid check operation
                    results["fail"].append(item["item_tag"])
                else:
                    # invalid tag_id
                    results["fail"].append(item["item_tag"])
        except KeyError:
            return ("Problem parsing: %r" % response, False)

        # check if all items were successfully checked
        if len(CHECKED_ITEMS) == len(results["success"]):
            return ("All items succeeded", True)
        else:
            return ("Some items failed", False)

    else:
        return ("ERROR: %d" % response.status_code, False)


def get_items_from_db():
    """
    PURPOSE: query the database for all the items and return them as a dict
    RETURNS: a dict with the tag_id as the key
    """
    item_dict = {}

    response = requests.get("http://api.checkmeout.us.to/kiosk/item")
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


def sync_database(update_items=False):
    """ queries the database to update ITEMS and RESERVATIOINS dicts """
    global ITEMS, RESERVATIONS, CHECKED_ITEMS

    if update_items:
        ITEMS = get_items_from_db()
    RESERVATIONS = get_reservations_from_db(ITEMS)
    CHECKED_ITEMS = []
