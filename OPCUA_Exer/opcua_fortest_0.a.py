from time import sleep
import json
from datetime import datetime

from opcua import Client
from opcua import ua

# from elasticsearch import Elasticsearch
# from elasticsearch import helpers
import time


# es = Elasticsearch(
#     http_auth=('elastic','changeme')
# )

client = Client("opc.tcp://10.101.100.190:4840")

dictNodesInfo = {
    'Opuca_DB': 'ns=3;s="Opuca_DB"',
    # 'Opucddsffdsfda_DB': 'ns=3;dfdsfdsfs="Opuca_DB"',
}

connected = False

def readAllNodes(node, dictNodes, dictDatas):
    for NodeKey, NodeValue in dictNodes.items():
        print("NodeValue: ", NodeValue)
        if len(node.get_children()) > 0:
            for _idx, child in enumerate(node.get_children()):
                checkIsExtObject(child)

        else:
            print("len(node.get_children()) == 0: ", node)
            print("node.get_value(): ", node.get_value())

            # dictDatas[NodeKey][child.get_browse_name().Name] = child.get_value()


def checkIsExtObject(node):
    print("Entering checkIsExtObject() method... ", node)
    if isinstance(node, ua.ExtensionObject):
        print("It's an ua.ExtensionObject: ", node)
        TempNode = client.get_node(node.TypeId)
        # print("node.TypeId.StringNodeId: ", TempNode)
        strTemp = TempNode.nodeid.Identifier
        # print("Old TempNode.nodeid.Identifier: ", strTemp)
        strTemp = strTemp.replace("TE_", "")
        TempNode.nodeid.Identifier = strTemp
        # print("New TempNode.nodeid.Identifier: ", TempNode.nodeid.Identifier)

        for _idx, child in enumerate(TempNode.get_children()):
            checkIsExtObject(child)

    elif len(node.get_children()) > 0:
        print("len(node.get_children()) > 0. It's not an ua.ExtensionObject: ", node)
        
        # If node is an Array or a Structure type, can run get_children() directly instead of get_value()
        # print("It's not an ua.ExtensionObject_get_value(): ", node.get_value())
        print("Parent: node.get_browse_name().Name: ", node.get_browse_name().Name)
        for _idx, child in enumerate(node.get_children()):
            # print("child.get_value(): ", child.get_browse_name().Name, child.get_value())
            checkIsExtObject(child)

    # If it's the most bottom node, then run the get_children() command will get an empty list.
    else:
        print("len(node.get_children()) == 0: ", node)
        print("node.get_value(): ", node.get_browse_name().Name, node.get_value())
        

while True:
    try:
        client.connect()
        # client.load_type_definitions()      # What's this?
        connected = True
        
        # root = client.get_root_node()
        # nodeN0_1_ID = root.get_child( ["0:Objects", "3:DataBlocksGlobal", "3:Opuca_DB", "3:Count_A", "3:N0.1"] )
        # nodeN0_1_ID = root.get_child( ["0:Objects", "3:DataBlocksGlobal", "3:Opuca_DB", "3:Count_B"] )
        # print("nodeN0.1_ID: ", nodeN0_1_ID)

        dictNodes = {}
        dictDatas = {}

        for nodeNameKey, nodeIdValue in dictNodesInfo.items():
            dictNodes[nodeNameKey] = client.get_node(nodeIdValue)
            dictDatas[nodeNameKey] = {}

        while True:
            tStart = time.time()
            # print("dictNodes: ", dictNodes)
            
            for NodeKey, NodeValue in dictNodes.items():
            #     # dictDatas[NodeKey]["timestamp"] = datetime.now().strftime('%c')       # datetime.utcnow()
            #     # print("NodeKey: ", NodeKey)
                # print("NodeValue: ", NodeValue)
            #     # If it's the most top node(ex: the whole DB), then run the get_value() command will raise an error.
            #     # print("NodeValue.get_value(): ", NodeValue.get_value())
                readAllNodes(NodeValue, dictNodes, dictDatas)
                print("="*50)

            #     for child in NodeValue.get_children():
            #         dictDatas[NodeKey][child.get_browse_name().Name] = child.get_value()
            #         # print("child: ", child)
            # tEnd = time.time()

            # print("dictDatas: ", dictDatas)

            # for dataKey, dataValue in dictDatas.items():

            #     print()                
            #     print(datetime.now().strftime('%c'), "--> Data from OPCUA : ", dataValue)
            #     if isinstance(dataValue, dict):
            #         print("It's a dictionary")
            #         # single quote can't be replaced with double quotes, otherwise it won't work.
            #         # strTemp = "ns={0};s={1}".format(3,'"Opuca_DB"."Count_A"')
            #         strTemp = "ns={0};s={1}".format(3,'"Opuca_DB"')
            #         strMemory = "ns={0};s={1}".format(3,'Memory')
                    
            #         for key, value in dataValue.items():
            #             print("key: ", key, " value: ", value)
                        
                        # if isinstance(value, ua.ExtensionObject):
                        #     print("It's an ua.ExtensionObject")

                        #     # strTemp = "ns={0};s={1}".format(3,'"Opuca_DB"."Count_A"."N0.3"')
                        #     # nodeTemp = client.get_node(strTemp)
                        #     # print("nodeTemp.get_data_value():{} ".format(nodeTemp.get_data_value()))
                        #     # print("nodeTemp.get_value():{} ".format(nodeTemp.get_value()))

                        #     tStart2 = time.time()
                        #     CountA_node = client.get_node(strTemp)
                        #     # print(CountA_node.get_data_value())
                        #     for _idx, child in enumerate(CountA_node.get_children()):
                        #         # pass
                        #         print("child: ", _idx, child)
                                
                        #         print("child.get_value(): ", _idx, child.get_value())
                        #         if isinstance(child.get_value(), ua.ExtensionObject):
                        #             print("child.get_value().TypeId.StringNodeId: ", client.get_node(child.get_value().TypeId))
                        #             TempNode = client.get_node(child.get_value().TypeId)
                        #             print("TempNode: ", TempNode)
                        #             # print("TempNode.get_value(): ", TempNode.get_attributes([attr for attr in ua.AttributeIds]))
                        #             print("TempNode.get_value(): ", TempNode.nodeid.Identifier)
                        #             strTemp2 = TempNode.nodeid.Identifier
                        #             print(strTemp2)
                        #             strTemp3 = strTemp2.replace("TE_", "")
                        #             print(strTemp3)
                        #             TempNode.nodeid.Identifier = strTemp3
                        #             print("TempNode..nodeid.Identifier: ", TempNode.nodeid.Identifier)
                        #             print("TempNode: ", TempNode)
                        #             for _idx2, child2 in enumerate(TempNode.get_children()):
                        #                 # pass
                        #                 print("TempNode.get_value(): ", _idx2, child2.get_value())
                            
                        #     Memory_node = client.get_node(strMemory)
                        #     for _idx, child in enumerate(Memory_node.get_children()):
                        #         pass
                        #         # print("Memory_node.get_value(): ", _idx, child.get_value())

                        #     tEnd2 = time.time()
                        #     print('\ntime_elapsed: {}'.format(tEnd2 - tStart2))
                        # print("="*30)

                            # params = ua.ReadParameters()
                            # for node_id_str in ['ns=3;s="Opuca_DB"."Count_A"']:
                            #     nodeid = ua.NodeId.from_string(node_id_str)
                            #     attr = ua.ReadValueId()
                            #     attr.NodeId = nodeid
                            #     attr.AttributeId = ua.AttributeIds.Value
                            #     params.NodesToRead.append(attr)
                            
                            # results = client.uaclient.read(params)
                            # print("results: ", results)
                            # print(results[0].Value)
                        # else:
                        #     print("It's not an ua.ExtensionObject")
                # else:
                #     print("It's not a dictionary")
                #     print("value: ", dataValue)

            # print('\ntime_elapsed: {}'.format(tEnd - tStart))

            sleep(2)

    except Exception as e:
        print(e)
            
    finally:
        client.disconnect()
        print("Disconnected")
        break
    connected = False
    sleep(0.5)
    

    # for doc in res['hits']['total']:
    #     print

