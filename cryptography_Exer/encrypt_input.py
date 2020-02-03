from cryptography.fernet import Fernet

strKey = b"fWn9BDrXryrtcxjXhaO2BR9Oc_bS_zk1k4b6aL_0rbI="
f = Fernet(strKey)
strEncryptedFile = 'serialID.txt'

while True:
    strMachineID = input("Please input the machineID (Type 'quit' to exit): ")
    if strMachineID != "quit":
        btMachineID = strMachineID.encode()
        strEncryptedMsg = f.encrypt(btMachineID)
        strEncryptedMsg_output = strEncryptedMsg.decode()
        print(strEncryptedMsg_output)

        try:
            with open(strEncryptedFile, 'wb') as w_f:
                w_f.write(strEncryptedMsg)
                
        except IOError as io_err:
            print("File error:", io_err)

        except Exception as e:
            print("Some errors happened :", e)
    else:
        break