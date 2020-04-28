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

def devicelogin(devicelist, DeviceN):
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
            FolderName = os.path.dirname(os.getcwd()) + '\\' + 'ScriptOutput' + '\\' + 'RunningConfig' + '\\'+ DeviceN

            #devicelist['host']
            os.mkdir(FolderName) ## This will create a folder with name of the Router
            ## This code is under try to catch exception if folder already exists
        except FileExistsError:
            pass
        pathrun = FolderName + "\\" + DeviceN + "_" + timestring[2] + "_" + timestring[1] + "_" +  timestring[3].split(':')[0] + "Hour" + "_" + "run.txt"
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
        ciscothreadlist.append(threading.Thread(target=devicelogin, name = 'Thread'+ str(n), args =[items, Ciscodevicelist[n-1]['Name']]))
        n = n + 1

    n = 0
    for threads in ciscothreadlist:
        if (n+1)%5 == 0:            ## This will make sure if more than 5 devices are there is the device list
            threads.join()      ## then after the 5th device there is some pause in the code
            while True:
                no = 1
                if ciscothreadlist[n].is_alive():
                    print("")

        threads.start()
        n = n + 1
