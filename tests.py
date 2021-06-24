'''Write some tests'''
import multiprocessing as mp
import socket as sock
import unittest as ut
from server import Server


class CommandsTest(ut.TestCase):
    host = "127.0.0.1"
    port = 50000
    server = Server(port=port)
    server_process = mp.Process(target=server.serve, args=())
    client = sock.socket()
    
    def setUp(self):
        self.server_process.start()
        self.client.connect((self.host, self.port)) 

    def tearDown(self) -> None:
        self.server_process.kill()
        return super().tearDown()

    def send_command(self, command):
        my_message = f"> {command}".encode('utf-8') + b'\n'
        self.client.sendall(my_message)

    def receive_response(self):
        return self.client.recv(4096).decode()
    
    def test_start_page(self):
        response = self.receive_response()
        self.assertIn("In the room you see", response)

