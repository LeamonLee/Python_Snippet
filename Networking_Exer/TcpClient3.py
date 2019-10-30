import socket
'''
建立socket通過client接收
連線服務端目的ip和埠號
與服務端資料互動
'''
#建立socket
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(("127.0.0.1",8081))
print("{} ：{}".format("伺服器",client.recv(1024).decode("utf-8")))
while True :
    clientdata = input("{} ：".format("客戶端")).encode("utf-8")
    client.send(clientdata)
    receivedata = client.recv(1024).decode("utf-8")
    print("{} :{}".format("伺服器", receivedata))
    
    