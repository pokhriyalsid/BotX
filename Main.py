 ## This is the main Robota script via which we will call the sub-scripts for different functions
import time
import sys
import subprocess
randomno = 1
def msg():
    print ("My Name is Robota and I can perform below tasks for you: ")
    print ("""1.) Manually copy the Device config's
2.) Run commands on multiple Devices
3.) Manually backup the Devices
    Apart from this I can also check for below data from my database:
4.) Check that subnet is behind which device \n """)
def Displayonstart():
#    msg()
    while True:
        subprocess.run('cls', shell = True)
        msg()
        try:
            input1 = int(input("Type the function you want me to execute else type 9 to quit: \n"))
        except ValueError:
            global randomno  ### Using global variable here
            if randomno == 3:
                sys.exit("I gave you many chances")
            print("Not an integer! Try again.")
            randomno = randomno + 1
            continue
        else:
            return input1
            break

while True:
    if randomno == 4:
        sys.exit("You were given many chances")
    #subprocess.run('cls', shell = True)
    input1 = Displayonstart()
    if input1 == 9 :
        sys.exit("You choosed option 9... I quit")
    if input1 != 9 and input1 > 5 or input1 == 0 or type(input1) is not int:
        if randomno < 3:
            print ("2ry AgAiN I DoNt uDerstand U")
        randomno = randomno + 1
        continue
    else:
        break
