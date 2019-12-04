# 19 July 2014
# 08 Dec 2016 - updated for Python3

# in case any of this upsets Python purists it has been converted from an equivalent JRuby program

# this is designed to work with ... ArduinoPC2.ino ...

# the purpose of this program and the associated Arduino program is to demonstrate a system for sending
#   and receiving data between a PC and an Arduino.

# The key functions are:
#    sendToArduino(str) which sends the given string to the Arduino. The string may
#                       contain characters with any of the values 0 to 255
#
#    recvFromArduino()  which returns an array.
#                         The first element contains the number of bytes that the Arduino said it included in
#                             message. This can be used to check that the full message was received.
#                         The second element contains the message as a string


# the overall process followed by the demo program is as follows
#   open the serial connection to the Arduino - which causes the Arduino to reset
#   wait for a message from the Arduino to give it time to reset
#   loop through a series of test messages
#      send a message and display it on the PC screen
#      wait for a reply and display it on the PC

# to facilitate debugging the Arduino code this program interprets any message from the Arduino
#    with the message length set to 0 as a debug message which is displayed on the PC screen

# the message to be sent to the Arduino starts with < and ends with >
#    the message content comprises a string, an integer and a float
#    the numbers are sent as their ascii equivalents
#    for example <LED1,200,0.2>
#    this means set the flash interval for LED1 to 200 millisecs
#      and move the servo to 20% of its range

# receiving a message from the Arduino involves
#    waiting until the startMarker is detected
#    saving all subsequent bytes until the end marker is detected

# NOTES
#       this program does not include any timeouts to deal with delays in communication
#
#       for simplicity the program does NOT search for the comm port - the user must modify the
#         code to include the correct reference.
#         search for the lines
#               serPort = "/dev/ttyS80"
#               baudRate = 9600
#               ser = serial.Serial(serPort, baudRate)
#


# =====================================

#  Function Definitions

# =====================================

def sendToArduino(sendStr):
    ser.write(sendStr.encode('utf-8'))  # change for Python3


# ======================================

def recvFromArduino():
    global startMarker, endMarker

    ck = ""
    x = "z"  # any value that is not an end- or startMarker
    byteCount = -1  # to allow for the fact that the last increment will be one too many

    # wait for the start character
    while ord(x) != startMarker:
        x = ser.read()

    # save data until the end marker is found
    while ord(x) != endMarker:
        if ord(x) != startMarker:
            ck = ck + x.decode("utf-8")  # change for Python3
            byteCount += 1
        x = ser.read()

    return (ck)


# ============================

def waitForArduino():
    # wait until the Arduino sends 'Arduino Ready' - allows time for Arduino reset
    # it also ensures that any bytes left over from a previous message are discarded

    global startMarker, endMarker

    msg = ""
    while msg.find("Arduino is ready") == -1:

        while ser.inWaiting() == 0:
            pass

        msg = recvFromArduino()

        print(msg)  # python3 requires parenthesis
        print()


# ======================================

def runTest(td):
    numLoops = len(td)
    waitingForReply = False

    n = 0
    while n < numLoops:
        teststr = td[n]

        if waitingForReply == False:
            sendToArduino(teststr)
            print("Sent from PC -- LOOP NUM " + str(n) + " TEST STR " + teststr)
            waitingForReply = True

        if waitingForReply == True:

            while ser.inWaiting() == 0:
                pass

            dataRecvd = recvFromArduino()
            print("Reply Received  " + dataRecvd)
            n += 1
            waitingForReply = False

            print("===========")

        #time.sleep(5)


def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


def avgFinder():
    global average

    for i in range(30):
        bytevalue=ser.readline()
        value=float(bytevalue.decode("utf-8"))
        avglist.append(value)
        print(value)

    print(avglist)
    averag=sum(avglist)
    print(averag)
    average=averag/30




# ======================================

# THE DEMO PROGRAM STARTS HERE

# ======================================

import serial
import time
from numpy import array
import matplotlib.pyplot as plt

print()
print()

# NOTE the user must ensure that the serial port and baudrate are correct
# serPort = "/dev/ttyS80"
serPort = "/dev/cu.usbmodem14301"
baudRate = 9600
ser = serial.Serial(serPort, baudRate)
print("Serial port " + serPort + " opened  Baudrate " + str(baudRate))

startMarker = 60
endMarker = 62

#waitForArduino()

testData = []

readinglist=[]
stepperlist=[]
plotlist=[]
avglist=[]

average=0

time.sleep(1) #waiting for equipment to warm up

avgFinder()

print("This is the average:",average)
input("Ok?")

for i in range(200):

    """testData.append(input("Enter <speed,acceleration,position>:"))
    runTest(testData)
    testData=[]"""

    fanread = ser.readline()
    #print("original reading:",float(fanread.decode())
    bfanread = (float(fanread.decode('utf-8'))-average) ** 2
    print("altered reading:",bfanread)
    stepperpos=translate(bfanread,1,17,0,600)
    print("stepperpos:",stepperpos)

    readinglist.append(bfanread)
    stepperlist.append(stepperpos)

    plotlist.append(i)
    i+=1
    stepperposition="<"+str(stepperpos)+">"
    ser.write(stepperposition.encode('utf-8'))


y=array(readinglist)
yhat=array(stepperlist)
x=array(plotlist)

plt.figure(figsize=(31,3))
plt.plot(x,y)
plt.plot(x,yhat)

plt.show()

ser.close

