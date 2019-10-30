# import signal
# # Define signal handler function
# def myHandler(signum, frame):
#     print('I received: ', signum)

# # register signal.SIGTSTP's handler 
# signal.signal(signal.SIGTSTP, myHandler)
# signal.pause()
# print('End of Signal Demo')

# =================================================

# import signal
# import time
# # Define signal handler function
# def myHandler(signum, frame):
#     print("Now, it's the time")
#     exit()

# # register signal.SIGALRM's handler 
# signal.signal(signal.SIGALRM, myHandler)
# signal.alarm(5)
# while True:
#     time.sleep(1)
#     print('not yet')

# ==================================================

# bResult = True
# bResult2 = True

# def JustAFunc():
#     bResult = False
#     print(bResult)

# # if bResult2:
# #     bResult = False
# #     print(bResult)

# JustAFunc()

# print(bResult)

# print(isinstance("0.0", float))

print( """
    Cold:\t\t{}
    Tempeature:\t\t{}
    RPis_to_Buy:\t{}
    Db_test_String:\t{}
    """.format(100,50,99,"Ivy"))
