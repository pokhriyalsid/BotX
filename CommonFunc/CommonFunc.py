import netmiko
import os
import sys
def devicelogin(list):
    netconnect = netmiko.ConnectHandler(**list)
    # {'device_type':'cisco_ios' , 'host':IPList[num - 1], 'username':Username, 'password':Pwd, 'secret' : 'test'}

def devicelist(filepath):
    with open(filepath) as func2devicelist:
        devlist = func2devicelist.read()
        deviplist = []
        for items in devlist.splitlines():
            deviplist.append(items.split()[-1])
        return devlist.splitlines(), deviplist ## First we are returning the list where each element has the device ip and device name and 2nd we are only returning the device ip

def commandlist(filepath):
    with open(filepath) as cmd:
        cmdlist =  cmd.read().splitlines()
        return cmdlist
