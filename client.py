import socket
import sys
import asyncio
from os import system
#TODO: make client async
#system('python -m serve')

try:
    port = int(sys.argv[1])
except IndexError:
    port = 50000

try:
    host = sys.argv[2]
except IndexError:
    host = "127.0.0.1"

client_socket = socket.socket()
client_socket.connect((host, port))
async def send_command():
    my_message = input("> ").encode('utf-8') + b'\n'
    client_socket.sendall(my_message)
    await asyncio.sleep(.25)

async def receive_response():
    response = client_socket.recv(4096).decode()
    print(response)
    await asyncio.sleep(.25)

async def main():
    while True:
        try:
            server_response = asyncio.create_task(receive_response())
            client_input = asyncio.create_task(send_command())
            await server_response
            await client_input
        except ConnectionAbortedError:
            print("Connection closed by host.")
            break

asyncio.run(main())


