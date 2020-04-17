#The Function performs below functions:
# Login to all devices and checks which Vlan, ip address subnets are behind them

# It will take the list of devices from the file input device which is created using a specific format
# This function should also ask twice if you want to run the command.
# It should also show the list of commands before executing
# It should only run show commands

import netmiko
import sys
import os

sys.path.append(os.path.dirname(os.getcwd())) ## Modifying sys.path in order to use CommonFunc package

from CommonFunc import CommonFunc # from CommonFunc package importing CommonFunc module
Username = 'test'
Pwd = 'test'

#cmds = CommonFunc.commandlist(os.path.dirname(os.getcwd()) + '\\Jsonfiles' + '\\func2commands.json', 'Juniper') ## commandlist function excepts the path of the file

Ciscodevicelist, juniperdevicelist = CommonFunc.devicelist(os.path.dirname(os.getcwd()) + '\\Jsonfiles' + '\\DeviceList.json')
## Ciscodevicelist and juniperdevice list gives both name and ip of the device
Ciscocommandlist = CommonFunc.commandlist(os.path.dirname(os.getcwd()) + '\\Jsonfiles' + '\\func2commands.json', 'Cisco')
Junipercommandlist = CommonFunc.commandlist(os.path.dirname(os.getcwd()) + '\\Jsonfiles' + '\\func2commands.json', 'Juniper')

# Here later i will add code to update user that which commands will be run on which devices and also if they want to update the command list or devicelist then they will be redirected to a different function.
cisconetmikodictobj = []  ## This list will have the parameters in the format we pass to netmiko ConnectHandler
if len(Ciscodevicelist) > 0:
    for items in Ciscodevicelist:
        cisconetmikodictobj.append({'device_type':'cisco_ios' , 'host':items['IP'], 'username':Username, 'Password':Pwd, 'secret' : 'test'})
if len(Ciscodevicelist) == 0:
    print("There are no Cisco device mentioned in the file to run commands on")
