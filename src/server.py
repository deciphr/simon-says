#! /usr/bin/env python3

"""
File: server.py
Desc: Server script for Simon Says game
Author: deciphr
Date: 07/13/22
"""

import socketserver
import threading

server_thread = None
class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()

        client_addr = self.client_address[0]
        response = self.data.decode()

        print(f"{client_addr} wrote: {response}")

        if response == "Key.up":
            print("Up")
        elif response == "Key.down":
            print("Down")
        elif response == "Key.left":
            print("Left")
        elif response == "Key.right":
            print("Right")

if __name__ == "__main__":
    ip, port = input("Set server IP: "), 9000

    # handle communication between server and client
    print(f"Starting server on {ip}:{port}")
    with socketserver.TCPServer(('localhost', port), TCPHandler) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("Server quitting!")