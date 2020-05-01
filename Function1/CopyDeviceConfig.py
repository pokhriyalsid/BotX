# This script is to be scheuled every Sunday . Use Linux Crontab for this.
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
        otheroutput1 = 'show cdp nei' + '\n' + netconnect.send_command('show cdp nei')
        otheroutput2 = 'show ip int brief | ex unas' + '\n' + netconnect.send_command('show ip int brief | ex unas')
        msg = "Output was collected at {}".format(time.asctime())
        finalotheroutput = msg + '\n' + '\n' + otheroutput1 + '\n' + '**'*20 + '\n' + otheroutput2
        try :
            FolderName = os.path.dirname(os.getcwd()) + '\\' + 'ScriptOutput' + '\\' + 'RunningConfig' + '\\'+ DeviceN

            os.mkdir(FolderName) ## This will create a folder with name of the Router
            ## This code is under try to catch exception if folder already exists
        except FileExistsError:
            pass
        pathrun = FolderName + "\\" + DeviceN + "_" + timestring[2] + "_" + timestring[1] + "_" +  timestring[3].split(':')[0] + "Hour" + "_" + "run.txt"
        pathother = FolderName + "\\" + DeviceN + "_" + "OtherOutput.txt"
        with open(pathrun, 'w+') as outputfile:
            outputfile.write(runconfig)
        with open(pathother, 'w+') as otherfile:
            otherfile.write(finalotheroutput)

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
    ##Below is old code , keeping it safe if required later
#    for threads in ciscothreadlist:
#        if (n+1)%5 == 0:            ## This will make sure if more than 5 devices are there is the device list
#            threads.join()      ## then after the 5th device there is some pause in the code
#            while True:
#                no = 1
#                if ciscothreadlist[n].is_alive():
#                    print("Still working on {}".format(Ciscodevicelist[no]['Name']))
#        threads.start()
#        n = n + 1

    for threads in ciscothreadlist:
        if (n+1)%5 == 0:
            threads.start()     ## This will make sure if more than 5 devices are there in the device list
            threads.join()      ## then the script waits for the 5th device to complete
                                ## And will also check if commands have exexuted on the last 5 devices
            no = 1              ## as per below while loop
            while True:
                if ciscothreadlist[n].is_alive():
                    print("Still working on {}".format(Ciscodevicelist[n]['Name']))
                    time.sleep(2)
                    if no == 15:  ## So if we have waited more than 30 sec then exit the function
                        sys.exit("Exiting the function")
                    no = no + 1
                    continue
                if ciscothreadlist[n-1].is_alive():
                    print("Still working on {}".format(Ciscodevicelist[n-1]['Name']))
                    time.sleep(2)
                    if no == 15:  ## So if we have waited more than 30 sec then exit the function
                        sys.exit("Exiting the function")
                    no = no + 1
                    continue
                if ciscothreadlist[n-2].is_alive():
                    print("Still working on {}".format(Ciscodevicelist[n-2]['Name']))
                    time.sleep(2)
                    if no == 15:  ## So if we have waited more than 30 sec then exit the function
                        sys.exit("Exiting the function")
                    no = no + 1
                    continue
                if ciscothreadlist[n-3].is_alive():
                    print("Still working on {}".format(Ciscodevicelist[n-3]['Name']))
                    time.sleep(2)
                    if no == 15:  ## So if we have waited more than 30 sec then exit the function
                        sys.exit("Exiting the function")
                    no = no + 1
                    continue
                if ciscothreadlist[n-4].is_alive():
                    print("Still working on {}".format(Ciscodevicelist[n-4]['Name']))
                    time.sleep(2)
                    if no == 15:  ## So if we have waited more than 30 sec then exit the function
                        sys.exit("Exiting the function")
                    no = no + 1
                    continue
                else:
                    break
            continue ### This continue is so that below threads.start() wont come in script for the 5th item
        threads.start() ## as it is already started
        n = n + 1
