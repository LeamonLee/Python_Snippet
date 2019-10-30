import snap7.client
import snap7.util
import snap7.snap7types
import time
import re
import byte_array




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
    '''
    'PE': 0x81,
    'PA': 0x82,
    'MK': 0x83,
    'DB': 0x84,
    'CT': 0x1C,
    'TM': 0x1D,
    '''
    strMemory.upper()
    if strMemory != "MK":
        nDBNum = 0
    result = dev.read_area(snap7.snap7types.areas[strMemory], nDBNum, byte_idx, dataType)
    print("result from read_aread(): {}".format(result))

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
    '''
    'PE': 0x81,
    'PA': 0x82,
    'MK': 0x83,
    'DB': 0x84,
    'CT': 0x1C,
    'TM': 0x1D,
    '''
    strMemory.upper()
    if strMemory != "MK":
        nDBNum = 0
    result = dev.read_area(snap7.snap7types.areas[strMemory], nDBNum, byte_idx, dataType)
    print("result from read_aread(): {}".format(result))

    if dataType == snap7.snap7types.S7WLBit:
        snap7.util.set_bool(result, 0, bit_idx, nValue)
    elif dataType in {snap7.snap7types.S7WLByte, snap7.snap7types.S7WLWord}:
        snap7.util.set_int(result, 0, nValue)
    elif dataType == snap7.snap7types.S7WLReal:
        snap7.util.set_real(result, 0, nValue)
    elif dataType == snap7.snap7types.S7WLDWord:
        snap7.util.set_dword(result, 0, nValue)
    dev.write_area(snap7.snap7types.areas[strMemory], nDBNum, byte_idx, result)

# ==================================================================

class DBObject(object):
    pass


m_dictOffsets = { "Bool":2,"Int": 2,"Real":4,"DInt":6,"String":256}

db_datas=\
"""
Temperature,Real,0.0
Cold,Bool,4.0
RPis_to_Buy,Int,6.0
Db_test_String,String,8.0
"""

nameKey = "name"
dataTypeKey = "datatype"
offsetKey = "offset"


def DBRead(dev, db_num, length, dbitems):
    data = dev.read_area(snap7.snap7types.areas['DB'], db_num, 0, length)
    obj = DBObject()
    
    for item in dbitems.values():
        value = None
        offset = int(item[offsetKey].split('.')[0])
        _type = item[dataTypeKey].lower()
        

        if _type == 'Real'.lower():
            value = snap7.util.get_real(data, offset)

        elif _type =='Bool'.lower():
            bit =int(item[offsetKey].split('.')[1])
            value = snap7.util.get_bool(data, offset, bit)

        elif _type == 'DINT'.lower():
            value = byte_array.get_dint(data, offset)
        
        elif _type == 'UDINT'.lower() or _type == 'DWORD'.lower():
            value = byte_array.get_udint(data, offset)

        elif _type == 'Int'.lower():
            value = snap7.util.get_int(data, offset)

        elif _type == 'UINT'.lower() or _type == 'WORD'.lower() :
            value = byte_array.get_uint(data, offset)

        elif _type == 'USINT'.lower():
            value = byte_array.get_byte(data, offset)
        
        elif _type == 'SINT'.lower():
            value = byte_array.get_sint(data, offset)

        elif _type == 'BYTE'.lower():
            value = byte_array.get_byte(data, offset)

        elif 'String'.lower() in _type:
            # value = snap7.util.get_string(data, offset, m_dictOffsets["String"])
            value = snap7.util.get_string(data, offset, byte_array.val_len(_type, None))
        
        elif _type == 'DTL'.lower():
            value = byte_array.get_DTL(data, offset)
        
        else:
            print('Unkown type', _type)
            value = None

        obj.__setattr__(item[nameKey], value)


    return obj

def DBReadTag(dev, db_num, offset, _type):

    offset = str(float(offset))
    byte = int(offset.split('.')[0])
    bit = int(offset.split('.')[1])

    length = byte_array.val_len(_type, None)
    data = dev.read_area(snap7.snap7types.areas['DB'], db_num, byte, length)

    value = None
    _type = _type.lower()
    if _type == 'Real'.lower():
            value = snap7.util.get_real(data, 0)

    elif _type =='Bool'.lower():
        
        value = snap7.util.get_bool(data, 0, bit)

    elif _type == 'DINT'.lower():
        value = byte_array.get_dint(data, 0)
    
    elif _type == 'UDINT'.lower() or _type == 'DWORD'.lower():
        value = byte_array.get_udint(data, 0)

    elif _type == 'Int'.lower():
        value = snap7.util.get_int(data, 0)

    elif _type == 'UINT'.lower() or _type == 'WORD'.lower() :
        value = byte_array.get_uint(data, 0)

    elif _type == 'USINT'.lower():
        value = byte_array.get_byte(data, 0)
    
    elif _type == 'SINT'.lower():
        value = byte_array.get_sint(data, 0)

    elif _type == 'BYTE'.lower():
        value = byte_array.get_byte(data, 0)

    elif 'String'.lower() in _type:
        # value = snap7.util.get_string(data, offset, m_dictOffsets["String"])
        value = snap7.util.get_string(data, 0, byte_array.val_len(_type, None))
    
    elif _type == 'DTL'.lower():
        value = byte_array.get_DTL(data, 0)
    
    else:
        print('Unkown type', _type)
        value = None
    
    return value

def DBWriteByTag(dev, db_num, item, value):

    offset = int(item[offsetKey].split('.')[0])
    _type = item[dataTypeKey].lower()
    _val_len = byte_array.val_len(_type, None)

    raw_bytearray = bytearray([0] * _val_len)

    if _type == 'Real'.lower():
        snap7.util.set_real(raw_bytearray, 0, value)

    elif _type =='Bool'.lower():
        raw_bytearray = dev.read_area(snap7.snap7types.areas['DB'], db_num, offset, _val_len)
        bit = int(item[offsetKey].split('.')[1])
        snap7.util.set_bool(raw_bytearray, 0, bit, value)

    elif _type == 'DINT'.lower():
        byte_array.set_dint(raw_bytearray, 0, value)
    
    elif _type == 'UDINT'.lower() or _type == 'DWORD'.lower():
        byte_array.set_udint(raw_bytearray, 0, value)

    elif _type == 'Int'.lower():
        snap7.util.set_int(raw_bytearray, 0, value)

    elif _type == 'UINT'.lower() or _type == 'WORD'.lower() :
        byte_array.set_uint(raw_bytearray, 0, value)

    elif _type == 'USINT'.lower():
        byte_array.set_byte(raw_bytearray, 0, value)
    
    elif _type == 'SINT'.lower():
        byte_array.set_sint(raw_bytearray, 0, value)

    elif _type == 'BYTE'.lower():
        byte_array.set_byte(raw_bytearray, 0, value)

    elif 'String'.lower() in _type:
        # value = snap7.util.get_string(data, offset, m_dictOffsets["String"])
        # snap7.util.set_string(raw_bytearray, 0, value, val_len(_type, None))
        byte_array.set_string(raw_bytearray, 0, value, 250)
    
    elif _type == 'DTL'.lower():
        byte_array.set_DTL(raw_bytearray, 0, value)
    
    else:
        print('Unkown type', _type)
        

    dev.db_write(db_num, offset, raw_bytearray)


def DBWriteByOffset(dev, db_num, offset, _type, value):

    offset = str(float(offset))
    byte = int(offset.split('.')[0])
    bit = int(offset.split('.')[1])
    
    _type = _type.lower()
    _val_len = byte_array.val_len(_type, None)

    raw_bytearray = bytearray([0] * _val_len)

    if _type == 'Real'.lower():
        snap7.util.set_real(raw_bytearray, 0, value)

    elif _type =='Bool'.lower():
        
        raw_bytearray = dev.read_area(snap7.snap7types.areas['DB'], db_num, byte, _val_len)
        snap7.util.set_bool(raw_bytearray, 0, bit, value)

    elif _type == 'DINT'.lower():
        byte_array.set_dint(raw_bytearray, 0, value)
    
    elif _type == 'UDINT'.lower() or _type == 'DWORD'.lower():
        byte_array.set_udint(raw_bytearray, 0, value)

    elif _type == 'Int'.lower():
        snap7.util.set_int(raw_bytearray, 0, value)

    elif _type == 'UINT'.lower() or _type == 'WORD'.lower() :
        byte_array.set_uint(raw_bytearray, 0, value)

    elif _type == 'USINT'.lower():
        byte_array.set_byte(raw_bytearray, 0, value)
    
    elif _type == 'SINT'.lower():
        byte_array.set_sint(raw_bytearray, 0, value)

    elif _type == 'BYTE'.lower():
        byte_array.set_byte(raw_bytearray, 0, value)

    elif 'String'.lower() in _type:
        # value = snap7.util.get_string(data, offset, m_dictOffsets["String"])
        # snap7.util.set_string(raw_bytearray, 0, value, val_len(_type, None))
        byte_array.set_string(raw_bytearray, 0, value, 250)
    
    elif _type == 'DTL'.lower():
        byte_array.set_DTL(raw_bytearray, 0, value)
    
    else:
        print('Unkown type', _type)
        

    dev.db_write(db_num, byte, raw_bytearray)
    


def get_db_size(_dictItems, _dataTypeKey, _offsetKey):
    '''
    Example:
    lstOffsets:  ['0.0', '4.0', '6.0', '8.0']
    lstTypes:  ['Real', 'Bool', 'Int', 'String']
    idx:  3
    '''
    lstOffsets, lstTypes = [float(x[_offsetKey]) for x in _dictItems.values()], [x[_dataTypeKey] for x in _dictItems.values()]
    
    idx = lstOffsets.index(max(lstOffsets))
    # print(f"lstOffsets: {lstOffsets}, lstTypes: {lstTypes}, idx: {idx}")
    # lastByte = int(max(lstOffsets).split('.')[0])+(m_dictOffsets[lstTypes[idx]])
    lastByte = int(str(max(lstOffsets)).split('.')[0])+(byte_array.val_len(lstTypes[idx], None))

    return lastByte


def csv2dict(strCsvContent):
    
    # remove all the spaces
    strCsvContent = strCsvContent.replace(" ", "")

    '''
    Example:
    lstDBDatas:  ['', 'Temperature,Real,0.0', 'Cold,Bool,4.0', 'RPis_to_Buy,Int,6.0', 'Db_test_String,String,8.0', '']
    '''
    lstDBDatas = strCsvContent.split('\n')
    # print("lstDBDatas: ", lstDBDatas)
    lstFilteredDatas = filter(lambda a: a!='',lstDBDatas)
    
    
    '''
    Example:
    item:  Temperature,Real,0.0
    item.split(',')[0] :Temperature
    '''
    # for item in lstFilteredDatas:
    #     print("item: ", item)
    #     print(item.split(',')[0])
    
    deliminator=','
    dictSortedDB_items = {
        item.split(deliminator)[0]: {
            nameKey : item.split(deliminator)[0],
            dataTypeKey : item.split(deliminator)[1],
            offsetKey : item.split(deliminator)[2]
        } for item in lstFilteredDatas
    }

    '''
    Example:
    lstSortedDB_items:  [{'name': 'Temperature', 'datatype': 'Real', 'offset': '0.0'}, 
            {'name': 'Cold', 'datatype': 'Bool', 'offset': '4.0'}, 
            {'name': 'RPis_to_Buy', 'datatype': 'Int', 'offset': '6.0'}, 
            {'name': 'Db_test_String', 'datatype': 'String', 'offset': '8.0'}]
    '''
    # print("lstSortedDB_items: ", lstSortedDB_items)
    
    return dictSortedDB_items


if __name__ == "__main__":
    
    plc = snap7.client.Client()
    plc.connect('10.101.100.45', 0, 0)

    with open('DB_format.csv', 'r', encoding="utf-8") as f_read:
        strContent = f_read.read()
    
    dictSortedDB_items = csv2dict(strContent)
    
    # get the max length(offset value) of datablock
    nLength = get_db_size(dictSortedDB_items, dataTypeKey, offsetKey)
    
    # Read the db value
    objDB_Results = DBRead(plc, 7, nLength, dictSortedDB_items)

    # print("""
    # Cold:\t\t\t{}
    # Tempeature:\t\t{}
    # Rpis_to_Buy:\t{}
    # Notes:\t{}
    # """.format(objDB_Results.Cold, objDB_Results.Temperature, objDB_Results.Rpis_to_Buy, objDB_Results.Notes))

    
    # lstAttr = [attr for attr in dir(objDB_Results) if not attr.startswith('__') and not callable(getattr(objDB_Results,attr))]
    # print("lstAttr: ", lstAttr)
    # for tag_name in lstAttr:
    #     print(tag_name,": ", objDB_Results[tag_name])


    for tag_name, value in objDB_Results.__dict__.items():
        print(tag_name,": ", value)


    DBWriteByTag(plc, 7, dictSortedDB_items["Temperature"], 1111)
    DBWriteByTag(plc, 7, dictSortedDB_items["Cold"], 1)
    DBWriteByTag(plc, 7, dictSortedDB_items["Rpis_to_Buy"], 9)
    DBWriteByTag(plc, 7, dictSortedDB_items["Notes"], "hiHiHi")
    DBWriteByTag(plc, 7, dictSortedDB_items["var_DINT"], -1234567)
    DBWriteByTag(plc, 7, dictSortedDB_items["var_UDINT"], 1234567)
    DBWriteByTag(plc, 7, dictSortedDB_items["var_INT"], -1234)
    DBWriteByTag(plc, 7, dictSortedDB_items["var_UINT"], 1234)
    DBWriteByTag(plc, 7, dictSortedDB_items["var_SINT"], -123)
    DBWriteByTag(plc, 7, dictSortedDB_items["var_USINT"], 123)
    DBWriteByTag(plc, 7, dictSortedDB_items["var_Byte"], 101)
    
    import datetime
    DBWriteByTag(plc, 7, dictSortedDB_items["var_DTL"], datetime.datetime.now())
    
    DBWriteByOffset(plc, 7, 0, "Real", 1111)
    DBWriteByOffset(plc, 7, 4, "Bool", 1)
    DBWriteByOffset(plc, 7, 4.1, "Bool", 1)
    DBWriteByOffset(plc, 7, 6, "Int", 100)
    DBWriteByOffset(plc, 7, 8, "String", "Hello Snap7")
    DBWriteByOffset(plc, 7, 264, "DInt", -765443321)
    DBWriteByOffset(plc, 7, 268, "UDInt", 765443321)
    DBWriteByOffset(plc, 7, 272, "Int", -9876)
    DBWriteByOffset(plc, 7, 274, "UInt", 9876)
    DBWriteByOffset(plc, 7, 276, "SInt", -125)
    DBWriteByOffset(plc, 7, 277, "USInt", 125)
    DBWriteByOffset(plc, 7, 278, "Byte", 100)
    DBWriteByOffset(plc, 7, 280, "DTL", datetime.datetime.now())

    plc.disconnect()