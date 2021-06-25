'''Write some tests'''
import multiprocessing as mp
import socket as sock
import unittest as ut
from server import Server

class CommandsTest(ut.TestCase):
    host = "127.0.0.1"
    port = 50000
    server_process = None
    server = None
    client = None

    def send_command(self, command):
        my_message = f"{command}".encode('utf-8') + b'\n'
        self.client.sendall(my_message)

    def receive_response(self):
        return self.client.recv(4096).decode()
    
    def setUp(self):
        self.server = Server(port=self.port)
        self.server_process = mp.Process(target=self.server.serve, args=())
        self.server_process.start()
        self.client = sock.socket()
        self.client.connect((self.host, self.port))
        response = self.receive_response()
        self.assertIn("What be your name, adventurer?", response)
        self.send_command("Player 1")
        response = self.receive_response()
        self.assertIn("Player 1", response)
    
    def tearDown(self) -> None:
        self.client.close()
        self.server_process.kill()
        return super().tearDown()
    
    def test_bad_commands(self):
        self.send_command("south")
        response = self.receive_response()
        self.assertIn("prevent you from doing that", response)

    def test_movement(self):
        self.send_command("move north")
        response = self.receive_response()
        print(response)
        self.assertIn("south", response)

