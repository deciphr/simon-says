"""
File: server.py
Desc: Server script for Simon Says game
Author: deciphr
Date: 07/13/22
"""

from re import X
import netifaces as ni
import socket
import threading
DEBUG = False

def on_client_connect(client_socket, addr):
    while True:
        msg = client_socket.recv(1024)
        print(f"{addr}: msg")

    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
    port = 42069

    server.bind('127.0.0.1', port)
    if DEBUG: print("Server binded")

    server.listen(5)
    print(f"Server started: {host}:{port}")
    print("Listening for clients")

    try:
        while True:
            client, addr = server.accept()
            threading.Thread(target=on_client_connect, args=(client, addr))
    except KeyboardInterrupt:
        print("\nClosing!")

if __name__ == "__main__":
    main()