#!/home/pi/robotics/dev/dev_env/bin/python

#Set project filesystem
# import os
# master_pwd = os.getcwd().split('/scripts/')[0]
# import sys
# sys.path.append(master_pwd)



#import util modeluls
import serial
import time
import zmq

import sys
import logging
# DEBUG
# INFO
# WARNING
# ERROR
# CRITICAL
logging.basicConfig(filename='log', level=logging.DEBUG, format='%(levelname)s [%(asctime)s] - "arduino_com.py" (line %(lineno)d): %(message)s')

logging.debug('Starting zmq servers')
try:
    context = zmq.Context()
    sub = context.socket(zmq.SUB)
    channel = 'arduinoCom'
    sub.setsockopt(zmq.SUBSCRIBE, channel.encode())
    sub.connect("tcp://localhost:5556")
    logging.info('Success - zmq is online')
except Exception as e:
    logging.critical('Error - ZMQ servers could not be initiated. Shutting down. Excpetion hit: {}'.format(e))
    sys.exit(0)



def connect_to_arduino_usb(braud=115200, timeout=0.1, write_timeout=0.5):

    try:
        port = "/dev/ttyACM0"
        ser = serial.Serial(port, braud)
        time.sleep(1)
        logging.info("Connected to arduino on port : {}".format(port))
        return ser
    except FileNotFoundError:
        port = "/dev/ttyACM1"
        ser = serial.Serial(port, braud)
        time.sleep(1)
        logging.info("Connected to arduino on port : {}".format(port))
        return ser
    except serial.serialutil.SerialException as error:
        logging.error("Could not connect to arduino. SerialException hit: {}".format(error))
        return False
    except Exception as error:
        logging.error("General exception hit when connecting to arduino. {}".format(error))
        return False



arduino_connected, disconnected_print, connected_print = False, False, False
i = 0
while True:


    if arduino_connected:
        if not connected_print:
            logging.info("Success - Arduino connected")
            connected_print = True
            disconnected_print = False
        # print(dir(arduino_connected))
        [address, msg] = sub.recv_multipart()
        if msg == b'QUIT':
            logging.warning('Quit message received. Closing ZMQ server and quiting script')
            arduino_connected.close()
            sys.exit(0)
        # print("[%s] %s" % (address, msg))
        # print(arduino_connected.isOpen())
        # arduino_connected.open()
        # print(arduino_connected.is_open())
        # if arduino_connected.isOpen(): # for oneshot operation
        #     arduino_connected.flush()
        try:
            arduino_connected.flushOutput()
            arduino_connected.write(msg)
            i = i + 1
            # print(msg, i)

            # arduino_connected.flush()
        except serial.serialutil.SerialTimeoutException as e:
            logging.warning('Arduino serial communication time out. Message reads: {} -  Attempting reconnection'.format(e))
            arduino_connected = connect_to_arduino_usb()
        # print(dir(arduino_connected))
        # time.sleep(0.1)
        #     arduino_connected.close()
        # arduino_connected.write(msg)
        # print(msg)



    elif not disconnected_print:
        logging.info('Looking for arduino board')
        disconnected_print=True
        connected_print = False
    else:
        arduino_connected = connect_to_arduino_usb()
