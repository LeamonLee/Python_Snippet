import socket


def Main():
    strHost = "127.0.0.1"
    nPort = 5000

    sokt = socket.socket()
    sokt.connect((strHost, nPort))
    print("Connection succeeded")

    strInputMsg = input("-> ")
    while strInputMsg != 'q':
        print("You input: ", strInputMsg)
        byteInputMsg = bytes(strInputMsg, 'utf-8') 
        print(byteInputMsg)

        sokt.send(byteInputMsg)
        recvData = sokt.recv(1024)
        print(f"Received from server: {str(recvData)}")
        strInputMsg = input("-> ")
    sokt.close()

if __name__ == "__main__":
    Main()
