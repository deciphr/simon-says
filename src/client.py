#! /usr/bin/env python3

"""
File: server.py
Desc: Client script for Simon Says game
Author: deciphr
Date: 07/13/22
"""

import socket
from pynput.keyboard import Key, Listener


def client(message, ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((ip, port))
            sock.sendall(bytes(str(message), 'ascii'))

            result = sock.recv(1024)

            if result:
                print(result.decode())
        except ConnectionRefusedError:
            print("\nCould not connect to the server")
            sock.close()

            raise KeyboardInterrupt


if __name__ == "__main__":
    ip, port = input("Host IP: "), 9000

    def handle_press(key):
        supported_keys = ["Key.up", "Key.down", "Key.left", "Key.right"]
        if key == Key.esc:
            raise KeyboardInterrupt

        if str(key) in supported_keys:
            client(key, ip, port)


    with Listener(on_press=handle_press) as listener:
        try:
            # is the server up?
            client("ping", ip, port)

            print("Press 'esc' to quit...")
            listener.join()

        except KeyboardInterrupt:
            print("Quitting!")
