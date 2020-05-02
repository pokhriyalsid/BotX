import netmiko
import os
import sys
import json
result = 'nil'
def devicelogin(list, cmdlist):
    try:
        netconnect = netmiko.ConnectHandler(**list)
    except netmiko.ssh_exception.NetmikoTimeoutException:
        print("Cant Login to Device {}".format(list['host']))
    except netmiko.ssh_exception.NetMikoAuthenticationException:
        print("Credentials not working for {}".format(list['host']))
    else:
        netconnect.send_command('terminal length 0')
        for cmds in cmdlist:
            output = netconnect.send_command(cmds)
            filepath = os.path.dirname(os.getcwd()) + '\\' + "ScriptOutput" + '\\' + list['host'] + '.txt'
            with open(filepath, 'a+') as file:
                file.write(cmds)
                print(' ', file= file)
                file.write(output)
                print(' ', file= file)
                print('************************', file = file)


    # {'device_type':'cisco_ios' , 'host':IPList[num - 1], 'username':Username, 'password':Pwd, 'secret' : 'test'}

def devicelist(filepath):       ##We would be using json files and will pass them here when calling this function
    with open(filepath) as func2devicelist:
        jsonstring = func2devicelist.read()
        jsondict = json.loads(jsonstring)## func2devicelist.read() is json representation hence using loads() to convert it into a json dictionary
        ciscodevicelist = jsondict['Cisco']     ##These would be a list
        juniperdevicelist = jsondict['Juniper']
        return ciscodevicelist, juniperdevicelist

def commandlist(filepath, devicevendor):##filepath variable would be json file and devicevendor is as the name says
    with open(filepath) as cmd:
        cmddictjson = json.loads(cmd.read()) ## This will have all the commands of Cisco and Juniper as well
        if devicevendor == "Cisco":
            cmdlist = cmddictjson['Cisco']
            return cmdlist
        if devicevendor == "Juniper":
            cmdlist = cmddictjson['Juniper']
            return cmdlist

def devicelogin_1(list, cmdlist):
    try:
        netconnect = netmiko.ConnectHandler(**list)
    except netmiko.ssh_exception.NetmikoTimeoutException:
        print("Cant Login to Device {}".format(list['host']))
        return 'None'
    except netmiko.ssh_exception.NetMikoAuthenticationException:
        print("Credentials not working for {}".format(list['host']))
        return 'None'
    else:
    #    return netconnect
        output = ''
        for cmds in cmdlist:
            output = output + netconnect.send_command(cmds)
        return output
