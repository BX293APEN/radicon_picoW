import socket

if __name__ == "__main__":
    ip = "192.168.10.60"
    port = 8080
    while True:
        txData = input("wasd : ")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(txData[0].encode("UTF-8"), (ip, port))