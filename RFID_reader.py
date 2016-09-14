import json
import os

print "Scan ID card"
UID = raw_input()

print "Scan items, type 'exit' to quit"
items = []
itemID = raw_input()
while itemID != "exit":
    items.append(itemID)
    itemID = raw_input()

object = [{"UID": UID, "items": items}]
JSON_obj = json.dumps(object)
print JSON_obj

host_url = "google.com"
print os.system("ping -c 1 " + host_url)
# 0 = up
