#!/home/pi/robotics/dev/dev_env/bin/python
# script added to /etc/rc.local to run on start

import subprocess
import time
import sys
import logging
# DEBUG
# INFO
# WARNING
# ERROR
# CRITICAL
logging.basicConfig(filename='log', level=logging.DEBUG, format='%(levelname)s [%(asctime)s] - "start_scripts.py" (line %(lineno)d): %(message)s')

def killProcesses(processes):
    for id, process in processes.items():
        try:
            process.kill()
        except Exception as e:
            logging.critical("Error - could not kill '{}'. The following exception was given: {}".format(id, e))


logging.info('----------------------------')
logging.info('----------------------------')
logging.info('----------------------------')
logging.info("Starting all Popen processes")
subprocess.Popen("tail -F log", shell=True)
server = subprocess.Popen("python server.py", shell=True)
xboxControl = subprocess.Popen("python xbox_control.py", shell=True)
arduinoCom = subprocess.Popen("python arduino_com.py", shell=True)

logging.debug("Processes launched, waiting 5s before monitoring".format(id))
time.sleep(5)
status = True
processes = {"server": server, "xboxControl": xboxControl, "arduinoCom": arduinoCom}
for id, process in processes.items():
    if process.poll() == None:
        logging.info("Success - process '{}' has started".format(id))
    else:
        logging.critical("Error - process '{}' did not start. Shutting down!!!".format(id))
        status = False

while status:
    for id, process in processes.items():
        if not process.poll() == None:
            logging.critical("Error - process '{}' has stopped. Shutting down!!!".format(id))

            status = False

killProcesses(processes)
sys.exit(0)





# import os
# from multiprocessing import Process
# cwd = os.getcwd()
# print(cwd)
# def server():
#     os.system("python "+ cwd+"/server.py")
# def arduino_com():
#     os.system("python "+ cwd+"/arduino_com.py")
# def xbox_control():
#     os.system("python "+ cwd+"/xbox_control.py")
#
# if __name__ == '__main__':
#     server_process = Process(target=server)
#     arduino_com_process = Process(target=arduino_com)
#     xbox_control_process = Process(target=xbox_control)
#     server_process.start()
#     arduino_com_process.start()
#     xbox_control_process.start()
#     xbox_control_process.join()
#     server_process.join()
#     arduino_com_process.join()
