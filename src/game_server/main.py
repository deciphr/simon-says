r"""
Server UI and Funcs
"""

from time import sleep
from tkinter import *
from tkinter import ttk

import socket
import socketserver
from itertools import islice, cycle

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

                print(
                    f"{client_addr} has connected!")
        # first connection
        try:
            client = connected_hosts[client_addr]
            if response == "ping" and client['status'] == "":
                client['status'] = 'etr_user'
            elif client['status'] == 'etr_user':
                client['username'] = response
                client['status'] = 'waiting_on_start'

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
        self.parent.grid(row=0, column=0, sticky=NSEW)
        start_frame_title = Label(
            self.parent, text="Simon Says", height=3, font=('Courier', 45))
        start_frame_title.pack(fill='x')

        def on_btn_press():
            global gameRunning, root

            gameRunning = True
            
            self.parent.destroy()
            load_frame('intro', root)

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


class IntroFrame(BlankFrame):
    def __init__(self, master):
        super().__init__(master)

        self.parent.grid(row=0, column=0, sticky=NSEW)
        self.messages = islice(cycle(["Welcome Simon Says!", "In order to play, you must use the following keys: W, A, S, D.",
                                        "Press the keys according to the pattern on the screen.", "Are you ready?"]), 4)
        self.message_count = 0
        self.title = Label(
            self.parent, text="", height=3, font=('Courier', 45), wraplength=root.winfo_width())
        self.title.place(relx=.5, rely=.5, anchor="center")

        if self.message_count < 4:
            self.update_label()

    def update_label(self):
        self.message_count += 1
        print('yes')
        try:
            value = next(self.messages)
            self.title['text'] = value

            root.after(1500, self.update_label)
        except StopIteration:
            self.parent.destroy()
            load_frame('play', root)
            print('stopped iter')
            
class PlayFrame(BlankFrame):
    def __init__(self, master):
        super().__init__(master)

        self.parent.grid(row=0, column=0, sticky=NSEW)
        # self.parent.config(bg="black")
        # # self.parent.grid_rowconfigure(0, weight=1)
        # # self.parent.grid_rowconfigure(1, weight=1)
        # # self.parent.grid_columnconfigure(0, weight=1)
        # # self.parent.grid_columnconfigure(2, weight=1)
        # self.parent.pack()
        self.buttons = {}

        def make_key(key, x, y, **grid_options):
            button = Label(self.parent, text=key, borderwidth=2, font=('Courier', 50), bg='white')
            button.grid(**grid_options)
            button.place(relx=x, rely=y, anchor="center")

            self.buttons[key] = button
        
        def flash_key(key):
            button = self.buttons[key]
            button.config(bg="black")
            root.after(1000, button.config(bg="white"))
        
        make_key('Up', x=0.5, y=0.25, row=0, column=1)
        make_key('Down', x=0.5, y=.75, row=1, column=1)
        make_key('Left', x=0.25, y=.75, row=1, column=0)
        make_key('Right', x=0.75,y=.75, row=1, column=2)
        flash_key('Up')
    def send_pattern(self, pattern):
        self.flash_key(self.buttons[pattern])


frames_list = {
    'start': StartFrame,
    'intro': IntroFrame,
    'play': PlayFrame
}


def get_frame(frame):
    if frame in frames_list:
        return frames_list.get(frame)


def load_frame(name, root):
    global running_window
    running_window = get_frame(name)(root)


def load_ui():
    global root
    root = Tk()

    root.attributes('-fullscreen', True)
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    load_frame('start', root)
    root.mainloop()

    print("Started UI")
