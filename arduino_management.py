#Set project filesystem
import os
master_pwd = os.getcwd().split('/scripts/')[0]
import sys
sys.path.append(master_pwd)

#import util modeluls
import serial
import time
from subprocess import call
import glob, shutil
import logging
# FORMAT = '%(levelname)s - [%(asctime)s] - [def %(funcName)s] : [%(message)s]'
# logging.basicConfig(filename = master_pwd + '/log/arduino_management.log', level=logging.DEBUG, format=FORMAT)

def connect_to_arduino_usb(braud=9600, timeout=.5, write_timeout=.1):

    try:
        port = "/dev/ttyACM0"
        ser = serial.Serial(port, braud, timeout=timeout, write_timeout=write_timeout)
        time.sleep(1)
        message = "Connected to arduino on port : " + port
        logging.info(message)
        return ser
    except FileNotFoundError:
        port = "/dev/ttyACM1"
        ser = serial.Serial(port, braud, timeout=timeout, write_timeout=write_timeout)
        time.sleep(1)
        message = "Connected to arduino on port : " + port
        logging.info(message)
        return ser
    except serial.serialutil.SerialException as error:
        message = "Could not connect to arduino : " + str(error)
        logging.critical(message)
        return False


def compile_upload(filename, board = "uno"):
    path = master_pwd + "/scripts/arduino/" + filename
    for builds in glob.glob(path+"/build*"):
        shutil.rmtree(builds, ignore_errors=True)


    try:
        f = open(path+"/"+"Makefile", 'w+')
        f.write("ARDUINO_DIR = /usr/share/arduino\n")
        f.write("ARDUINO_PORT = /dev/ttyACM*\n\n")
        f.write("USR_LIB_PATH = "+path+"/libraries\n")
        f.write("BOARD_TAG = " + board+"\n\n")
        f.write("include /usr/share/arduino/Arduino.mk\n")
        f.close()
    except Excpetion as error:
        message = "Could not write '" + filename + "' Makefile : " + str(error)
        logging.critical(message)
        return False

    fLog = open(path+"/"+"make.log", 'w+')
    call("make upload clean",cwd=path, shell=True, stdout=fLog)
    fLog.close()

    if os.path.isdir(path+"/build-"+board):
        message = "Could not make or upload '" + filename + "' to arduino. Check: " + filename + "/make.log"
        logging.critical(message)
        return False
    else :
        message = "Uploaded '" + filename + "' to arduino."
        logging.info(message)
        os.remove(os.path.join(path, "make.log"))
        return True
