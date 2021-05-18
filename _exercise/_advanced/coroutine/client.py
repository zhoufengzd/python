#perf file

import socket
import threading
import time


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect( ("localhost", 8000) )

n = 0

def printReqRate():
    global n
    while True:
        time.sleep(1)
        print(n)
        n = 0

counter = threading.Thread(target=printReqRate)
counter.start()

while True:
    sock.send(b'1')
    resp = sock.recv(100)
    n += 1
