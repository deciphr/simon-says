r"""
Server UI and Funcs
"""

from cProfile import run
from pydoc import cli
from sqlite3 import paramstyle
import game_server.frames as frames
import socket, socketserver

player_count = 0
connected_hosts = {}

running_window = None
gameRunning = False

class GameClientHandler(socketserver.BaseRequestHandler):
    def listen(self):
        # print("listening")
        self.data = self.request.recv(1024).strip()

    def handle(self):
        self.listen()
    
        client_addr = self.client_address[0]
        response = self.data.decode()

        if player_count < 5:
            if client_addr not in connected_hosts:
                connected_hosts[client_addr] = {
                    "status": "",
                    "username": None
 
                }

                print(f"{socket.gethostbyaddr(client_addr)[0]}@{client_addr} has connected!")
        # first connection
        try:
            client = connected_hosts[client_addr]
            
            if response == "ping" and client['status'] == "":
                client['status'] = 'etr_user'
            elif client['status'] == 'etr_user':
                client['username'] = response
                client['status']  = 'waiting_on_start'

                running_window.add_player(client['username'])
                print(f"{client_addr}'s user is {client['username']}")
            elif client['status'] == 'waiting_on_start':
                print("waiting on start!")
            if response == "Key.up":
                print("Up")
            elif response == "Key.down":
                print("Down")
            elif response == "Key.left":
                print("Left")
            elif response == "Key.right":
                print("Right")

            self.request.sendall(client['status'].encode())
        except ValueError:
            pass

def load_frame(name, root):
    global running_window
    frame = frames.get_frame(name)(root)

    running_window = frame
