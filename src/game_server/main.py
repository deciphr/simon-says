r"""
Server UI and Funcs
"""

from tkinter import *
from tkinter import ttk

import socket, socketserver
import threading

root = None
running_window = None
gameRunning = False

player_count = 0
connected_hosts = {}

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


class BlankFrame:
    def __init__(self, master):
        #=== Create Base Frame ===#
        self.parent = Frame(master)
        self.parent.grid(row=0, column=0, sticky=NSEW)

        return self

class StartFrame(BlankFrame):
    def add_player(self, name):
        test_label = Label(self.player_wrapper,
                           text=name, background="#fcdc92",
                           font=('Courier', 24))
        test_label.pack(fill=BOTH, expand="yes", pady=20)

    def __init__(self, master):
        super().__init__(master)

        #===Frame===#
        start_frame_title = Label(
            self.parent, text="Simon Says", height=3, font=('Courier', 45))
        start_frame_title.pack(fill='x')

        def on_btn_press():
            global gameRunning, root

            gameRunning = True
            load_frame('game', root)

        start_frame_btn = Button(
            self.parent, text="Begin!", command=on_btn_press)
        start_frame_btn.pack(side=BOTTOM)

        #===Player List===#
        self.player_wrapper = LabelFrame(self.parent)
        self.player_wrapper.pack(
            fill="both", expand="yes", padx=20, pady=50)

        player_canvas = Canvas(self.player_wrapper)
        player_canvas.place(relx=0.5, rely=0.5, anchor=CENTER)

        player_scrollbar = ttk.Scrollbar(
            self.player_wrapper, orient="vertical", command=player_canvas.yview)
        player_scrollbar.pack(side=RIGHT, fill="y")

class GameFrame(BlankFrame):
    def __init__(self, master):
        super().__init__(master)

        title = Label(
            self.parent, text="HELO!", height=3, font=('Courier', 45))
        title.pack(fill='x')

frames_list = {
    'start': StartFrame,
    'game': GameFrame
}

def get_frame(frame):
    if frame in frames_list:
        return frames_list.get(frame)

def load_frame(name, root):
    global running_window
    frame = get_frame(name)(root)

    running_window = frame

def load_ui():
        global root
        root = Tk()

        root.attributes('-fullscreen', True)
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        load_frame('start', root)
        root.mainloop()

        print("Started UI")

