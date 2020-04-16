import netmiko
import os
import sys
import json
def devicelogin(list):
    netconnect = netmiko.ConnectHandler(**list)
    # {'device_type':'cisco_ios' , 'host':IPList[num - 1], 'username':Username, 'password':Pwd, 'secret' : 'test'}

def devicelist(filepath):       ##We would be using json files and will pass them here when calling this function
    with open(filepath) as func2devicelist:
        devlist = func2devicelist.read()  ## func2devicelist.read() is json representation hence using loads() to convert it into a json dictionary
        deviplist = []
        for items in devlist.splitlines():
            deviplist.append(items.split()[-1])
        return devlist.splitlines(), deviplist ## First we are returning the list where each element has the device ip and device name and 2nd we are only returning the device ip

def commandlist(filepath, devicevendor):##filepath variable would be json file and devicevendor is as the name says
    with open(filepath) as cmd:
        cmddictjson = json.loads(cmd.read()) ## This will have all the commands of Cisco and Juniper as well
        if devicevendor == "Cisco":
            cmdlist = cmddictjson['Cisco']
            return cmdlist
        if devicevendor == "Juniper":
            cmdlist = cmddictjson['Juniper']
            return cmdlist
