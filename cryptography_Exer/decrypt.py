from cryptography.fernet import Fernet

strKeyFile = "key.key"
strEncryptedFile = 'encrypted.txt'

try:
    with open(strKeyFile, 'rb') as r_f:
        strKey = r_f.read()

except IOError as io_err:
    print("File error:", io_err)

except Exception as e:
    print("Some errors happened :", e)


try:
    with open(strEncryptedFile, 'rb') as f:
        strEncryptedMsg = f.read()

except IOError as io_err:
    print("File error:", io_err)

except Exception as e:
    print("Some errors happened :", e)


print("strKey: ", strKey)
print("type(strKey): ", type(strKey))
fernet = Fernet(strKey)
print("type(strEncryptedMsg):", type(strEncryptedMsg))
strDecryptedMsg = fernet.decrypt(strEncryptedMsg)
print("strDecryptedMsg: ", strDecryptedMsg)

