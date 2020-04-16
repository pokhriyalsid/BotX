import json

with open("jsonex.json") as jsonfile:
#    print(type(jsonfile.read()))  #This is a string
    jsondict = json.loads(jsonfile.read())
    jsonlistcisco = jsondict['Cisco']
    for item in jsonlistcisco:
        print(item['Name'], item['IP'])

newName = input("Device Name: ")
newIP = input("Enter IP: ")

newitemdict = {'Name': newName, "IP": newIP}
jsonlistcisco.append(newitemdict)

#print(jsonlistcisco)
with open("jsonex.json", 'r+') as jsonfile:
    jsonfiledict = json.loads(jsonfile.read())
    jsonfiledict['Cisco'] = jsonlistcisco


    jsonfilestring = json.dumps(jsonfiledict, indent=2, sort_keys=True)
    jsonfile.seek(0)
    jsonfile.write(jsonfilestring)
