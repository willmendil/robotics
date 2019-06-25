#!/home/pi/robotics/dev/dev_env/bin/python

import zmq
import subprocess
import sys
import logging
# DEBUG
# INFO
# WARNING
# ERROR
# CRITICAL
logging.basicConfig(filename='log', level=logging.DEBUG, format='%(levelname)s [%(asctime)s] - "server.py" (line %(lineno)d): %(message)s')

logging.debug('Closing 5555 and 5556 ports in case of crash')
port_5555 = subprocess.run("sudo fuser -KILL -k -n tcp 5555", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
port_5556 = subprocess.run("sudo fuser -KILL -k -n tcp 5556", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
logging.debug('Killing open ports (5555) sdtout: {}; sdterr: {} | (5556) sdtout: {}; sdterr: {} '.format(port_5555.stdout, port_5555.stderr, port_5556.stdout, port_5556.stderr))

logging.debug('Starting zmq servers')
try:
    context = zmq.Context()
    pull = context.socket(zmq.PULL)
    pull.bind("tcp://*:5555")

    pub = context.socket(zmq.PUB)
    ID = 'serverPUB'
    pub.setsockopt(zmq.IDENTITY, ID.encode())
    pub.bind("tcp://*:5556")
    poller = zmq.Poller()
    poller.register(pull, zmq.POLLIN)
    logging.info('Success - zmq is online')

except Exception as e:
    logging.critical('Error - ZMQ servers could not be initiated. Shutting down. Excpetion hit: {}'.format(e))
    sys.exit(0)

while True:
    sockets = dict(poller.poll())

    if pull in sockets :
        message = pull.recv()

        pub.send_multipart([b"arduinoCom", message])
        if message == b'QUIT':
            logging.warning('Quit message received. Closing ZMQ server and quiting script')
            pull.close()
            pub.close()
            sys.exit(0)
