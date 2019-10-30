import socket

def Main():
    strHost = "127.0.0.1"
    nPort = 5000

    sokt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sokt.bind((strHost, nPort))

    print("Server started...")

    while True:
        recvData, addr = sokt.recvfrom(1024)
        print("message from: " + str(addr))
        print("Data from connected user: " + str(recvData))
        newData = str(recvData).upper()
        print("sending back: " + str(newData))
        sokt.sendto(newData, addr)
    sokt.close()

if __name__ == "__main__":
    Main()