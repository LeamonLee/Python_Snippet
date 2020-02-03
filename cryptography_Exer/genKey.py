from cryptography.fernet import Fernet

strKey = Fernet.generate_key()

try:
    with open("key.key", 'wb') as f:
        f.write(strKey)
    print("strKey: ", strKey)

except IOError as io_err:
    print("File error:", io_err)

except Exception as e:
    print("Some errors happened :", e)




