import socket

def Main():
    strHost = "127.0.0.1"
    nPort = 5001

    server = ("127.0.0.1",5000)

    sokt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sokt.bind((strHost, nPort))

    strInputMsg = raw_input("-> ")
    while strInputMsg != 'q':
        sokt.sendto(strInputMsg, server)
        recvData, addr = sokt.recvfrom(1024)
        print("Received from server: " + str(recvData))
        strInputMsg = raw_input("-> ")
    sokt.close()

if __name__ == "__main__":
    Main()