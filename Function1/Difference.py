## This module has 2 functions
## DiffinRunConfig will compare the changes between last 2 running config files saved by the Script
## CurrentDif() will login to the Device to check current run and will check any changes as compared to the last file saved by the Script.

import diffios
import os
import glob
import sys
import netmiko
import time
#import CopyDeviceConfig
sys.path.append(os.path.dirname(os.getcwd()))

from CommonFunc import CommonFunc
Username = 'test'
Pwd = 'test'

Ciscodevicelist, juniperdevicelist = CommonFunc.devicelist(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '\\Jsonfiles' + '\\DeviceList.json') ## Using os.path.realpath here instead of os.getcwd because this function will be called from Main.py and if we use getcwd the it will print the cwd of BotX.

RunconfigDirPath = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\" + "ScriptOutput" + "\\" + "RunningConfig"
Dirlist = os.listdir(RunconfigDirPath)  ## Here we are putting all the directories in the folder /Scriptoutput/RunningConfig/ in a list Dirlist.. This will be list of directories created after running config is copied


def DiffinRunConfig(): # This function will check for changes in the config periodically
    global RunconfigDirPath
    for dir in Dirlist:
        filepath = RunconfigDirPath + '\\' + dir
        list_of_files = glob.glob(filepath + "/*run.txt") ## This will return type list of all files ending with run.txt
        sortfilelist = sorted(list_of_files, key = os.path.getctime) ## Sorting files as per creation date
        try:
            oldfile = sortfilelist[-2]
            newfile = sortfilelist[-1]
        #    ignorefile = "ignore.txt"
        #    Diff = diffios.Compare(oldfile, newfile, ignorefile) ## Later will add ignore.txt to ignore irrelevant changes
            Diff = diffios.Compare(oldfile, newfile)
            with open(filepath + '\\' + 'Difference.txt', 'w+') as diffile:
                print ("Running config difference between {} and {}".format(newfile.split('\\')[-1], oldfile.split('\\')[-1]), file=diffile)
                print (Diff.delta(), file=diffile)
                print ('_'*40, file=diffile)
            #ignorefile.close()
        except IndexError:
            print('Not much files to compare')
        else:
            print("Difference Output saved in the designated folders")

def CurrentDif(): #This function will check changes in the config comparing last saved file via this script and the current device config
    input1 = input("Enter the Device Name for which you want to check the changes made as compared to Last Run: \n")
    randomno = 0
    for dir in Dirlist:
        if dir.lower() == input1.lower():  ## .lower() helps comparing string ignoring case sensitivity
            randomno = 1
            filepath = RunconfigDirPath + '\\' + dir
            list_of_files = glob.glob(filepath + "/*run.txt")
            sortfilelist = sorted(list_of_files, key = os.path.getctime)
            lastfile = sortfilelist[-1] ### This would be the lastfile

            for device in Ciscodevicelist:
                if device['Name'].lower() == input1.lower():
                    IP = (device['IP'])
                    netmikoobj = {'device_type':'cisco_ios' , 'host':IP, 'username':Username, 'password':Pwd}
                    latestoutput = CommonFunc.devicelogin_1(netmikoobj, ['terminal length 0', 'show running-config'])
                    if latestoutput == 'None':
                        sys.exit()
                    with open('CurrentR.txt', 'w+') as currentrun:
                        print(latestoutput, file=currentrun)
                    Diff = diffios.Compare(lastfile,'CurrentR.txt' )
                    print("Below is the difference between Current Config and config copied on {}".format(lastfile.split('\\')[-1]))
                    print(Diff.delta())


    if randomno == 0:
        print("Couldnt find the device data, Kindly check if Device Name is correct or its data is backed up via this Script")
