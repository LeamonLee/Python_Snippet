from cryptography.fernet import Fernet

message = "003AI27".encode()
strKeyFile = "key.key"
strEncryptedFile = 'encrypted.txt'

try:
    with open(strKeyFile, 'rb') as r_f:
        strKey = r_f.read()

except IOError as io_err:
    print("File error:", io_err)

except Exception as e:
    print("Some errors happened :", e)

print("strKey: ", strKey)
f = Fernet(strKey)
strEncryptedMsg = f.encrypt(message)
print("strEncryptedMsg: ", strEncryptedMsg)

try:
    with open(strEncryptedFile, 'wb') as w_f:
        w_f.write(strEncryptedMsg)

except IOError as io_err:
    print("File error:", io_err)

except Exception as e:
    print("Some errors happened :", e)