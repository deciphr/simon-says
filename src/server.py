#! /usr/bin/env python3

"""
File: server.py
Desc: Server script for Simon Says game
Author: deciphr
Date: 07/13/22
"""

import socketserver
import threading

from game_server import *

server_thread = None


if __name__ == "__main__":
    ip, port = input("Set server IP: "), 9000

    if len(ip) == 0:
        ip = "127.0.0.1"

    # handle communication between server and client
    print(f"Starting server on {ip}:{port}")
    with socketserver.TCPServer(('localhost', port), GameClientHandler) as server:
        try:
            server_thread = threading.Thread(target=server.serve_forever())
            server_thread.start()
            server_thread.join()
            
            #=== LOAD UI===#
            root = Tk()

            root.attributes('-fullscreen',True)
            root.rowconfigure(0, weight=1)
            root.columnconfigure(0, weight=1)

            StartFrame(root)
            root.mainloop()
        except KeyboardInterrupt:
            print("Server quitting!")
