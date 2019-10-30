from datetime import datetime

from opcua import Client
from opcua import ua

import json
import time
import csv
import pprint

client = Client("opc.tcp://10.101.100.190:4840")                            # Without user and password

# client = Client("opc.tcp://10.101.100.92:4840/MyOPCUA")                    # Without user and password
# client = Client("opc.tcp://user:password@10.101.100.92:4840/MyOPCUA")      # With user and password

dictNodesInfo = {
    # 'myOpcua_DB': 'ns=3;s="Opuca_DB"',

}

lstDefaultHeader = ["NodeName", "NodeId"]

bConnected = False

def connentToServer():
    global client
    global bConnected
    try:
        client.connect()
        bConnected = True
        print("bConnected: ", bConnected)
    except Exception as e:
        print(e)


def iterateAllNodesId(Node, _dictDatas, strParentName=None):

    if strParentName is not None:
        strNodeName = strParentName + '.'+ Node.get_browse_name().Name
    else:
        strNodeName = Node.get_browse_name().Name
    
    strParentName = strNodeName
    
    if len(Node.get_children()) > 0:    
        for _idx, child in enumerate(Node.get_children()):
            iterateAllNodesId(child, _dictDatas, strParentName)
    else:
        _dictDatas[strNodeName] = Node.nodeid.Identifier
        # print("Node.nodeid.Identifier: ", Node.nodeid.Identifier)

    # return _dictDatas


def exportAllNodesIdCsv(strFileName, _dictDatas):
    with open('AllnodesId.csv', 'w') as new_file:
        csv_writer = csv.writer(new_file, quoting=csv.QUOTE_NONE, quotechar='')
        csv_writer.writerows(_dictDatas.items())


def readConfig(strFileName):
    global client
    global lstDefaultHeader
    global dictNodesInfo
    if strFileName:
        with open(strFileName, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for idx, line in enumerate(csv_reader):
                if idx == 0:
                    nLength = len(line)
                    if nLength != len(lstDefaultHeader):
                        print("Format error! The length of header is not correct: ", nLength)
                        break
                    for element in line:
                        if element not in lstDefaultHeader:
                            print("Format error! Unexpected header element: ", element)
                            break
                        # else:
                        #     print("Header: ", element)        #  debug purpose
                else:
                    try:
                        if len(line) != len(lstDefaultHeader):
                            continue
                        # Filter out the bad value in config file before sorting into dictionary
                        _node = client.get_node(line[1])            # get_node() won't throw an exception even if the nodeId doesn't exist.
                        # _tempValue = _node.get_value()            # get_value() does throw an exception if the nodeId doesn't exist. But also throws an error in the root node
                        _tempValue = _node.get_browse_name().Name   # get_browse_name() won't throw an exception in the root node.
                        print("_tempValue: ", _tempValue)
                        dictNodesInfo[line[0]] = line[1]            # line[0]: NodeName, line[1]: NodeId
                        
                    except Exception as e:
                        print(e)
                        print("Bad config data: ", line[0], line[1])


def readAllNodes(_dictNodes, _dictDatas, bFast=True):
    
    if bFast:
        for NodeKey, NodeValue in _dictNodes.items():
            # _dictDatas[NodeKey] = {}
            # _dictDatas[NodeKey][NodeValue.get_browse_name().Name] = NodeValue.get_value()
            _tStart = time.time()
            _dictDatas[NodeKey] = NodeValue.get_value()
            _tEnd = time.time()
            print('Inner iteration time_elapsed: {}'.format(_tEnd - _tStart))

    else:
        for NodeKey, NodeValue in _dictNodes.items():
            # print("NodeValue: ", NodeValue)
            _dictDatas[NodeKey] = {}
            if len(NodeValue.get_children()) > 0:
                # get_browse_name() returns an object. Should use get_browse_name().Name
                # print("Parent: NodeValue.get_browse_name(): ", NodeValue.get_browse_name())
                # print("Parent: NodeValue.get_browse_name().Name: ", NodeValue.get_browse_name().Name)
                
                _dictDatas[NodeKey][NodeValue.get_browse_name().Name] = {}
                dictTemp = _dictDatas[NodeKey][NodeValue.get_browse_name().Name]
                # print("len(NodeValue.get_children()): ", NodeValue.get_children())
                for _idx, child in enumerate(NodeValue.get_children()):
                    _dictDatas[NodeKey][NodeValue.get_browse_name().Name] = checkIsExtObject(child, dictTemp)

            else:
                # print("len(NodeValue.get_children()) == 0: ", NodeValue)
                # print("NodeValue.get_value(): ", NodeValue.get_value())
                _dictDatas[NodeKey][NodeValue.get_browse_name().Name] = NodeValue.get_value()

    return _dictDatas


def checkIsExtObject(node, _dictDatas):
    global client
    # print("Entering checkIsExtObject() method... ")
    if isinstance(node, ua.ExtensionObject):
        # print("It's an ua.ExtensionObject: ", node)
        TempNode = client.get_node(node.TypeId)
        # print("node.TypeId.StringNodeId: ", TempNode)
        strTemp = TempNode.nodeid.Identifier
        # print("Old TempNode.nodeid.Identifier: ", strTemp)
        strTemp = strTemp.replace("TE_", "")
        TempNode.nodeid.Identifier = strTemp
        # print("New TempNode.nodeid.Identifier: ", TempNode.nodeid.Identifier)
        
        # print("Parent: node.get_browse_name().Name: ", TempNode.get_browse_name().Name)
        _dictDatas[TempNode.get_browse_name().Name] = {}
        dictTemp = _dictDatas[TempNode.get_browse_name().Name]
        for _idx, child in enumerate(TempNode.get_children()):
            _dictDatas[TempNode.get_browse_name().Name] = checkIsExtObject(child, dictTemp)

    elif hasattr(node, "get_children"):
        if len(node.get_children()) > 0:
            # print("len(node.get_children()) > 0. It's not an ua.ExtensionObject: ", node)
            
            # If node is an Array or a Structure type, we can run get_children() directly instead of get_value()
            # print("It's not an ua.ExtensionObject_get_value(): ", node.get_value())
            
            # print("Parent: node.get_browse_name().Name: ", node.get_browse_name().Name)
            _dictDatas[node.get_browse_name().Name] = {}
            dictTemp = _dictDatas[node.get_browse_name().Name]
            for _idx, child in enumerate(node.get_children()):
                # print("child.get_value(): ", child.get_browse_name().Name, child.get_value())
                _dictDatas[node.get_browse_name().Name] = checkIsExtObject(child, dictTemp)

        # If it's the most bottom node, then run the get_children() command will get an empty list.
        else:
            # print("len(node.get_children()) == 0: ", node)
            # print("node.get_value(): ", node.get_browse_name().Name, node.get_value())
            _dictDatas[node.get_browse_name().Name] = node.get_value()
    else:
        print("This object isn't an ua.ExtensionObject nor has get_children() method: ", node)
        _dictDatas[str(node)] = node
    
    return _dictDatas


def run():
    global bConnected
    global client
    global dictNodesInfo
    while True:
        try:
            
            dictNodes = {}
            dictDatas = {}

            for nodeNameKey, nodeIdValue in dictNodesInfo.items():
                dictNodes[nodeNameKey] = client.get_node(nodeIdValue)

                # dictDatas[nodeNameKey] = None               # Just for Testing

            while True:
                tStart = time.time()
                # dictDatas = readAllNodes(dictNodes, dictDatas, False)
                dictDatas = readAllNodes(dictNodes, dictDatas)
                tEnd = time.time()
                print(dictDatas)
                print('time_elapsed: {}'.format(tEnd - tStart))
                print()

                time.sleep(2)
        except KeyboardInterrupt:
            if bConnected:
                client.disconnect()
                bConnected = False
                print("Disconnected")

        except Exception as e:
            print("Exception occurred")
            print(e)
                
        finally:
            if bConnected:
                client.disconnect()
                bConnected = False
                print("Disconnected")
            # break         # No problem
        
        break               # Problem one
        # time.sleep(0.5)
        
    

if __name__ == "__main__":
    connentToServer()
    readConfig("opcua_Config.csv")
    # readConfig("opcua_Test2.csv")
    print("dictNodesInfo: ", dictNodesInfo)
    # run()

    dictTempNodes = {}
    dictTempDatas = {}
    for nodeNameKey, nodeIdValue in dictNodesInfo.items():
        dictTempNodes[nodeNameKey] = client.get_node(nodeIdValue)
        iterateAllNodesId(dictTempNodes[nodeNameKey], dictTempDatas)
        break
    # print("dictTempDatas: ", json.dumps(dictTempDatas, indent=2))
    # print("dictTempDatas: ", pprint.pprint(dictTempDatas, width=2))
    exportAllNodesIdCsv("exportedNodeIDs.csv", dictTempDatas)
    print("Done!")
    if bConnected:
        client.disconnect()
        bConnected = False
        print("Disconnected")

