import os
import json
import netmiko
import time
import sys
import threading
sys.path.append(os.path.dirname(os.getcwd()))

from CommonFunc import CommonFunc

Username = 'test'
Pwd = 'test'




x = time.asctime()    # x is a string object returned
timestring = x.split()

def devicelogin(devicelist):
    try:
        netconnect = netmiko.ConnectHandler(**devicelist)
    except netmiko.ssh_exception.NetmikoTimeoutException:
        print("Cant Login to Device {}".format(devicelist['host']))
    except netmiko.ssh_exception.NetMikoAuthenticationException:
        print("Credentials not working for {}".format(devicelist['host']))
    else:
        netconnect.send_command("terminal length 0")
        runconfig = netconnect.send_command("show running-config")
        try :
            FolderName = os.path.dirname(os.getcwd()) + '\\' + 'ScriptOutput' + '\\' + 'RunningConfig' + '\\'+ devicelist['host']
            os.mkdir(FolderName) ## This will create a folder with name of the Router
            ## This code is under try to catch exception if folder already exists
        except FileExistsError:
            pass
        pathrun = FolderName + "\\" + devicelist['host'] + "_" + timestring[2] + "_" + timestring[1] + "_" +  timestring[3].split(':')[0] + "Hour" + "_" + "run.txt"
        with open(pathrun, 'w+') as outputfile:
            outputfile.write(runconfig)

Ciscodevicelist, juniperdevicelist = CommonFunc.devicelist(os.path.dirname(os.getcwd()) + '\\Jsonfiles' + '\\DeviceList.json')
cisconetmikoobj = []
if len(Ciscodevicelist) == 0:
    print("There are no Cisco device mentioned in the file to run commands on")
else:
    for items in Ciscodevicelist:
        cisconetmikoobj.append({'device_type':'cisco_ios' , 'host':items['IP'], 'username':Username, 'password':Pwd})
    n = 1
    ciscothreadlist = []
    for items in cisconetmikoobj:
        ciscothreadlist.append(threading.Thread(target=devicelogin, name = 'Thread'+ str(n), args =[items]))

    for threads in ciscothreadlist:
        threads.start()
