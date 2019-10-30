import bcrypt

salt = bcrypt.gensalt(rounds=10)

password = "1188"

# Hash a password for the first time, with a randomly-generated salt
# hashed = bcrypt.hashpw(password.encode("utf8"), salt)
hashed = "$2a$10$ExNzeWUQBlSL1z2ZgKyvu.ksf3PBHbDL9XtxAhgS2s8XYYN6rCUmy"

# Check that an unhashed password matches one that has previously been hashed
if bcrypt.checkpw(password.encode("utf8"), hashed.encode("utf8")):
    print("It Matches!")
else:
    print("It Does not Match :(")
