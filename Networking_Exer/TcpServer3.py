import socket
'''
#建立socket :通過server接收
#繫結目的ip和埠號
#設定監聽
#建立連線Socket,Address接收資訊
#資料互動senddata 傳送資料
         receive 接收資料
'''
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
'''
socket.AF_INET :
socket.AF_STREAM :
'''
server.bind(("127.0.0.1",8081)) #繫結的ip和埠在元組中
server.listen(1)   #引數為監聽的數目
print("{}啟動成功，等待{}連線".format("伺服器","客戶端"))
Socket,Adress =server.accept()#返回一個新的socket連線和客戶端地址
Socket.sendto("你好，歡迎訪問伺服器".encode("utf-8"),("127.0.0.1",8081))
while True :
    receivedata = Socket.recv(1024).decode("utf-8")
    print("{} :{}".format("客戶端",receivedata))
    senddata = input("{}:".format("伺服器")).encode("utf-8")
    Socket.send(senddata)