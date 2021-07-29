import time
#import RPi.GPIO as GPIO
from time import sleep

import datetime
#import smbus
import os
import zipfile
import shutil

from pymongo import MongoClient
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
import sys

app = QtWidgets.QApplication(sys.argv)
#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)

def takefile():
    global mydict, file_path, path, jobname, print_job_path, print_profilepath
    mydict = {}
    file_path = QFileDialog.getOpenFileName()
    path = file_path[0]
    #print(file_path)
    #print(path)

    head, tail = os.path.split(path)

    jobname = tail.split('.')[0]
    mydict["Partname"] = jobname
    date_time = datetime.datetime.now()
    mydict['Date&Time'] = (date_time.strftime("%Y-%b-%d %H:%M"))

    print_job_path = '/home/pi/Desktop/one'
    print_profilepath = '/home/pi/printprofiles/'

#total_layers = 5

def vardeclare():
    global I2C_ADDR, LED_CURRENT, LED_CURRENT_WR, LED_CURRENT_RD, DMD_FAN, LED_FAN1, LED_FAN2, INPUT_SOURCE, TEST_PATTERN, SOLID_FIELD_GENERATOR, i2c
    global delay, delay1, delay2, delay_home, enable_z, opto_z, pull_z, dir_z, top_z, bottom_z, enable_tilt, opto_tilt, pull_tilt, dir_tilt, projector, LED
    I2C_ADDR = 0x1b

    LED_CURRENT = 0x52
    LED_CURRENT_WR = 0x54
    LED_CURRENT_RD = 0x55
    DMD_FAN = 0xeb
    LED_FAN1 = 0xec
    LED_FAN2 = 0xed
    INPUT_SOURCE = 0x01
    TEST_PATTERN = 0x11
    SOLID_FIELD_GENERATOR = 0x13

    #i2c = smbus.SMBus(1)
## GPIO setup and declaration

    delay = 0.001*2   #Z-axis normal movement 0.0001
    delay1 = 0.0025 #Tank movement
    delay2 = 0.001*4  #Z-axis slow movement #0.004
    delay_home = 0.001
    enable_z = 27
    opto_z = 21
    pull_z = 26
    dir_z = 13
    top_z = 23
    bottom_z = 17
    enable_tilt = 5
    opto_tilt = 24
    pull_tilt = 25
    dir_tilt = 6
    projector = 20
    LED = 19
    distance_z1 = 450
    stepcount_z1 = 200 * distance_z1


def setGPIO():
    vardeclare()
    GPIO.setup(top_z,GPIO.IN, pull_up_down=GPIO.PUD_UP) 
    GPIO.setup(bottom_z,GPIO.IN, pull_up_down=GPIO.PUD_UP) 

    GPIO.setup(enable_z,GPIO.OUT) #ch1 heating element
    GPIO.setup(opto_z,GPIO.OUT) #ch2 fan
    GPIO.setup(pull_z,GPIO.OUT) ##Pulse(for step (pump))
    GPIO.setup(dir_z,GPIO.OUT) ##for direction (pump)
    GPIO.setup(projector, GPIO.OUT)
    GPIO.setup(LED, GPIO.OUT)
    GPIO.output(opto_z,GPIO.LOW)
    time.sleep(delay)
    GPIO.output(enable_z,GPIO.LOW)
    time.sleep(delay)
    GPIO.setup(enable_tilt,GPIO.OUT) #ch1 heating element
    GPIO.setup(opto_tilt,GPIO.OUT) #ch2 fan
    GPIO.setup(pull_tilt,GPIO.OUT) ##Pulse(for step (pump))
    GPIO.setup(dir_tilt,GPIO.OUT) ##for direction (pump)
    GPIO.output(opto_tilt,GPIO.LOW)
    time.sleep(delay)
    GPIO.output(enable_tilt,GPIO.LOW)
    time.sleep(delay)

def scanmaterial():

    global card_id, card, print_start
    ser = serial.Serial('/dev/ttyUSB0', 9600, 8, 'N', 1, timeout=1)
    soh = 0x01
    stx = 0x02
    etx = 0x03
    command = 'S01A0'
    bcc = 0x33

    data = ''
    card_id = ''
    card = False
    print_start = False

    while not(print_start):
        if not(card):
            try:
                print("scan the card")
                ser.write(soh)
                ser.write(str.encode(command))
                ser.write(soh)
                ser.write(etx)
                ser.write(bcc)
                time.sleep(2)
                serdata = ser.readline()
                if(len(serdata) > 0):
                    data = str(serdata.decode().split('x'))
                    card_id = (data[16:31])
                    print(card_id)
                    card = True
            except:
                pass
                print("card not available")
        elif(card):
            if (card_id = '00000000C7DBA45'):
                print("material is biocompatible")
                print_start = True
            else:
                print("Material is not biocompatible")
                print_start = False
            break


def clearprintjobfile():  
    takefile()
    files_in_dir = os.listdir(print_job_path) 
    for file in files_in_dir:                  
        os.remove(f'{print_job_path}/{file}')

def extractPrintjob():
    with zipfile.ZipFile(path, 'r') as zipobj:
        global counter, total_layers
        counter = 0
        inflist = zipobj.namelist()
        #zipobj.extractall()
        for name in inflist:
            if name.endswith('.txt'):
                tfile = zipobj.open(name, 'r')
                for line in tfile:
                    split = line.decode().split(':')
                    key = split[0]
                    value = str(split[1].rstrip('\r\n'))
                    #value = str(value.lstrip(''')
                    mydict[key] = value
            elif name.endswith('.png'):
                counter += 1
        zipobj.extractall(print_job_path)
        total_layers = counter
        
def readprintprofile():
    filename = mydict['Parameter']
    filename = str(filename.replace('"',""))
    filename = filename.strip()
    filename_suffix = 'txt'
    printprofilefile = os.path.join(print_profilepath, filename + "." + filename_suffix)
    tfile = open(printprofilefile , 'rb')
    for line in tfile:            
        split = line.decode().split(':')
        key = str(split[0].strip('\"'))
        value = str(split[1].rstrip('\r\n'))
        mydict[key] = value
    global initial_layers, base_layers, basecuring, basebwlayer, curing, curebwlayer
    initial_layers = int(mydict['buffer_layer'])
    base_layers = int(mydict['base_layers'])
    basecuring = float(mydict['base_curing'])  
    basebwlayer = 3
    curing = float(mydict['curing_time'])
    curebwlayer = 3
    
    global distance_z, stepcount_z
    distance_z = float(mydict['thickness']) #in mm
    stepcount_z = int(200 * distance_z)
def postcuring():
    mydict['cleaningSolution'] = "IPA"
    mydict['cleaningTime(min)'] = "10"
    mydict['PostcuringUnit'] = "NextDent"
    mydict['PostcuringTime(min)'] = "3"
def checkprint():
    print(curing)
    time.sleep(curing)
    print(stepcount_z)

def logindb():
    client = MongoClient("mongodb+srv://cs:cs24@cluster0.fwiab.mongodb.net/Test?retryWrites=true&w=majority")
    db = client.get_database('Test')
    records = db.Print_data
    records.insert_one(mydict)

def proj():
    vardeclare()
    setGPIO()
    GPIO.output(projector, GPIO.HIGH)
    print("projector on")

def projoff():
    vardeclare()
    setGPIO()
    GPIO.output(projector, GPIO.LOW)
    print("projector off")

def homebottom():
    setGPIO()
    vardeclare()
    GPIO.output(opto_z,GPIO.HIGH)
    time.sleep(delay_home)
    GPIO.output(enable_z,GPIO.HIGH)
    time.sleep(delay_home)
    GPIO.output(dir_z,GPIO.LOW)
    time.sleep(delay_home)
    print("pumping")
    #counter = counter + 1
    for x in range(stepcount_z1):
        GPIO.output(pull_z,GPIO.HIGH)
        time.sleep(delay_home)
        GPIO.output(pull_z,GPIO.LOW)
        time.sleep(delay_home)
        if (GPIO.input(bottom_z) == 1):
            print("movement")
            break
def hometop():
    setGPIO()
    vardeclare()
    GPIO.output(opto_z,GPIO.HIGH)
    time.sleep(delay_home)
    GPIO.output(enable_z,GPIO.HIGH)
    time.sleep(delay_home)
    GPIO.output(dir_z,GPIO.HIGH)
    time.sleep(delay_home)
    print("pumping")
    #counter = counter + 1
    for x in range(stepcount_z1):
        GPIO.output(pull_z,GPIO.HIGH)
        time.sleep(delay_home)
        GPIO.output(pull_z,GPIO.LOW)
        time.sleep(delay_home)
        if (GPIO.input(top_z) == 1):
            print("movement 2")
            break

def bottomz():
    setGPIO()
    vardeclare()
    GPIO.output(opto_z,GPIO.HIGH)
    time.sleep(delay)
    GPIO.output(enable_z,GPIO.HIGH)
    time.sleep(delay)
    GPIO.output(dir_z,GPIO.LOW)
    time.sleep(delay)
    #print("pumping")
    #counter = counter + 1
    #use 50 * stepcount_z
    for x in range(int(80 * stepcount_z)):
        GPIO.output(pull_z,GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(pull_z,GPIO.LOW)
        time.sleep(delay)
        if (GPIO.input(bottom_z) == 1):
            print("movement")
            break

def bottomzslow():
    setGPIO()
    vardeclare()
    GPIO.output(opto_z,GPIO.HIGH)
    time.sleep(delay2)
    GPIO.output(enable_z,GPIO.HIGH)
    time.sleep(delay2)
    GPIO.output(dir_z,GPIO.LOW)
    time.sleep(delay2)
    #print("pumping")
    #counter = counter + 1
    #use 10 * stepcount_z
    for x in range(int(20 * stepcount_z)): #10
        GPIO.output(pull_z,GPIO.HIGH)
        time.sleep(delay2)
        GPIO.output(pull_z,GPIO.LOW)
        time.sleep(delay2)
        if (GPIO.input(bottom_z) == 1):
            print("movement")
            break

def topz():
    setGPIO()
    vardeclare()
    GPIO.output(opto_z,GPIO.HIGH)
    time.sleep(delay)
    GPIO.output(enable_z,GPIO.HIGH)
    time.sleep(delay)
    GPIO.output(dir_z,GPIO.HIGH)
    time.sleep(delay)
    #print("pumping")
    #counter = counter + 1
    for x in range(int(80 * stepcount_z)):
        GPIO.output(pull_z,GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(pull_z,GPIO.LOW)
        time.sleep(delay)
        if (GPIO.input(top_z) == 1):
            print("movement 2")
            break

def nextlayer():
    setGPIO()
    vardeclare()
    GPIO.output(opto_z,GPIO.HIGH)
    time.sleep(delay)
    GPIO.output(enable_z,GPIO.HIGH)
    time.sleep(delay)
    GPIO.output(dir_z,GPIO.HIGH)
    time.sleep(delay)
    #print("pumping")
    #counter = counter + 1
    for x in range(int(stepcount_z)):
        GPIO.output(pull_z,GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(pull_z,GPIO.LOW)
        time.sleep(delay)
        if (GPIO.input(top_z) == 1):
            print("movement 2")
            break

def topzslow():
    setGPIO()
    vardeclare()
    GPIO.output(opto_z,GPIO.HIGH)
    time.sleep(delay2)
    GPIO.output(enable_z,GPIO.HIGH)
    time.sleep(delay2)
    GPIO.output(dir_z,GPIO.HIGH)
    time.sleep(delay2)
    #print("pumping")
    #counter = counter + 1
    for x in range(int(20 * stepcount_z)):
        GPIO.output(pull_z,GPIO.HIGH)
        time.sleep(delay2)
        GPIO.output(pull_z,GPIO.LOW)
        time.sleep(delay2)
        if (GPIO.input(top_z) == 1):
            print("movement 2")
            break

def afterhome():
    setGPIO()
    vardeclare()
    GPIO.output(opto_z,GPIO.HIGH)
    time.sleep(delay)
    GPIO.output(enable_z,GPIO.HIGH)
    time.sleep(delay)
    GPIO.output(dir_z,GPIO.HIGH)
    time.sleep(delay)
    #print("pumping")
    #counter = counter + 1
    for x in range(int(30 * stepcount_z)):
        GPIO.output(pull_z,GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(pull_z,GPIO.LOW)
        time.sleep(delay)
        if (GPIO.input(top_z) == 1):
            print("movement 2")
            break

    GPIO.output(opto_z,GPIO.HIGH)
    time.sleep(delay2)
    GPIO.output(enable_z,GPIO.HIGH)
    time.sleep(delay2)
    GPIO.output(dir_z,GPIO.LOW)
    time.sleep(delay2)
    #print("pumping")
    #counter = counter + 1
    for x in range(stepcount_z1):
        GPIO.output(pull_z,GPIO.HIGH)
        time.sleep(delay2)
        GPIO.output(pull_z,GPIO.LOW)
        time.sleep(delay2)
        if (GPIO.input(bottom_z) == 1):
            print("bot_home")
            break

def resetz():
    vardeclare()
    setGPIO()
    GPIO.output(opto_z,GPIO.LOW)
    time.sleep(delay)
    GPIO.output(enable_z,GPIO.LOW)
    time.sleep(delay)
    GPIO.output(opto_tilt,GPIO.LOW)
    time.sleep(delay)
    GPIO.output(enable_tilt,GPIO.LOW)
    time.sleep(delay)
    GPIO.cleanup()
    print("done")

def tiltup():
    setGPIO()
    vardeclare()
    GPIO.output(opto_tilt,GPIO.HIGH)
    time.sleep(delay1)
    GPIO.output(enable_tilt,GPIO.HIGH)
    time.sleep(delay1)
    GPIO.output(dir_tilt,GPIO.LOW)
    time.sleep(delay1)
    print("pumping")
    #counter = counter + 1
    for x in range(1600):
        GPIO.output(pull_tilt,GPIO.HIGH)
        time.sleep(delay1)
        GPIO.output(pull_tilt,GPIO.LOW)
        time.sleep(delay1)

def tiltdown():
    setGPIO()
    vardeclare()
    GPIO.output(opto_tilt,GPIO.HIGH)
    time.sleep(delay1)
    GPIO.output(enable_tilt,GPIO.HIGH)
    time.sleep(delay1)
    GPIO.output(dir_tilt,GPIO.HIGH)
    time.sleep(delay1)
    print("pumping")
    #counter = counter + 1
    for x in range(1600):
        GPIO.output(pull_tilt,GPIO.HIGH)
        time.sleep(delay1)
        GPIO.output(pull_tilt,GPIO.LOW)
        time.sleep(delay1)

def SetLedCurrent():
    vardeclare()
    val = [65,0,65,0,65,0]
    i2c.write_i2c_block_data(I2C_ADDR,LED_CURRENT_WR,val)
    return

def ledon():
    vardeclare()
    #SetGPIO()
    os.system('sudo killall -9 fbi')
    GPIO.output(19, GPIO.HIGH) #HIgh
    #i2c.write_i2c_block_data(I2C_ADDR, 0x52, 0x02)
    #display image to projector   
    i2c.write_byte_data(I2C_ADDR, 0x52,0x02)
    #os.system('sudo fbi --noverbose -d /dev/fb1 -T 1 /home/pi/Desktop/black.png')
    #os.system("sudo fbi -noverbose -d /dev/fb1  -T 1 /home/pi/Desktop/black.png 2> /dev/null")
    #time.sleep(4)
    """os.system("sudo fbi -noverbose -d /dev/fb1  -T 1 /home/pi/Desktop/black.png 2> /dev/null")
    time.sleep(3)
    
    os.system("sudo fbi -noverbose -d /dev/fb1  -T 1 /home/pi/Desktop/01.png 2> /dev/null")
    time.sleep(2)"""
    #GPIO.output(6, GPIO.HIGH) #HIgh to turn ON UV LED
    print("P LED On")
    sleep(1)
    SetLedCurrent()
#-----------------------------------------------------------------------
        #To turn the projector LED off
#-----------------------------------------------------------------------
def ledoff():
    vardeclare()
    #SetGPIO()
    i2c.write_byte_data(I2C_ADDR, 0x52,0x00)
    #i2c.write_i2c_block_data(I2C_ADDR, LED_CURRENT, 0x00)
    GPIO.output(19, GPIO.LOW) #LOw to turn off the UV LED
    print("P LED Off")

def print_seq():
    vardeclare()
    setGPIO()
    proj()
    print("projon")
    time.sleep(10)
    homebottom()
    print("homebottom")
    time.sleep(2)
    afterhome()
    print("afterhome")
    time.sleep(5)
    current_layer = 1
    while current_layer <= base_layers:
        i = current_layer
        os.system("sudo fbi --noverbose -d /dev/fb1 -T 1 /home/pi/Desktop/black.png 2> /dev/null")
        time.sleep(1)
        ledon()
        print(i)
        os.system("sudo fbi --noverbose -d /dev/fb1 -T 1 /home/pi/Desktop/one/%04d.png 2> /dev/null" % i)
        time.sleep(basecuring)
        ledoff()
        time.sleep(basebwlayer)
        topzslow()
        topz()
        bottomz()
        bottomzslow()
        time.sleep(4)
        nextlayer()
        current_layer += 1
    
    while current_layer <= initial_layers:
        i = current_layer
        os.system("sudo fbi --noverbose -d /dev/fb1 -T 1 /home/pi/Desktop/black.png 2> /dev/null")
        time.sleep(1)
        ledon()
        print(i)
        os.system("sudo fbi --noverbose -d /dev/fb1 -T 1 /home/pi/Desktop/one/%04d.png 2> /dev/null" % i)
        time.sleep(curing)
        ledoff()
        time.sleep(5)
        topzslow()
        topz()
        bottomz()
        bottomzslow()
        time.sleep(4)
        nextlayer()
        current_layer += 1
    
    while current_layer <= total_layers:
        i = current_layer
        os.system("sudo fbi --noverbose -d /dev/fb1 -T 1 /home/pi/Desktop/black.png 2> /dev/null")
        time.sleep(1)
        ledon()
        print(i)
        os.system("sudo fbi --noverbose -d /dev/fb1 -T 1 /home/pi/Desktop/one/%04d.png 2> /dev/null" % i)
        time.sleep(curing)
        ledoff()
        time.sleep(curebwlayer)
        topzslow()
        topz()
        bottomz()
        bottomzslow()
        time.sleep(4)
        nextlayer()
        current_layer += 1

def onelayer():
    vardeclare()
    proj()
    print("projon")
    time.sleep(10)
    homebottom()
    print("homebottom")
    time.sleep(2)
    afterhome()
    print("afterhome")
    time.sleep(5)
    current_layer = 1
    while current_layer <= base_layers:
        i = current_layer
        os.system("sudo fbi --noverbose -d /dev/fb1 -T 1 /home/pi/Desktop/black.png 2> /dev/null")
        time.sleep(1)
        ledon()
        print(i)
        os.system("sudo fbi --noverbose -d /dev/fb1 -T 1 /home/pi/Desktop/one/%04d.png 2> /dev/null" %i)
        time.sleep(basecuring)
        ledoff()
        time.sleep(basebwlayer)
        topzslow()
        topz()
        bottomz()
        bottomzslow()
        time.sleep(4)
        nextlayer()
        current_layer +=1
    while current_layer <= total_layers:
        i = current_layer
        os.system("sudo fbi --noverbose -d /dev/fb1 -T 1 /home/pi/Desktop/black.png 2> /dev/null")
        time.sleep(1)
        ledon()
        print(i)
        os.system("sudo fbi --noverbose -d /dev/fb1 -T 1 /home/pi/Desktop/one/%04d.png 2> /dev/null" % i)
        time.sleep(curing)
        ledoff()
        time.sleep(5)
        topzslow()
        topz()
        bottomz()
        bottomzslow()
        time.sleep(4)
        nextlayer()
        current_layer += 1

def startmain():
    print("Printing")
    clearprintjobfile()
    time.sleep(2)
        
    extractPrintjob()
    time.sleep(1)
    print(total_layers)
        
    readprintprofile()
    time.sleep(1)
        
    print_seq()
    time.sleep(4)
        
    postcuring()
    time.sleep(2)
        
    hometop()
    time.sleep(2)
    #logindb()
#clearprintjobfile()
#time.sleep(2)
#extractPrintjob()

#print(total_layers)

#readprintprofile()
#checkprint()
#print(mydict)
#bottomz()
#topz()
#time.sleep(10)
#topzslow()
#time.sleep(2)
#bottomzslow()
#topzslow()
#tiltdown()
#tiltup()
#hometop()
#resetz()
#homebottom()
#time.sleep(2)
#topz()
#afterhome()
#print_seq()
#proj()
#onelayer()
#postcuring()
#time.sleep(2)
#ledon()
#time.sleep(75)
#ledoff()
#projoff()
#hometop()
#resetz()
#logindb()

#os.system('sudo fbi -a --noverbose -T 2 /home/pi/Pixtenddemo/kalib/Mixer_screw/%s.png' % (str(current_layer)))

