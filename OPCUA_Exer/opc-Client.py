from opcua import ua, Client
import time
from datetime import datetime

def main():
    strUrl = "opc.tcp://127.0.0.1:5000"
    
    myClient = Client(strUrl)
    try:
        myClient.connect()
        print("Client connected to {} ...".format(strUrl))

        # Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
        root = myClient.get_root_node()
        print("Object's root node is: ", root)
        
        objectsRoot = myClient.get_objects_node()
        print("Objects node is: ", objectsRoot)
        print()

        tStart = time.time()
        lstObjectsRootChildren = objectsRoot.get_children()
        print("lstObjectsRootChildren are: ", lstObjectsRootChildren)
        print("It costs {} sec".format(time.time() - tStart))

        print()
        objectsRootChildrensChild = lstObjectsRootChildren[1].get_children()
        print("objectsRootChildrensChild[1] is: ", objectsRootChildrensChild)
        for obj in objectsRootChildrensChild:
            print(obj.get_value())

        print()
        objectsRootChildrensChild = lstObjectsRootChildren[2].get_children()
        print("objectsRootChildrensChild[2] is: ", objectsRootChildrensChild)
        for obj in objectsRootChildrensChild:
            print(obj.get_value())

        # print("Browser name of root is: ", root.get_browse_name())
        # print("Attributes of root is: ", root.get_attributes())

        # Node objects have methods to read and write node attributes as well as browse or populate address space
        node_ID = root.get_child( ["0:Objects", "2:myParameters", "2:myPressure"] )
        print("node_ID: ", node_ID)
        print("node_ID.get_value(): ", node_ID.get_value())
        print("Children of root are: ", root.get_children())
        print()
        
        

        while True:

            nTemp = myClient.get_node("ns={0};i={1}".format(2,2))
            print("nTemp.get_data_value():{} ".format(nTemp.get_data_value()))
            
            tStart = time.time()
            nTemperature = nTemp.get_value()
            print("It costs {} sec".format(time.time() - tStart))

            nPress = myClient.get_node("ns={0};i={1}".format(2,3))
            nPressure = nPress.get_value()

            TIME = myClient.get_node("ns={0};i={1}".format(2,4))
            TIME_VALUE = TIME.get_value()

            print("Temperature:{0}, Pressure:{1}, TIME:{2}".format(nTemperature, nPressure, TIME_VALUE))
            nTemp2 = myClient.get_node("ns={0};i={1}".format(2,6))
            nTemp2.set_value(99)

            time.sleep(2)
    finally:
        myClient.disconnect()


if __name__ == "__main__":
    main()