#! /usr/bin/env python3

"""
File: server.py
Desc: Server script for Simon Says game
Author: deciphr
Date: 07/13/22
"""

import socket
import socketserver
import threading

import game_server

server_thread = None
connected_hosts = []


class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()

        client_addr = self.client_address[0]
        response = self.data.decode()

        if client_addr not in connected_hosts:
            connected_hosts.append(client_addr)
            print(f"{socket.gethostbyaddr(client_addr)[0]}@{client_addr} has connected!")

        if response == "ping":
            self.request.sendall("pong!")

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
            game_server.load_game()
            server.serve_forever()
        except KeyboardInterrupt:
            print("Server quitting!")
