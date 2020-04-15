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

cmds = CommonFunc.commandlist(os.getcwd() + '\\func2commands.txt') ## commandlist function excepts the path of the file

print(cmds)
