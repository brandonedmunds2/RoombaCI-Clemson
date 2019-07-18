''' script.py
Purpose: Code to test our roomba program;
IMPORTANT: Must be run using Python 3 (python3)
Last Modified: 7/3/2019
'''
## Import libraries ##
import serial
import math
import time
import RPi.GPIO as GPIO
import RoombaCI_lib
#import microprocessing
import threading
import concurrent.futures

## Variables and Constants ##
# LED pin numbers
yled = 5
rled = 6
gled = 13
micOne=17
micTwo=22
micThree=27
reset=24
#notHeard=0.01
#oneNotHeard=True
#twoNotHeard=True
#threeNotHeard=True
#notHeards=[True,True,True]
#lastHeard=-1
statusOne=0
statusTwo=0
statusThree=0
times=[0,0,0]


## Functions and Definitions ##
''' Displays current date and time to the screen
    '''
def DisplayDateTime():
    # Month day, Year, Hour:Minute:Seconds
    date_time = time.strftime("%B %d, %Y, %H:%M:%S", time.gmtime())
    print("Program run: ", date_time)

def timedReset():
    GPIO.output(reset,GPIO.LOW)
    time.sleep(1)
    GPIO.output(reset,GPIO.HIGH)
    
def triangulate(t12,t23,t13,c):
    a12=0.5*343*t12
    b12=math.sqrt(c**2-a12**2)
    
    
    a23=0.5*343*t23
    b23=math.sqrt(c**2-a23**2)
     
    
    
    a13=0.5*343*t13
    b13=math.sqrt(c**2-a13**2)
    
def checkMic(pin, mic, times):
    status=0
    while status==0:
        status=GPIO.input(pin)
        #print(time.time()-startloop)
    times[mic-1]=time.time()

## -- Code Starts Here -- ##
# Setup Code #
GPIO.setmode(GPIO.BCM) # Use BCM pin numbering for GPIO
DisplayDateTime() # Display current date and time

# LED Pin setup
GPIO.setup(yled, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(rled, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(gled, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(micOne, GPIO.IN, pull_up_down= GPIO.PUD_UP)##Check for initial later
GPIO.setup(micTwo, GPIO.IN,  pull_up_down= GPIO.PUD_UP)
GPIO.setup(micThree, GPIO.IN, pull_up_down= GPIO.PUD_UP)
GPIO.setup(reset, GPIO.OUT, initial=GPIO.LOW)
#statusOneTwo=0
#statusTwoTwo=0
#statusThreeTwo=0
#stuck=False
startloop=0

#with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
#        executor.map(thread_function, range(3))

GPIO.output(reset,GPIO.LOW)
startTime=time.time()
timeBase=time.time()
GPIO.output(reset, GPIO.HIGH)
# one=threading.Thread(target=checkMic, args=(micOne, 1,times), daemon=False)
# two=threading.Thread(target=checkMic, args=(micTwo, 2,times), daemon=False)
# three=threading.Thread(target=checkMic, args=(micThree, 3,times), daemon=False)
# threads=[]
# threads.append(one)
# threads.append(two)
# threads.append(three)
# while True
# try:
one=threading.Thread(target=checkMic, args=(micOne, 1,times), daemon=False)
two=threading.Thread(target=checkMic, args=(micTwo, 2,times), daemon=False)
three=threading.Thread(target=checkMic, args=(micThree, 3,times), daemon=False)
threads=[]
threads.append(one)
threads.append(two)
threads.append(three)
startloop=time.time()
for t in threads:
    t.start()
# for t in threads:
    # t.join()
while 0 in times:
    GPIO.output(gled,GPIO.HIGH)
    GPIO.output(yled,GPIO.HIGH)
    GPIO.output(rled,GPIO.HIGH)
    start=time.time()
    while time.time()-1<start:
    GPIO.output(gled,GPIO.LOW)
    GPIO.output(yled,GPIO.LOW)
    GPIO.output(rled,GPIO.LOW))
if max(times)-min(times)>0.002:
    print("Nah fam")
    times=[0,0,0]
else:
    print("T1-T2: {0:.7f}".format(1000*(times[0]-times[1])))
    print("T2-T3: {0:.7f}".format(1000*(times[1]-times[2])))
    print("T1-T3: {0:.7f}".format(1000*(times[0]-times[2])))
    if times[0]<times[1] and times[0]<times[2]:
        if times[1]<times[2]:
            print("123")
        else:
            print("132")
    elif times[1]<times[0] and times[1]<times[2]:
        if times[0]<times[2]:
            print("213")
        else:
            print("231")
    elif times[2]<times[1] and times[2]<times[0]:
        if times[1]<times[0]:
            print("321")
        else:
            print("312")
    times=[0,0,0]
    #time.sleep(0.5)
    #calculations go here
    timedReset()
    #stuck=False 
#    print("Mic One: {0}".format(statusOne))
#    print("Mic Two: {0}".format(statusTwo))
#    print("Mic Three: {0}".format(statusThree))
#time.sleep(0.1)
if time.time()-timeBase>1.0:
    print(time.time()-startloop)
    timeBase=timeBase+1
    #   time.sleep(1)
# except KeyboardInterrupt:
     # break
GPIO.output(reset,GPIO.LOW)

'''
# Wake Up Roomba Sequence
GPIO.output(gled, GPIO.HIGH) # Turn on green LED to say we are alive
print(" Starting ROOMBA... ")
Roomba = RoombaCI_lib.Create_2("/dev/ttyS0", 115200)
Roomba.ddPin = 23 # Set Roomba dd pin number
GPIO.setup(Roomba.ddPin, GPIO.OUT, initial=GPIO.LOW)
Roomba.WakeUp(131) # Start up Roomba in Safe Mode
# 131 = Safe Mode; 132 = Full Mode (Be ready to catch it!)
Roomba.BlinkCleanLight() # Blink the Clean light on Roomba

if Roomba.Available() > 0: # If anything is in the Roomba receive buffer
	x = Roomba.DirectRead(Roomba.Available()) # Clear out Roomba boot-up info
	#print(x) # Include for debugging

print(" ROOMBA Setup Complete")
GPIO.output(yled, GPIO.HIGH) # Indicate within setup sequence
# Initialize IMU
print(" Starting IMU...")
imu = RoombaCI_lib.LSM9DS1_I2C() # Initialize IMU
time.sleep(0.1)
# Clear out first reading from all sensors
x = imu.magnetic
x = imu.acceleration
x = imu.gyro
# Calibrate IMU
print(" Calibrating IMU...")
Roomba.Move(0,75) # Start Roomba spinning
imu.CalibrateMag() # Calculate magnetometer offset values
Roomba.Move(0,0) # Stop Roomba spinning
time.sleep(0.5)
imu.CalibrateGyro() # Calculate gyroscope offset values
# Display offset values
print("mx_offset = {:f}; my_offset = {:f}; mz_offset = {:f}"\
	.format(imu.m_offset[0], imu.m_offset[1], imu.m_offset[2]))
print("gx_offset = {:f}; gy_offset = {:f}; gz_offset = {:f}"\
	.format(imu.g_offset[0], imu.g_offset[1], imu.g_offset[2]))
print(" IMU Setup Complete")
time.sleep(3) # Gives time to read offset values before continuing
GPIO.output(yled, GPIO.LOW) # Indicate setup sequence is complete

if Xbee.inWaiting() > 0: # If anything is in the Xbee receive buffer
    x = Xbee.read(Xbee.inWaiting()).decode() # Clear out Xbee input buffer
    #print(x) # Include for debugging

# Main Code #


## -- Ending Code Starts Here -- ##
# Make sure this code runs to end the program cleanly

Roomba.ShutDown() # Shutdown Roomba serial connection
Xbee.close()
'''
GPIO.cleanup() # Reset GPIO pins for next program