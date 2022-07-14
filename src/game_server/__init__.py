r"""
Server UI and Funcs
"""

import socket, socketserver
from tkinter import *
from tkinter import ttk

from time import sleep

player_count = 0
connected_hosts = {}

class GameClientHandler(socketserver.BaseRequestHandler):
    def listen(self):
        self.data = self.request.recv(1024).strip()

    def handle(self):
        self.listen()
    
        client_addr = self.client_address[0]
        response = self.data.decode()

        if client_addr not in connected_hosts:
            connected_hosts[client_addr] = {
                "status": 0,
                "username": None
            }

            print(f"{socket.gethostbyaddr(client_addr)[0]}@{client_addr} has connected!")

        # first connection
        try:
            client = connected_hosts[client_addr]

            if response == "ping":
                client['status'] = 'etr_user'
                self.listen()
            elif client['status'] == 'etr_user':
                client['username'] = response
                print(f"{client_addr}'s user is {client['username']}")

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

        
class StartFrame:
    def __init__(self, master):
        #=== Create Base Frame ===#
        self.start_frame = Frame(master)
        self.start_frame.grid(row=0, column=0, sticky=NSEW)

        start_frame_title = Label(
            self.start_frame, text="Simon Says", height=3, font=('Courier', 45))
        start_frame_title.pack(fill='x')

        start_frame_btn = Button(self.start_frame, text="Begin!")
        start_frame_btn.pack(side=BOTTOM)

        #===Player List===#
        self.player_wrapper = LabelFrame(self.start_frame)
        self.player_wrapper.pack(
            fill="both", expand="yes", padx=20, pady=50)

        player_canvas = Canvas(self.player_wrapper)
        player_canvas.place(relx=0.5, rely=0.5, anchor=CENTER)

        player_scrollbar = ttk.Scrollbar(
            self.player_wrapper, orient="vertical", command=player_canvas.yview)
        player_scrollbar.pack(side=RIGHT, fill="y")

        def add_player(self, name):
            global player_count
            if player_count < 5:
                player_count += 1
                test_label = Label(self.player_wrapper,
                                   text=name, background="#923f31")
                test_label.pack(fill=BOTH, expand="yes", pady=20)
