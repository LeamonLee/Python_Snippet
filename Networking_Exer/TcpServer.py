import socket

def Main():
    strHost = "127.0.0.1"
    nPort = 5000

    sokt = socket.socket()
    sokt.bind((strHost, nPort))

    print("Waiting for connection...")
    sokt.listen(1)

    connected_sokt, addr = sokt.accept()
    print(f"Connection from {str(addr)}")
    while True:
        data = connected_sokt.recv(1024)
        if not data:
            break
        
        print(f"from connected user: {str(data)}")
        new_data = str(data).upper()
        print(f"sending new data: {str(new_data)}")
        connected_sokt.send(bytes(new_data,'utf-8'))
    connected_sokt.close()

if __name__ == "__main__":
    Main()

