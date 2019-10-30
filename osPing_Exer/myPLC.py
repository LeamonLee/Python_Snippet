import snap7.client as c
import snap7.util
import snap7.snap7types
import time


def vWriteSingleOutput(dev, byte_idx, bit_idx, cmd):
    # read_area(self, area, dbnumber, start, size):
    data = dev.read_area(0x82, 0, byte_idx, 1)
    
    snap7.util.set_bool(data, byte_idx, bit_idx, cmd)

    # write_area(self, area, dbnumber, start, data):
    dev.write_area(0x82, 0, byte_idx, data)

def vWriteSingleOutput2(dev, strByteBit, cmd):

    byte_idx, bit_idx = strByteBit.split('.')
    byte_idx, bit_idx = int(byte_idx), int(bit_idx)

    # read_area(self, area, dbnumber, start, size):
    data = dev.read_area(0x82, 0, byte_idx, 1)
    
    snap7.util.set_bool(data, byte_idx, bit_idx, cmd)

    # write_area(self, area, dbnumber, start, data):
    dev.write_area(0x82, 0, byte_idx, data)

def vToggleOutput(dev, strByteBit, intervalTime):
    # Mamybe create a thread to do this so that it won't block our main thread
    for n in range(10):
        vWriteSingleOutput2(dev, strByteBit, n%2==0)    # if even number
        time.sleep(intervalTime)

def bReadSingleOutput(dev, strByteBit):
    byte_idx, bit_idx = strByteBit.split('.')
    byte_idx, bit_idx = int(byte_idx), int(bit_idx)

    # read_area(self, area, dbnumber, start, size):
    data = dev.read_area(0x82, 0, byte_idx, 1)
    bStatus = snap7.util.get_bool(data, byte_idx, bit_idx)
    return bStatus

def ReadMemory(dev, strMemory, nDBNum,byte_idx, bit_idx, dataType):
    strMemory.upper()
    if strMemory != "MK":
        nDBNum = 0
    result = dev.read_area(snap7.snap7types.areas[strMemory], nDBNum, byte_idx, dataType)
    # print("result from read_aread(): {}".format(result))

    if dataType == snap7.snap7types.S7WLBit:
        return snap7.util.get_bool(result, 0, bit_idx)
    elif dataType in {snap7.snap7types.S7WLByte, snap7.snap7types.S7WLWord}:
        return snap7.util.get_int(result, 0)
    elif dataType == snap7.snap7types.S7WLReal:
        return snap7.util.get_real(result, 0)
    elif dataType == snap7.snap7types.S7WLDWord:
        return snap7.util.get_dword(result, 0)
    else:
        return None

def WriteMemory(dev, strMemory, nDBNum,byte_idx, bit_idx, dataType, nValue):
    strMemory.upper()
    if strMemory != "MK":
        nDBNum = 0
    result = dev.read_area(snap7.snap7types.areas[strMemory], nDBNum, byte_idx, dataType)
    # print("result from read_aread(): {}".format(result))

    if dataType == snap7.snap7types.S7WLBit:
        snap7.util.set_bool(result, 0, bit_idx, nValue)
    elif dataType in {snap7.snap7types.S7WLByte, snap7.snap7types.S7WLWord}:
        snap7.util.set_int(result, 0, nValue)
    elif dataType == snap7.snap7types.S7WLReal:
        snap7.util.set_real(result, 0, nValue)
    elif dataType == snap7.snap7types.S7WLDWord:
        snap7.util.set_dword(result, 0, nValue)
    dev.write_area(snap7.snap7types.areas[strMemory], nDBNum, byte_idx, result)



offsets = { "Bool":2,"Int": 2,"Real":4,"DInt":6,"String":256}

db=\
'''
Tag\tBool\tOffset
'''

class DBObject(object):
    pass


def DBRead(dev, db_num, length, dbitems):
    data = dev.read_area(snap7.snap7types.areas['DB'], db_num, 0, length)
    objDB = DBObject()
    for item in dbitems:
        value = None
        offset = int(item["bytebit"].split('.')[0])

        if item["datatype"] == "Real":
            value = snap7.util.get_real(data, offset)

        if item["datatype"] == "Bool":
            bit = int(item["bytebit"].split('.')[1])
            value = snap7.util.get_bool(data, offset, bit)
        
        if item["datatype"] == "Int":
            value = snap7.util.get_int(data, offset)
        
        if item["datatype"] == "String":
            value = snap7.util.get_string(data, offset, 256)

        objDB.__setattr__(item["name"], value)
    
    return objDB

# get length of datablock
def get_db_size(lstItems, byteKey, dataTypeLey):
    seq, length = [x[byteKey] for x in lstItems], [x[dataTypeLey] for x in lstItems]
    idx = seq.index(max(seq))
    lastByte = int(max(seq).split('.')[0])+(offsets[length[idx]])
    return lastByte


if __name__ == "__main__":
    lstItem = filter(lambda a: a!='', db.split('\n'))
    deliminator = '\t'
    items = [
        {
            "name":x.split(deliminator)[0],
            "datatype":x.split(deliminator)[1],
            "bytebit":x.split(deliminator)[2],
        } for x in lstItem
    ]

    # get length of datablock
    length = get_db_size(items, "bytebit", "datatype")
    meh = DBRead(PLC_1200, 10, length, items)

