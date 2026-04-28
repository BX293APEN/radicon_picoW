#!/usr/bin/env python3
import socket

if __name__ == "__main__":
    ip = "192.168.10.60"
    port = 8080
    while True:
        data    = input("wasd : ")
        txData  = data[0] if data else " "
        sock    = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(txData.encode("UTF-8"), (ip, port))