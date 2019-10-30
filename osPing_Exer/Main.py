import os
import sys
import threading
import time
import myPLC
import snap7
import snap7.snap7types
import signal

# Define some global variables
lock_PLC = threading.Lock()
PLC_1200 = snap7.client.Client()
bFingerPrinter = False
bStop_flag = True
bIsPLC_Connected = False

strIP_PLC = "10.101.100.27"
strIP_Fingerprinter = "10.101.100.21"


def Run_Ping():
    global bStop_flag
    global bFingerPrinter

    # hostname = "www.google.com"     # example

    while bStop_flag:
        response = os.system("ping -c 1 " + strIP_Fingerprinter)
        #and then check the response...
        if response == 0:
            print(strIP_Fingerprinter, ' is up!')
            bFingerPrinter = True
        else:
            print(strIP_Fingerprinter, ' is down!')
            bFingerPrinter = False
            
        time.sleep(5)

def Run_PLC_HeartBeat():
    global bStop_flag, lock_PLC, PLC_1200

    strMemType = "MK"
    nDBNum = 0
    byte_idx = 100
    bit_idx = 0
    while bStop_flag:
        if bIsPLC_Connected:
            lock_PLC.acquire()
            bResult = myPLC.ReadMemory(PLC_1200, strMemType, nDBNum, byte_idx, bit_idx, snap7.snap7types.S7WLBit)
            myPLC.WriteMemory(PLC_1200, strMemType, nDBNum, byte_idx, bit_idx, snap7.snap7types.S7WLBit, not bResult)
            lock_PLC.release()
        time.sleep(1)


def Run_PLC_Comm():
    global bStop_flag, lock_PLC, PLC_1200, bFingerPrinter
    
    bChanged = bFingerPrinter
    
    strMemType = "MK"
    nDBNum = 0
    byte_idx = 100
    bit_idx = 1

    while bStop_flag:
        if bIsPLC_Connected and (bChanged != bFingerPrinter):
            
            lock_PLC.acquire()
            myPLC.WriteMemory(PLC_1200, strMemType, nDBNum, byte_idx, bit_idx, snap7.snap7types.S7WLBit, bFingerPrinter)
            lock_PLC.release()
            bChanged = bFingerPrinter
        time.sleep(2)


def connectToPLC():
    global lock_PLC, bIsPLC_Connected

    lock_PLC.acquire()
    while bStop_flag and (not bIsPLC_Connected): 
        # def connect(self, address, rack, slot, tcpport=102):
        try:
            PLC_1200.connect(strIP_PLC, 0, 1)
        except:
            pass
        finally:
            bIsPLC_Connected = PLC_1200.get_connected()
            if bIsPLC_Connected:
                print("Connected to PLC successfully...")
            else:
                print("Connected to PLC failed !!! Try to connect it again...")
    lock_PLC.release()


def stop_handler(*args):
    global bStop_flag
    bStop_flag = False
    print("Quit command received...")


if __name__ == "__main__":

    th_Ping = threading.Thread(target=Run_Ping, name="Pinging Thread")
    th_PLC_HeartBeat = threading.Thread(target=Run_PLC_HeartBeat, name="PLC_HeartBeat Thread")
    th_PLC_Comm = threading.Thread(target=Run_PLC_Comm, name="PLC_Communication Thread")

    signal.signal(signal.SIGTERM, stop_handler)
    signal.signal(signal.SIGQUIT, stop_handler)
    signal.signal(signal.SIGINT,  stop_handler)     # Ctrl-C

    th_Ping.start()
    print("Pinging thread is running...")
    th_PLC_HeartBeat.start()
    print("PLC_HeartBeat thread is running...")
    th_PLC_Comm.start()
    print("PLC_Communication thread is running...")
    
    while bStop_flag:
        connectToPLC()
        time.sleep(2)

    th_Ping.join()
    th_PLC_HeartBeat.join()
    th_PLC_Comm.join()

    print("exit program.")
    sys.exit(0)
