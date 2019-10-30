import socket
import time

def Main():
    strHost = "127.0.0.1"
    nPort = 5000

    sokt = socket.socket()
    sokt.connect((strHost, nPort))
    print("Connection succeeded")

    isKeyboardInterrupt = False
    try:
        while not isKeyboardInterrupt:
            strInputMsg = "Hello socket"
            byteInputMsg = bytes(strInputMsg, 'utf-8') 
            print(byteInputMsg)
            sokt.send(byteInputMsg)

            # time.sleep(1)

    except KeyboardInterrupt:
        print("received KeyboardInterrupt")
        isKeyboardInterrupt = True
        sokt.close()

if __name__ == "__main__":
    Main()
