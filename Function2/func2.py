# The module has below functions
# Mainfunc2() : This is the main function which calls other function based on user input
# devicelogin() : This function is called inside Mainfunc2_1 and used to create threads
# Mainfunc2_1() : This function initiates the threads
# deviceloginCustom() : this would be used in customcmds function and used to create threads
# customcmds() : Function to run custom commands to mentioned list of devices

import netmiko
import sys
import os
import threading
import time
import pandas
import subprocess

sys.path.append(os.path.dirname(os.getcwd())) ## Modifying sys.path in order to use CommonFunc package
from CommonFunc import CommonFunc # from CommonFunc package importing CommonFunc module
Username = 'test'
Pwd = 'test'

#cmds = CommonFunc.commandlist(os.path.dirname(os.getcwd()) + '\\Jsonfiles' + '\\func2commands.json', 'Juniper') ## commandlist function excepts the path of the file

Ciscodevicelist, juniperdevicelist = CommonFunc.devicelist(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '\\Jsonfiles' + '\\DeviceList.json')
## Ciscodevicelist and juniperdevice list gives both name and ip of the device
Ciscocommandlist = CommonFunc.commandlist(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '\\Jsonfiles' + '\\func2commands.json', 'Cisco')
Junipercommandlist = CommonFunc.commandlist(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '\\Jsonfiles' + '\\func2commands.json', 'Juniper')
def Mainfunc2():
    print("Below are commands I am going to run")
    for cmds in Ciscocommandlist:
        print('-> ' + cmds)
    print("\n")
    print("Below is the list of device I have ----------------------")
    for device in Ciscodevicelist:
        print(device)
    input2 = input("Enter 1 if you want to run the above commands to the saved devices or press 2 if you want edit the commands or device list \n")
    if input2 == str(1):
        Mainfunc2_1()
    elif input2 == str(2):
        customcmds()
    else:
        print("You didnt enter 1 and neither 2")

def devicelogin(list, cmdlist):
    try:
        netconnect = netmiko.ConnectHandler(**list)
    except netmiko.ssh_exception.NetmikoTimeoutException:
        print("Cant Login to Device {}".format(list['host']))
    except netmiko.ssh_exception.NetMikoAuthenticationException:
        print("Credentials not working for {}".format(list['host']))
    else:
        filepath = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '\\' + "ScriptOutput" + '\\' + list['host'] + '.txt'
        file = open(filepath, 'a+')
        for cmds in cmdlist:
            output = netconnect.send_command(cmds)
            print('************************', file = file)
            file.write(cmds)
            print(' ', file= file)
            file.write(output)
            print(' ', file= file)
        #    print('************************', file = file)

        print("Script Ended at {}".format(time.asctime()), file = file)
        print('************************', file = file)
        print('************************', file = file)
        print('\n'*3, file = file)
        file.close()

def Mainfunc2_1():
    cisconetmikoobj = []  ## This list will have the parameters in the format we pass to netmiko ConnectHandler
    if len(Ciscodevicelist) > 0:
        for items in Ciscodevicelist:
            cisconetmikoobj.append({'device_type':'cisco_ios' , 'host':items['IP'], 'username':Username, 'password':Pwd})
        ThreadlistCisco = []
        n = 1
        for items in cisconetmikoobj:
            ThreadlistCisco.append(threading.Thread(target=devicelogin, name= 'Thread' + str(n), args = [items, Ciscocommandlist]))
            n = n+ 1
        n = 0
        for elem in ThreadlistCisco:
            #    print("Logging to {}".format(Ciscodevicelist[n]['Name']))
            elem.start()   ### Note try and except exception statements are to be added in CommonFunc module, they are not working if added here
            n = n + 1


    if len(Ciscodevicelist) == 0:
        print("There are no Cisco device mentioned in the file to run commands on")

def deviceloginCustom(list, cmdlist):
    try:
        netconnect = netmiko.ConnectHandler(**list)
    except netmiko.ssh_exception.NetmikoTimeoutException:
        print("Cant Login to Device {}".format(list['host']))
    except netmiko.ssh_exception.NetMikoAuthenticationException:
        print("Credentials not working for {}".format(list['host']))
    else:
        filepath = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '\\' + "ScriptOutput" + '\\'  + "Function2"  + '\\' + list['host'] + '.txt'
        file = open(filepath, 'w+')
        for cmds in cmdlist:
            output = netconnect.send_command(cmds)
            print('************************', file = file)
            file.write(cmds)
            print(' ', file= file)
            file.write(output)
            print(' ', file= file)
        #    print('************************', file = file)

        print("Script Ended at {}".format(time.asctime()), file = file)
        print('************************', file = file)
        print('************************', file = file)
        print('\n'*3, file = file)
        file.close()

def customcmds():
    print("Edit the Excel files just opened on your Screen and save it")
    print("""Add the Device Name and Commands in that Excel which you want to run and after that type 'Done' or else type 'Exit'
    """)
    filepath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))  + '\\Jsonfiles' + '\\' + 'CustomDevice.xlsx'
    os.startfile(filepath)
    time.sleep(2)
    n = 1
    while True:
        input1 = input()
        if input1 == 'Done' or input1 == 'done':
            print("Great Job")
            break
        elif input1 == 'Exit' or input1 == 'exit':
            sys.exit()
        else:
            print("You didnt enter Done or exit. 1 more try. Type exit or Done")
            if n == 2:
                sys.exit()
            else:
                n = n + 1
    subprocess.run('cls', shell = True)
    excel_devicename = pandas.read_excel(filepath, sheet_name='DeviceList', skiprows = 1)
    excel_cmd = pandas.read_excel(filepath, sheet_name='Commands', skiprows = 1)
    devicedict = dict(zip(excel_devicename.Name, excel_devicename.IP))
    cmdlist = ['terminal length 0']
    cmdlist= cmdlist + excel_cmd.Command.to_list()

    print("So below are the list of commands you want to run")
    for cmd in cmdlist:
        print(cmd)
    print("And below are the list of Devices on which you want to run above command")
    print(devicedict)
    input1 = input("To continue type 'Go' and press enter: \n")
    if input1 != 'Go' and input1 != 'go':
        sys.exit("You type {} and not 'Go' so quiting the program".format(input1))

    threadlist = []
    n = 1
    for deviceip in devicedict.values():
        netmikoobj = {'device_type':'cisco_ios' , 'host':deviceip, 'username':Username, 'password':Pwd}
        threadlist.append(threading.Thread(target=deviceloginCustom, name= 'Thread' + str(n), args = [netmikoobj, cmdlist]))
        n = n + 1
    for threads in threadlist:
        threads.start()
