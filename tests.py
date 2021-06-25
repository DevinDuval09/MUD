'''Write some tests'''
import multiprocessing as mp
import socket as sock
import unittest as ut
from server import Server

module_client = sock.socket()
module_server = Server()
module_server_process = mp.Process(target=module_server.serve, args=())

def setUpModule():
    host = "127.0.0.1"
    port = 50000
    module_server = Server(port=port)
    module_server_process.start()
    module_client.connect((host, port))

def tearDownModule():
    module_client.close()
    module_server_process.kill()


class CommandsTest(ut.TestCase):
    server_process = None
    server = module_server
    client = module_client

    def send_command(self, command):
        my_message = f"{command}".encode('utf-8') + b'\n'
        self.client.sendall(my_message)

    def receive_response(self):
        return self.client.recv(4096).decode()
    
    def setUp(self):
        response = self.receive_response()
        print(response)
        self.assertIn("What be your name, adventurer?", response)
        self.send_command("Player 1")
        response = self.receive_response()
        print(response)
        self.assertIn("Player 1", response)
    
    def test_bad_commands(self):
        pass

