

try:
    with open("key.key", 'rb') as f:
        strKey = f.read()
    print("strKey: ", strKey)

except IOError as io_err:
    print("File error:", io_err)

except Exception as e:
    print("Some errors happened :", e)