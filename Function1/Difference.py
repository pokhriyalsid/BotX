## Not using this

import diffios
import os
from GetIpFromFile import GetIpFromFile
import glob

DirList = GetIpFromFile() ## This function returns ip of all devices in the devicelist
                         ## But we can use it here because name of Directory would be equal to the ip of device

#print (DirList)
for dir in DirList:
    list_of_files = glob.glob(dir + "/*run.txt") # This will return list of file in the directory
    #print (list_of_files)
    #latestfile = sort(list_of_files, key=os.path.getctime)
    #print(sorted(list_of_files, key = os.path.getctime)) ## This will sort the files from oldest to newest
                                                        ## So for comparision we can select the last 2 new files
                                                        ## like [-1] would be last and [-2] second last

    sortfilelist = sorted(list_of_files, key = os.path.getctime)
    try:
        oldfile = sortfilelist[-2]
        newfile = sortfilelist[-1]
        ignorefile = "ignore.txt"
        Diff = diffios.Compare(oldfile, newfile, ignorefile)
        print (Diff.delta())
        print ('_'*40)
        #ignorefile.close()
    except IndexError:
        print('Not much files to compare')
