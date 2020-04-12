## This is the main Robota script via which we will call the sub-scripts for different functions
## Test comment
import time
import sys
randomno = 1
def Displayonstart():
    print ("My Name is Robota and I can perform below tasks for you: ")
    print ("""1.) Manually copy the Device config's
    2.) Run commands on multiple Devices
    3.) Manually backup the Devices \n
    Apart from this I can also check for below data from my database:
    4.) Check that subnet is behind which device \n """)
    input1 = input("Type the function you want me to execute else type 9 to quit: \n")
    return int(input1)

randomno = 1
while True:
    input1 = Displayonstart()
    if randomno == 3:
        sys.exit("You were given many chances")
    if input1 == 9 :
        sys.exit("You choosed option 9... I quit")
    if input1 != 9 and input1 > 5 or input1 == 0 or type(input1) is not int :
        print ("2ry AgAiN I DoNt uDerstand U")
        randomno = randomno + 1
        continue
    else:
        break
