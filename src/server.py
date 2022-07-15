#! /usr/bin/env python3

"""
File: server.py
Desc: Server script for Simon Says game
Author: deciphr
Date: 07/13/22
"""

import tkinter as tk

import socketserver
import threading
from game_server import GameClientHandler, StartFrame

server_thread = None
ui_thread = None

if __name__ == "__main__":
    ip, port = input("Set server IP: "), 9000

    if len(ip) == 0:
        ip = "127.0.0.1"

    #=== LOAD UI===#
    def load_ui():
        root = tk.Tk()

        root.attributes('-fullscreen', True)
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        StartFrame(root)
        root.mainloop()

        print("Started UI")

    ui_thread = threading.Thread(target=load_ui)
    ui_thread.daemon = True
    ui_thread.start()

    # handle communication between server and client
    with socketserver.TCPServer(('localhost', port), GameClientHandler) as server:
        try:
            print(f"Starting server on {ip}:{port}")
            server.serve_forever()
            print("Started!")
        except KeyboardInterrupt:
            print("Server quitting!")
        except OSError as e:
            print(e)