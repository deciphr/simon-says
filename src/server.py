"""
File: server.py
Desc: Server script for Simon Says game
Author: deciphr
Date: 07/13/22
"""

import netifaces as ni
import socket
import threading
DEBUG = False

def on_client_connect(client, addr):
    print(f"Connect: {addr}")

    try:
        while True:
            msg = client.recv(1024)
            print(f"{addr}: {msg.decode()}")

            client.send("Receieved!".encode())
    finally:
        client.close()
        print(f"Disconnected: {addr}")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
    port = 42069

    server.bind(('127.0.0.1', port))
    if DEBUG: print("Server binded")

    server.listen(5)
    print(f"Server started: {host}:{port}")
    print("Listening for clients")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(('127.0.0.1', port))
        server.listen(1)

        while True:
            conn, addr = server.accept()
            with conn:
                client_thread = threading.Thread(target=on_client_connect, args=(conn, addr))
                client_thread.start()
                client_thread.join()

if __name__ == "__main__":
    main()