#!/home/pi/robotics/dev/dev_env/bin/python

#Set project filesystem
import os
master_pwd = os.getcwd().split('/dev')[0]
import sys
sys.path.append(master_pwd)

#APPROXENG - modeul for xbox one controller
from approxeng.input.controllers import find_all_controllers
from approxeng.input.selectbinder import ControllerResource
from approxeng.input.selectbinder import bind_controllers
from approxeng.input.controllers import find_matching_controllers


# Custom modeuls
from modules import xboxone2015  # integrate xbox one 2015 wired controller

#Util
import time
import serial
import logging
# DEBUG
# INFO
# WARNING
# ERROR
# CRITICAL
logging.getLogger("approxeng.input").setLevel(logging.WARNING)
logging.basicConfig(filename='log', level=logging.DEBUG, format='%(levelname)s [%(asctime)s] - "xbox_control.py" ( %(module)s line %(lineno)d): %(message)s')


import zmq
import jsonpickle

logging.debug('Starting zmq servers')
try:
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    ID = 'XboxPUSH'
    socket.setsockopt(zmq.IDENTITY,ID.encode())
    socket.connect("tcp://localhost:5555")
    logging.info('Success - zmq is online')
except Exception as e:
    logging.critical('Error - ZMQ servers could not be initiated. Shutting down. Excpetion hit: {}'.format(e))
    sys.exit(0)


COMMANDS_BTN = {
    "square"  :"bx",
    "triangle" : "by",
    "circle" : "bb",
    "cross" : "ba",
    "ls" : "ls",
    "rs" : "rs",
    "select" : "se",
    "start" : "st",
    "home" : "ho",
    "dleft" : "dl",
    "dup" : "du",
    "dright" : "dr",
    "ddown" : "dd",
    "l1" : "lb",
    "r1" : 'rb' }

COMMANDS_AXE ={
    "lt" : "lt",
    "rt" : "rt",
    "lx" : "dx",
    "ly" : "dy",
    "rx" : "gx",
    "ry" : "gy",
    "stop" : "sp"
}

BRAUD_COM = {
    "veryslow" : "2400",
    "slow" : "4800",
    "standard" : "9600",
    "fast" : "115200",
    "veryfast" : "250000"
}

def connect_to_xbox_usb():
    discoveries = None
    try:
        discoveries = find_all_controllers()
        # device, controller, phys = find_all_controllers()
        return True
    except IOError:
        discoveries = None
        return False


def send_to_arduino(message):
    socket.send(message)


def set_to_three_digits(value):
    try:
        value = str(int(value))
        while len(value) < 3:
            value = "0" + value
        return value
    except Exception as error:
        logging.warning("Could not convert analogue value {}. Exception hit: {}".format(value, error))

def interpret_cmd(command, value):
    value = value /1.5
    if command in COMMANDS_BTN:
        command  = COMMANDS_BTN[command]
        bytes_to_send = b"B"+command.encode()+b"000"+b"\0"
        send_to_arduino(bytes_to_send)

    elif command in COMMANDS_AXE:
        command = COMMANDS_AXE[command]
        if command =="lt" or command=="rt":
            computed_value = int(value * 255)
        elif command == "dx":
            if value < 0:
                computed_value = int(-1 * value * 255)
                command = "dl"
            elif value > 0:
                computed_value = int(value * 255)
                command = "dr"
        elif command == "dy":
            if value < 0:
                computed_value = int(-1 * value * 255)
                command = "db"
            elif value > 0:
                computed_value = int(value * 255)
                command = "df"
        elif command == "gx":
            if value < 0:
                computed_value = int(-1 * value * 255)
                command = "gl"
            elif value > 0:
                computed_value = int(value * 255)
                command = "gr"
        elif command == "gy":
            if value < 0:
                computed_value = int(-1 * value * 255)
                command = "gb"
            elif value > 0:
                computed_value = int(value * 255)
                command = "gf"
        elif command == "sp":
            computed_value = 0

        proccessed_value = set_to_three_digits(computed_value)
        bytes_to_send =b'\x01'+b"A"+command.encode()+proccessed_value.encode()+b"\x00"

        send_to_arduino(bytes_to_send)


    else :
        logging.warning("Command '{}' not recognised.".format(command))



xboxConnected, disconnected_print, connected_print = False, False, False
while True:
    if xboxConnected:

        try:

            with ControllerResource() as joystick:
                if not connected_print:
                    logging.info("Success - Xbox controller detected")
                    connected_print = True
                    disconnected_print = False
                notsent=False
                while joystick.connected:

                    valuesDic = {}
                    for stick in COMMANDS_AXE:
                        try:
                            valuesDic[stick] = getattr(joystick,stick)
                        except AttributeError :
                            pass
                    keys = {v:valuesDic[v] for v in valuesDic if not -0.05 < valuesDic[v] < 0.05}
                    if keys != {}:
                        for i in keys:
                            interpret_cmd(i, keys[i])
                        notsent=True
                    elif notsent:
                        interpret_cmd("stop", 0)
                        notsent = False

                    presses = joystick.check_presses()
                    if joystick.has_presses:
                        for presses in joystick.presses:
                            if presses =="r2" or presses == "l2":
                                pass
                            elif COMMANDS_BTN[presses] == "ho" :
                                logging.info("Home button pressed, quiting scirpt !")
                                socket.send(b"QUIT")
                                sys.exit(0)
                            else:
                                interpret_cmd(presses, 0)
                    time.sleep(0.01)
        except OSError as e:
            xboxConnected = False
            # socket.send(b"end")

    elif not disconnected_print:
        logging.info('Looking for xbox controller')
        disconnected_print=True
        connected_print = False
    else:
        xboxConnected = connect_to_xbox_usb()
