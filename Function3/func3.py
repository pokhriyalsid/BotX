import os
import time
import sys
import netmiko
import subprocess
Username = 'test'
Pwd = 'test'
import threading
import socket

## Send few cmds and then some shut command and then few other commands  and see whats the result
## Add some show command at the end of the config commands to verify if there is any return in output. If this cmd doesnt return anything that send a message on the console that check the device and revert it to old config + delete EEM, SLA and track
## if device lose access in between but the EEM script brought it back then stop the program to execute other commands


def devicelogin(list, cmdlist):
    try:
        netconnect = netmiko.ConnectHandler(**list)
    except netmiko.ssh_exception.NetmikoTimeoutException:
        print("Cant Login to Device {}".format(list['host']))
        sys.exit()
    except netmiko.ssh_exception.NetMikoAuthenticationException:
        print("Credentials not working for {}".format(list['host']))
        sys.exit()
    else:
    #    return netconnect
        output = ''
        outputr = ''
        cmdssucceded = []
        for cmds in cmdlist:
            try:
                output = netconnect.send_command(cmds,  auto_find_prompt=False, strip_command = False)
            except OSError:
                print("Seems I lost access to the Device and rollback script also coudn't bring the access to the device back. Kindly check manually")
                cmdssucceded.append(cmds)
                if len(cmdssucceded) > 0:
                    print("Few Command's which were pushed are below: \n")
                    for cmd in cmdssucceded:
                        print(cmd)
                sys.exit()
            #print(output)
            outputr = outputr + '\n' + output
            if '^' in output:
                print("'{}' command is not working on the device so ignoring the rest of the commands".format(cmds))
                if len(cmdssucceded) > 0:
                    print("Few Command's which were pushed are below: \n")
                    for cmd in cmdssucceded:
                        print(cmd)
                sys.exit()
            elif 'Incomplete command' in output:
                print("Incomplete command '{}'".format(cmds))
                if len(cmdssucceded) > 0:
                    print("Few Command's which were pushed are below: \n")
                    for cmd in cmdssucceded:
                        print(cmd)
                sys.exit()
            else:
                cmdssucceded.append(cmds)
                eemstats = netconnect.send_command('do show event manager statistics policy | in rollbackbotx')
            #    print (eemstats.split()[2]) ## This will print EEM script count and if value is not 0 then script has executed
                if int(eemstats.split()[2]) > 0 :
                    print("Rollback script has executed that means SLA has failed")
                    print("Few Command's which were pushed are below. Kindly check if these commands needs to be removed if not mentioned in rollback script: \n")
                    for cmd in cmdssucceded:
                        print(cmd)
                    netconnect.send_command('no event manager applet rollbackbotx', auto_find_prompt=False)
                    netconnect.send_command('no track 192', auto_find_prompt=False)
                    netconnect.send_command('no ip sla 192', auto_find_prompt=False)
                    sys.exit()
                #print(netconnect.is_alive())


        #return outputr
        with open(filepath + '\\' + 'configpushed.txt', 'w+') as configfile:
            configfile.write(outputr)
        print("Output of operation is saved in configpushed.txt.. Will open it now")
        os.startfile(filepath + '\\configpushed.txt')
        return netconnect
    #    print("Command pushed : {}".format(cmdssucceded))

def EEMfn():
    rollback = open(filepath + '\\rollback.txt')
    content = rollback.read().splitlines()
    rollback.close()

    eemscript = ['event manager applet rollbackbotx', 'event track 192 state down', 'action 1.1 cli command "enable"', 'action 1.2 cli command "config t"']
    n = 3
    for cmd in content:
        cmdstr = 'action 1.' + str(n) + ' cli command ' + '"{}"'.format(cmd)
        eemscript.append(cmdstr)
        n = n + 1
    eem = open(filepath + '\\EEM.txt', 'w+')
    print (eemscript, file=eem)
    eem.close()
    return eemscript


def slafn(list):
    slacmds = ['ip sla 192', 'icmp-echo ' + slaip, 'frequency 5' ,'ip sla schedule 192 start-time now', 'track 192 ip sla 192' ]
    try:
        netconnect = netmiko.ConnectHandler(**list)
    except netmiko.ssh_exception.NetmikoTimeoutException:
        print("Cant Login to Device {}".format(list['host']))
        sys.exit()
    except netmiko.ssh_exception.NetMikoAuthenticationException:
        print("Credentials not working for {}".format(list['host']))
        sys.exit()
    else:
        print("Logged in to the Device")
        eemexist = netconnect.send_command('show event manager statistics policy | in rollbackbotx') ## This is to check if EEM script already exists
        for items in eemexist.splitlines():
            if items.split()[-1] == 'rollbackbotx':
                sys.exit('Check EEM script with name rollbackbotx already exists, so not proceeding further')
        slexist = netconnect.send_command('show ip sla configuration 192')
        for items in slexist.splitlines():
            if 'Entry number: 192' in items:
                sys.exit('ip sla 192 already exists kindly check, not proceeding with the Script')
        netconnect.send_config_set(slacmds)
        print("Sleeping for 10 sec for the SLA to change the status")
        #time.sleep(10)
        output = netconnect.send_command('show track 192 | in State')
        print("Sla status before the script is {}".format(output))
        if 'Down' in output:
            print("SLA status is down even before the change, Do you stil want to continue")
            no = 1
            while True:
                input5 = input("Enter Yes or no: \n")
                if input5 == 'No' or input5 == 'no':
                    print("Removing the ip sla commands")
                    netconnect.send_config_set(['no track 192 ip sla 192', ' no ip sla 192'])
                    sys.exit("Exiting the Code as requested")
                elif input5 == 'Yes' or input5 == 'yes':
                    print("Proceeding further")
                    eemscript = EEMfn()
                    print("Now will send EEM script")
                    netconnect.send_config_set(eemscript)
                    outputeem = netconnect.send_command('show run | section event')
                    print("Output of event Script is below:")
                    print(outputeem)
                    input("Enter to continue")
                    break
                else:
                    if no == 3:
                        sys.exit("Too Many attempts")
                    print("You didnt enter Yes or No")
                    no = no + 1
        else:
            while True:
                input5 = input("SLA status is up so do you want to proceed further, Enter Yes or No :\n")
                if input5 == 'No' or input5 == 'no':
                    print("Removing the ip sla commands")
                    netconnect.send_config_set(['no track 192 ip sla 192', ' no ip sla 192'])
                    sys.exit("Exiting the Code as requested")
                elif input5 == 'Yes' or input5 == 'yes':
                    print("Proceeding further")
                    break
                else:
                    if no == 3:
                        sys.exit("Too Many attempts")
                    print("You didnt enter Yes or No")
                    no = no + 1
            eemscript = EEMfn()
            print("Now will send EEM script")
            netconnect.send_config_set(eemscript)
            outputeem = netconnect.send_command('show run | section event')
            print("Output of event Script is below:")
            print(outputeem)
            input("Enter to continue")
            netconnect.disconnect()


def func3():
    print("""A Folder will open in your Screen. Kindly fill the 2 notepad files as below:
    config.txt -> Enter the config here which you want to pushed
    rollback.txt -> Enter the rollback plan here
    Leave the files empty if you dont want to run anything""")
    input("Check Anyconnect VPN should not be connected")

    global filepath
    filepath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))  + '\\Jsonfiles' + '\\Function3Files'
    #filepath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))  + '\\Jsonfiles' + '\\' + 'Function3config.txt'
    time.sleep(1)
    os.startfile(filepath)

    input1 = input("Review all 3 files and type 'Go' to proceed or 'Exit' and press enter: \n")
    if input1 == 'exit' or input1 == 'Exit':
        sys.exit('Exiting the program as requested')
    if input1 == 'Go' or input1 == 'go':
        pass
    elif input1 != 'go' and input1 != 'Go'  and input1 != 'Exit' and input1 != 'exit':
        sys.exit('Not sure what you typed')
    global deviceip
    deviceip = input("Enter the Device ip to which you want to push the config: \n")
    subprocess.run('cls', shell = True)
    print("Working on {}".format(deviceip))

    global slaip
    slaip = input("Type the ip address you want to ping. Rollback script will be pushed if SLA fails: \n")
    global netmikoobj
    netmikoobj = {'device_type':'cisco_ios' , 'host': deviceip, 'username':Username, 'password':Pwd}


    ## Later add code here to validate the ip
    slafn(netmikoobj)


    with open(filepath + '\\' + 'config.txt') as file:
        configcmdlist = file.read().splitlines()
    #print(configcmdlist)

    nc = devicelogin(netmikoobj, configcmdlist)
    print("Script Completed")

    ## Below we are deleting the track, ip sla and event
    nc.send_command('no event manager applet rollbackbotx', auto_find_prompt=False)
    nc.send_command('no track 192', auto_find_prompt=False)
    nc.send_command('no ip sla 192', auto_find_prompt=False)


func3()
