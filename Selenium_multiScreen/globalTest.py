

a = 0

def foo():
    a = 100

foo()
print("Global area a= ", a)

if True:
    global a
    a = 100

print("Global area a= ", a)