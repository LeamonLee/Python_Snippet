from opcua import Server
from random import randint
import datetime
import time

def main():
    MyServer = Server()
    strUrl = "opc.tcp://127.0.0.1:5000"
    MyServer.set_endpoint(strUrl)

    # setup our own namespace, not really necessary but should as spec
    strAddrSpaceName = "MY_OPCUA_SIMULATION_SERVER"
    oAddrSpace = MyServer.register_namespace(strAddrSpaceName)

    # get Objects node, this is where we should put our nodes
    oNode = MyServer.get_objects_node()
    print("oNode:{}".format(oNode))

     # populating our address space
    oParam = oNode.add_object(oAddrSpace, "myParameters")
    nTemperature = oParam.add_variable(oAddrSpace, "myTemperature", 0)
    nPressure = oParam.add_variable(oAddrSpace, "myPressure", 0)
    nTime = oParam.add_variable(oAddrSpace, "Time", 0)

     # populating our address space
    oParam2 = oNode.add_object(oAddrSpace, "myParameters2")
    nTemperature2 = oParam2.add_variable(oAddrSpace, "myTemperature", 0)
    nPressure2 = oParam2.add_variable(oAddrSpace, "myPressure", 0)
    nTime2 = oParam2.add_variable(oAddrSpace, "Time", 0)

    # Set variables to be writable by clients
    nTemperature.set_writable()
    nPressure.set_writable()
    nTime.set_writable()

    nTemperature2.set_writable()
    nPressure2.set_writable()
    nTime2.set_writable()

    try:
        # starting!
        MyServer.start()
        print("Server started at {} ...".format(strUrl))

        while True:
            nTemp = randint(10,70)
            nPress = randint(20,50)
            nTm = datetime.datetime.now()

            print("nTemp: {0}, nPress: {1}, nTime:{2}".format(nTemp, nPress, nTm))
            nTemperature.set_value(nTemp)
            nPressure.set_value(nPress)
            nTime.set_value(nTm)

            print("nTemp2: {0}, nPress2: {1}, nTime2:{2}".format(nTemperature2.get_value(),
                                                                 nPressure2.get_value(), 
                                                                 nTime2.get_value()))

            print("="*50)
            time.sleep(1)
    finally:
        #close connection, remove subcsriptions, etc
        MyServer.stop()

if __name__ == "__main__":
    main()
