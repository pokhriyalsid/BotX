#The Function performs below functions:
# Login to all devices and checks which Vlan, ip address subnets are behind them

# It will take the list of devices from the file input device which is created using a specific format
# This function should also ask twice if you want to run the command.
# It should also show the list of commands before executing
# It should only run show commands

import netmiko
import sys
import os
import threading

sys.path.append(os.path.dirname(os.getcwd())) ## Modifying sys.path in order to use CommonFunc package

from CommonFunc import CommonFunc # from CommonFunc package importing CommonFunc module
Username = 'test'
Pwd = 'test'

#cmds = CommonFunc.commandlist(os.path.dirname(os.getcwd()) + '\\Jsonfiles' + '\\func2commands.json', 'Juniper') ## commandlist function excepts the path of the file

Ciscodevicelist, juniperdevicelist = CommonFunc.devicelist(os.path.dirname(os.getcwd()) + '\\Jsonfiles' + '\\DeviceList.json')
## Ciscodevicelist and juniperdevice list gives both name and ip of the device
Ciscocommandlist = CommonFunc.commandlist(os.path.dirname(os.getcwd()) + '\\Jsonfiles' + '\\func2commands.json', 'Cisco')
Junipercommandlist = CommonFunc.commandlist(os.path.dirname(os.getcwd()) + '\\Jsonfiles' + '\\func2commands.json', 'Juniper')


def devicelogin(list, cmdlist):
    try:
        netconnect = netmiko.ConnectHandler(**list)
    except netmiko.ssh_exception.NetmikoTimeoutException:
        print("Cant Login to Device {}".format(list['host']))
    except netmiko.ssh_exception.NetMikoAuthenticationException:
        print("Credentials not working for {}".format(list['host']))
    else:
        for cmds in cmdlist:
            output = netconnect.send_command(cmds)
            filepath = os.path.dirname(os.getcwd()) + '\\' + "ScriptOutput" + '\\' + list['host'] + '.txt'
            with open(filepath, 'a+') as file:
                file.write(cmds)
                print(' ', file= file)
                file.write(output)
                print(' ', file= file)
                print('************************', file = file)
# Here later i will add code to update user that which commands will be run on which devices and also if they want to update the command list or devicelist then they will be redirected to a different function.
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
