#! /usr/bin/env python3

"""
File: client.py
Desc: Client script for Simon Says game
Author: deciphr
Date: 07/13/22
"""

import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = input("Host: ")
port = 42069

client.connect((host, port))
print(f"Connecting to {host}:{port}")

try:   
    while True:
        msg = input("Message: ")
        client.send(msg.encode())
except KeyboardInterrupt:
    print("\nClosing!")