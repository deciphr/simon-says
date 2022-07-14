#! /usr/bin/env python3

"""
File: server.py
Desc: Client script for Simon Says game
Author: deciphr
Date: 07/13/22
"""

import socket
import tty
import sys
import termios

orig_settings = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin)

def client(message, ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((ip, port))
            print('sending')
            sock.sendall(bytes(str(message), 'ascii'))

            result = sock.recv(1024).decode()

            if result:
                if result == "etr_user":
                    username = input("Enter a username: ")
            else:
                print('no result')
        except ConnectionRefusedError:
            print("\nCould not connect to the server")
            sock.close()

            raise KeyboardInterrupt


if __name__ == "__main__":
    ip, port = input("Host IP: "), 9000

    if len(ip) == 0:
        ip = "127.0.0.1"
    print(f"Connecting to {ip}:{port}")

    client('ping', ip, port)

    # x = 0
    
    # while x != chr(27): # ESC
    #     x=sys.stdin.read(1)[0]
    #     print("You pressed", x)

    # termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)    
