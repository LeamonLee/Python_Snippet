import snap7
import snap7.snap7types
import mySnap7

def Run():
    PLC_1200 = snap7.client.Client()

    # def connect(self, address, rack, slot, tcpport=102):
    PLC_1200.connect("10.101.100.84", 0, 1)
    
    IsConnected = PLC_1200.get_connected()
    if IsConnected:
        print("Connected successfully...")
    else:
        print("Connected failed !!!")

    while IsConnected:
        bValid = True
        bSinOrMul = False
        bCmd = False
        nDBNum = 0
        strMemType = input("Memory type: I(i), Q(q), M(m), DB(d) or quit(qq) ?")
        strMemType.lower()
        if strMemType not in {'i', 'q', 'm', 'd', 'qq'}:
            print("Only accept command 'i', 'q', 'm', 'd' and 'qq'.")
            bValid = False
        else:
            if strMemType == 'i':
                strMemType = 'PE'
            elif strMemType == 'q':
                strMemType = 'PA'
            elif strMemType == 'm':
                strMemType = 'MK'
            elif strMemType == 'd':
                strMemType = 'DB'
                strDBNum = input("DB Number: ")
                if not strDBNum.isdigit():
                    print("Please enter an interger")
                    bValid = False
                else:
                    nDBNum = int(strDBNum)
            else:
                break
           
        if bValid == True:
            strSinOrMul = input("Single(s) or multiple(m) or quit?(qq) ")
            strSinOrMul.lower()
            if strSinOrMul not in {'s', 'm', 'qq'}:
                print("Only accept command 's', 'm' and 'qq'.")
            else:
                if strSinOrMul == 's':
                    bSinOrMul = True
                elif strSinOrMul == 'm':
                    bSinOrMul == False
                else:
                    break

        if bValid == True and bSinOrMul == True:
            strCMD = input("True(t), false(f) or quit?(qq) ")
            strCMD.lower()
            if strCMD not in {'t', 'f', 'qq'}:
                print("Only accept command 't', 'f' and 'qq'.")
            else:
                if strCMD == 't':
                    bCmd = True
                elif strCMD == 'f':
                    bCmd = False
                else:
                    break
            
            strAddress = input("Address: ")
            if not isinstance(float(strAddress), float):
                print("Please enter a valid address. Ex: I0.0, Q0.0 or M0.0 etc.")
            else:
                print("You want to read address {}".format(strAddress))
                byte_idx, bit_idx = strAddress.split('.')
                byte_idx, bit_idx = int(byte_idx), int(bit_idx)
                strRorW = input("Read(r) or Write(w)?")
                strRorW.lower()
                if strRorW not in {'r', 'w'}:
                    print("Only accept command 'r' and 'w'. ")
                else:
                    if strRorW == 'r':
                        result = mySnap7.ReadMemory(PLC_1200, strMemType, nDBNum, byte_idx, bit_idx, snap7.snap7types.S7WLBit)
                        print("You want to read {0}, and the result is {1}".format(strAddress, str(result)))
                    else:
                        mySnap7.WriteMemory(PLC_1200, strMemType, nDBNum, byte_idx, bit_idx, snap7.snap7types.S7WLBit, bCmd)

                
        elif bValid == True and bSinOrMul == False:
            result = mySnap7.ReadMemory(PLC_1200, strMemType, nDBNum, 0, 1, snap7.snap7types.S7WLBit)
            print("You want to read {0}, and the result is {1}".format(strAddress, str(result)))
if __name__ == "__main__":
    Run()

    

