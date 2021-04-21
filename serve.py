"""
serve.py

Instantiates a socket-adventure `Server` and serves it on a specified
port.

You should not need to make any changes in this file.
"""


import sys
from multiprocessing import Process
from time import sleep
from server import Server


try:
    port = int(sys.argv[1])
except IndexError:
    port = 50000

server = Server(port)
#server_proc = Process(target=server.serve, args=())
server.serve()

if __name__ == '__main__':
    #server_proc.start()
    #server_proc.join()
    server.serve()
    sleep(1)

