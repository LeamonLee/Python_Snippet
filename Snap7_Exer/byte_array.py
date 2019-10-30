
import struct
import re
import datetime
import logging
from snap7 import six

def set_bool(B_ar, B_idx, b_idx, value):
    '''
    Set boolean value on location in bytearray
    '''
    current_value = get_bool(B_ar, B_idx, b_idx)
    index_value = 1 << b_idx

    # check if bool already has correct value
    if current_value == value:
        return

    if value:
        # make sure index_v is IN current byte
        B_ar[B_idx] += index_value
    else:
        # make sure index_v is NOT in current byte
        B_ar[B_idx] -= index_value

def get_bool(B_ar, B_idx, b_idx):
    '''
    Get the BOOLEAN value from Byte_Array
    '''
    bVal = 1 << b_idx
    BVal = B_ar[B_idx]
    return bVal == (bVal & BVal)


def set_real(B_ar, B_idx, value, big=True):
    '''
    Set Real value

    make 4 byte data from real

    '''
    value = float(value)
    if big:
        value = struct.pack('>f', value)
    else:
        value = struct.pack('<f', value)
    _bytes = struct.unpack('4B', value)
    for i, b in enumerate(_bytes):
        B_ar[B_idx + i] = b


def get_real(B_ar, B_idx, big=True):
    '''
    Get the REAL value from Byte_Array
    '''
    x = B_ar[B_idx:B_idx + 4]
    if big:
        v = struct.unpack('>f', struct.pack('4B', *x))[0]
    else:
        v = struct.unpack('<f', struct.pack('4B', *x))[0]
    return v


def set_int(B_ar, B_idx, _int, big=True):
    '''
    Set value in bytearray to int
    '''
    # make sure were dealing with an int
    _int = int(_int)
    if big:
        _bytes = struct.unpack('2B', struct.pack('>h', _int))
    else:
        _bytes = struct.unpack('2B', struct.pack('<h', _int))
    #B_ar[B_idx:2] = _bytes
    for i, b in enumerate(_bytes):
        B_ar[B_idx + i] = b

def get_int(B_ar, B_idx, big=True):
    '''
    Get the INT value from Byte_Array
    '''
    x = B_ar[B_idx:B_idx + 2]
    if big:
        v = struct.unpack('>h', struct.pack('2B', *x))[0]
    else:
        v = struct.unpack('<h', struct.pack('2B', *x))[0]
    return v


def set_uint(B_ar, B_idx, _int, big=True):
    '''
    Set value in bytearray to int
    '''
    # make sure were dealing with an int
    _int = int(_int)
    if big:
        _bytes = struct.unpack('2B', struct.pack('>H', _int))
    else:
        _bytes = struct.unpack('2B', struct.pack('<H', _int))
    for i, b in enumerate(_bytes):
        B_ar[B_idx + i] = b


def get_uint(B_ar, B_idx, big=True):
    '''
    Get the UNSIGNED INT value from Byte_Array
    '''

    x = B_ar[B_idx:B_idx + 2]
    if big:
        v = struct.unpack('>H', struct.pack('2B', *x))[0]
    else:
        v = struct.unpack('<H', struct.pack('2B', *x))[0]
    return v


def set_dint(B_ar, B_idx, value, big=True):
    '''
    Get the DINT value from Byte_Array
    '''
    value = int(value)
    if big:
        _bytes = struct.unpack('4B', struct.pack('>i', value))
    else:
        _bytes = struct.unpack('4B', struct.pack('<i', value))
    for i, b in enumerate(_bytes):
        B_ar[B_idx + i] = b


def get_dint(B_ar, B_idx, big=True):
    '''
    Get the DINT value from Byte_Array
    '''
    x = B_ar[B_idx:B_idx + 4]
    if big:
        v = struct.unpack('>i', struct.pack('4B', *x))[0]
    else:
        v = struct.unpack('<i', struct.pack('4B', *x))[0]
    return v


def set_udint(B_ar, B_idx, value, big=True):
    '''
    Get the unsigned DINT value from Byte_Array
    '''
    value = int(value)
    if big:
        _bytes = struct.unpack('4B', struct.pack('>I', value))
    else:
        _bytes = struct.unpack('4B', struct.pack('<I', value))
    for i, b in enumerate(_bytes):
        B_ar[B_idx + i] = b


def get_udint(B_ar, B_idx, big=True):
    '''
    Get the UNSIGNED DINT value from Byte_Array
    '''
    x = B_ar[B_idx:B_idx + 4]
    if big:
        v = struct.unpack('>I', struct.pack('4B', *x))[0]
    else:
        v = struct.unpack('<I', struct.pack('4B', *x))[0]
    return v
   

def set_byte(B_ar, B_idx, value):
    B_ar[B_idx] = value


def get_byte(B_ar, B_idx):
    '''
    Get the BYTE value from Byte_Array
    '''
    v = B_ar[B_idx]
    return v


def set_sint(B_ar, B_idx, value, big=True):
    '''
    '''
    value = int(value)
    if big:
        _bytes = struct.unpack('B', struct.pack('>b', value))
    else:
        _bytes = struct.unpack('B', struct.pack('<b', value))
    for i, b in enumerate(_bytes):
        B_ar[B_idx + i] = b
    # B_ar[B_idx] = value


def get_sint(B_ar, B_idx):
    '''
    Get the SINT(=signed char) value from Byte_Array
    '''
    v = B_ar[B_idx]
    
    if v > 127:
        return (256 - v) * (-1)
    else:
        return v


def set_string(B_ar, B_idx, value, max_size, big=True):
    '''
    Set string value

    :params value: string data
    :params max_size: max possible string size
    '''
    if six.PY2:
        assert isinstance(value, (str, unicode))
    else:
        assert isinstance(value, str)

    size = len(value)
    # FAIL HARD WHEN trying to write too much data into PLC
    if size > max_size:
        raise ValueError('size {0} > max_size {1} {2}'.format(size, max_size, value))
    # set len count on first position
    
    B_ar[B_idx] = max_size
    B_ar[B_idx + 1] = len(value)

    i = 0
    nStartIdx = B_idx + 2
    # fill array which chr integers
    for i, c in enumerate(value):
        B_ar[nStartIdx + i] = ord(c)

    nStartIdx += i
    # fill the rest with empty space
    for r in range(nStartIdx + 1, B_ar[B_idx]):
        B_ar[r] = ord(' ')


def get_string(B_ar, B_idx, max_size, big=True):
    '''
    Get the STRING[..] value from Byte_Array
    '''
    size = B_ar[B_idx + 1]
    if (size > max_size):
        size = max_size

    val = map(chr, B_ar[B_idx + 2:B_idx + 2 + size])
    return "".join(val)

def uint2ByteArray(val, big=True):
    
    if big:
        _bytes = struct.unpack('2B', struct.pack('>H', val))
    else:
        _bytes = struct.unpack('2B', struct.pack('<H', val))

    return _bytes

def ByteArray2uint(_bytes, big=True):
    
    if big:
        _size = struct.unpack('>H', struct.pack('2B', *_bytes))[0]
    else:
        _size = struct.unpack('<H', struct.pack('2B', *_bytes))[0]
    
    return _size

def set_wstring(B_ar, B_idx, value, max_size, big=True):
    '''
    Set string value

    :params value: string data
    :params max_size: max possible string size
    '''
    if six.PY2:
        assert isinstance(value, (str, unicode))
        value = value.decode("utf-8")
    else:
        assert isinstance(value, str)

    
    size = len(value)
    # FAIL HARD WHEN trying to write too much data into PLC
    if size > max_size:
        raise ValueError('size {0} > max_size {1} {2}'.format(size, max_size, value))
    
    # set len count on first position
    _sizeBytes = uint2ByteArray(max_size)
    _lenBytes = uint2ByteArray(len(value))
    
    B_ar[B_idx] = _sizeBytes[0]
    B_ar[B_idx + 1] = _sizeBytes[1]
    B_ar[B_idx + 2] = _lenBytes[0]
    B_ar[B_idx + 3] = _lenBytes[1]

    i = 0
    nStartIdx = B_idx + 4
    # fill array which chr integers
    for i, c in enumerate(value):
        i *= 2
        uni_code = ord(c)

        _valBytes = uint2ByteArray(uni_code)

        for _i, b in enumerate(_valBytes):
            B_ar[nStartIdx + i + _i] = b
            
    # fill the rest with empty space
    for r in range(nStartIdx + i + 2, nStartIdx + max_size*2):
        B_ar[r] = ord(' ')

def get_wstring(B_ar, B_idx, max_size, big=True):
    '''
    Get the WSTRING[..] value from Byte_Array
    '''
    
    # _sizeBytes = B_ar[B_idx: B_idx + 2]
    # _size = ByteArray2uint(_sizeBytes)
    
    lenBytes = B_ar[B_idx + 2: B_idx + 4]
    _len = ByteArray2uint(lenBytes)
    if (_len > max_size):
        _len = max_size

    nStartIdx = B_idx + 4
    nEndIdx = nStartIdx + (_len * 2)

    lstVal = []
    while nStartIdx < nEndIdx:
    
        x = B_ar[nStartIdx:nStartIdx + 2]
        v = ByteArray2uint(x)

        if six.PY2:
            lstVal.append(unichr(v))
        else:
            lstVal.append(chr(v))

        nStartIdx += 2 

    val = "".join(lstVal)
    return val


def set_DTL(B_ar, B_idx, value, big=True):

    if not isinstance(value, datetime.datetime):
        return

    set_uint(B_ar, B_idx, value.year)
    set_udint(B_ar, B_idx+8, value.microsecond * 1000)
    B_ar[B_idx+2] = value.month
    B_ar[B_idx+3] = value.day
    B_ar[B_idx+4] = ((value.weekday()+1) % 7)+1
    B_ar[B_idx+5] = value.hour
    B_ar[B_idx+6] = value.minute
    B_ar[B_idx+7] = value.second

    

def get_DTL(B_ar, B_idx, big=True):
    '''
    Get the DTL value from Byte_Array
    '''
    DTL = B_ar[B_idx:B_idx + 12]

    year = get_uint(DTL, 0)
    nanosecond = int(get_udint(DTL, 8) / 1000)

    if year == 0:
        return datetime.datetime(1970, 1, 1)

    # snap7 (DTL): year, month, day, weekday, hour, minute, second, nanosecond
    # python (datetime): year, month, day, hour, minute, second, microsecond
    # year - 2 Bytes unsigned integer
    # nanosecond - 4 Bytes unsigned integer
    return datetime.datetime(year, DTL[2], DTL[3], DTL[5], DTL[6], DTL[7], nanosecond)


def get_udt(type, udt_dict):
    _m = re.search(r'UDT\[(\w+)\]', type)
    if _m:
        _udt_name = _m.group(1)
        if _udt_name in udt_dict:
            return (_udt_name, udt_dict[_udt_name])
        else:
            return (_udt_name, None)
    else:
        return (None, None)


def get_udt_type_from_tag(tag):
    _m = re.search(r'UDT\[(\w+)\]', tag['type'])
    if _m:
        return _m.group(1)
    else:
        return None


def val_len(qry, udt_dict):
    '''
    Get the type length from tag object
    '''

    if isinstance(qry, str):
        _type = qry.upper()
    elif isinstance(qry, dict):
        _type = qry.get('type', 'UNKNOWN').upper()
    else:
        _type = 'UNKNOWN'
     
    chk_support(_type, udt_dict)
    
    if _type == 'REAL':
        return 4
    elif _type == 'DINT':
        return 4
    elif _type == 'UDINT':
        return 4
    elif _type == 'DWORD':
        return 4
    elif _type == 'INT':
        return 2
    elif _type == 'UINT':
        return 2
    elif _type == 'WORD':
        return 2
    elif _type == 'BYTE':
        return 1
    elif _type == 'SINT':
        return 1
    elif _type == 'USINT':
        return 1
    elif _type == 'BOOL':
        return 1
    elif _type.startswith('WSTRING'):
        matchedResult = re.search(r'\d+', _type)
        if matchedResult:
            max_size = int(matchedResult.group(0))
            if max_size > 16382:
                max_size = 16382
            max_size = max_size * 2
            max_size += 4
        else:
            max_size = (16382 * 2) + 4
        return max_size
    elif _type.startswith('STRING'):
        matchedResult = re.search(r'\d+', _type)
        if matchedResult:
            max_size = int(matchedResult.group(0))
            max_size += 2
            if max_size > 256:
                max_size = 256
        else:
            max_size = 256
        return max_size
    elif _type.startswith('UDT'):
        (name, info) = get_udt(_type, udt_dict)    # checked, should get both
        return info.get('Bulk_End', 0) + 1
    elif _type == 'DTL':
        return 12
    else:
        return 0


def chk_support(qry_type, udt_dict):
    '''
    Check if TYPE is support, raise exception if not
    '''

    if six.PY2:
        assert isinstance(qry_type, (str, unicode))
    else:
        assert isinstance(qry_type, str)


    _type = qry_type.upper()

    if _type.startswith('STRING') or _type.startswith('WSTRING'):
        # Exception should be raised if max_size is not found
        matchedResult = re.search(r'\d+', _type)
        if matchedResult:
            max_size = matchedResult.group(0)
            max_size = int(max_size)
        else:
            max_size = 256
        return True

    if _type.startswith('UDT'):
        (name, info) = get_udt(_type, udt_dict)
        if name is None:
            raise Exception('TypeError: {} format error'.format(_type))
        elif info is None:
            raise Exception('TypeError: UDT {} is not difined'.format(_type))
        else:
            return True
            

    if _type not in  ['REAL', 'DINT', 'UDINT', 'INT', 'UINT', 'BYTE', 'SINT', 'USINT', 'BOOL', 'DTL', 'WORD', 'DWORD']:
        raise Exception ('TypeError: {} is not supported yet'.format(_type))

    return True



def get_val(data, qry, big=True):
    '''
    Get the value from Byte_Array according to type
    TODO: string / DTL not yet implement big/little endian switch
    bool does not have big/little endian problem(does it?)
    '''
       
    if qry['type'] == 'REAL':
        ret = get_real(data, qry['byte_idx'], big)
    elif qry['type'] == 'DINT':
        ret = get_dint(data, qry['byte_idx'], big)
    elif qry['type'] == 'UDINT' or qry['type'] == 'DWORD':
        ret = get_udint(data, qry['byte_idx'], big)
    elif qry['type'] == 'INT':
        ret = get_int(data, qry['byte_idx'], big)
    elif qry['type'] == 'UINT' or qry['type'] == 'WORD' :
        ret = get_uint(data, qry['byte_idx'], big)
    elif qry['type'] == 'BOOL':
        ret = get_bool(data, qry['byte_idx'], qry['bit_idx'])
    elif qry['type'] == 'BYTE':
        ret = get_byte(data, qry['byte_idx'])
    elif qry['type'] == 'USINT':
        ret = get_byte(data, qry['byte_idx'])
    elif qry['type'] == 'SINT':
        ret = get_sint(data, qry['byte_idx'])
    elif qry['type'].startswith('STRING'):
        max_size = re.search(r'\d+', qry['type']).group(0)
        max_size = int(max_size)
        ret = get_string(data, qry['byte_idx'], max_size)
    elif qry['type'] == 'DTL':
        ret = get_DTL(data, qry['byte_idx'])
    else:
        print('Unkown type', qry['type'])

    '''
    log = logging.getLogger('Com_Device')
    if qry['type'] == 'BOOL':
        log.info('Read:{}[{}.{}] = {}'.format(qry['name'], qry['byte_idx'], qry['bit_idx'], ret))    
    else:
        log.info('Read:{}[{}] = {}'.format(qry['name'], qry['byte_idx'], ret))
    '''
    return ret


def set_val(data, offset, qry, value, big=True):
    '''
    '''
    idx = offset + qry['byte_idx']


    #log = logging.getLogger('Com_Device')
    #log.info('set_val(offset={}, qry={}, value={}'.format(idx, qry, value))
    #if qry['type'] == 'BOOL':
    #    log.info('Write: {}[{}.{}] = {}'.format(qry['name'],  idx, qry['bit_idx'], value))    
    #else:
    #    log.info('Write: {}.{}({})[{}] = {}'.format(uname, qry['name'], qry['type'],  idx, value))
  

    if qry['type'] == 'REAL':
        return set_real(data, idx, value, big)
    elif qry['type'] == 'DINT':
        return set_dint(data, idx, value, big)
    elif qry['type'] == 'UDINT' or qry['type'] == 'DWORD':
        return set_udint(data, idx, value, big)
    elif qry['type'] == 'INT':
        return set_int(data, idx, value, big)
    elif qry['type'] == 'UINT' or qry['type'] == 'WORD':
        return set_uint(data, idx, value, big)
    elif qry['type'] == 'BOOL':
        return set_bool(data, idx, value, qry['bit_idx'])
    elif qry['type'] == 'BYTE':
        return set_byte(data, idx, value)
    elif qry['type'] == 'USINT':
        return set_byte(data, idx, value)
    elif qry['type'] == 'SINT':
        return set_sint(data, idx, value)
    elif qry['type'].startswith('STRING'):
        max_size = re.search(r'\d+', qry['type']).group(0)
        max_size = int(max_size)
        return set_string(data, idx, value, max_size)
    elif qry['type'] == 'DTL':
        return set_DTL(data, idx, value)
    else:
        print('Unkown type', qry['type'])


def bytearray_to_keys(raw, qry, udt_dict, big=True):
    '''
    Map the whole structure including UDT[...]
    '''
    def map_mem_to_udt(raw, offset, udt_qry):
        '''
        According to the definition from qry, map bytearray[offset:] 
        '''
        local_data = raw[offset:]
        local_len = len(local_data)

        sub = {}
        for q_name in udt_qry:
            q = udt_qry[q_name]
            if (q['byte_idx'] + val_len(q, udt_dict)) > local_len+1:
                raise Exception('Tag %s: idex %d + offset %d out of range (%d)', q_name, q['byte_idx'], val_len(q, udt_dict), local_len)
                
            if q['type'].startswith('UDT'):
                raise Exception('Only 1 level of UDT is supported for now')
            sub[q_name] = get_val(local_data, q, big)

        return sub

    data = {}

    for q_name in qry:
        q = qry[q_name]
        if q['type'].startswith('UDT'):
            _m = re.search(r'UDT\[(\w+)\]', q['type'])
            if _m:
                udt_name = _m.group(1) # found, use the first match in parenthesis
                if udt_name not in udt_dict:
                    raise Exception('Tag %s: Used undefined UDT %s', q_name, udt_name)
                udt_qry = udt_dict[udt_name]
                # {key: {sub_key1: value1, sub_key2: value2, ...}}
                data[q_name]  = map_mem_to_udt(raw, q['byte_idx'], udt_qry['Tags'])
        else:
            # {key: value}
            data[q_name] = get_val(raw, q, big)

    return data


def keys_to_bytearray(raw, qry, val, udt_dict, big=True):
    '''
    raw = previous read bytearray[...]
    qry = tags_map[name]
    val = data[name]
    udt_dict = global udt_map
    big = big endian

    '''
    #log = logging.getLogger('Com_Device')

    def map_udt_to_mem(uname, offset, udt, val):
        '''
        offset : integer offset
        udt : {"Bulk End" : 408, ..., "Tags" : {...}}
        val : {key1 : value1, key2 : value 2, ...}
        '''


        for _vkey in val:   
            if _vkey in udt['Tags']:
                q = udt['Tags'][_vkey] # tag udt (dict)
                v = val[_vkey] # new value

                if isinstance(v, dict):
                    raise Exception('Only 1 level of UDT is supported for now')

                #msg = 'Write: {}.{}({})[{}] = {}'.format(uname, q['name'], q['type'],  q['byte_idx'] + offset,  v)

                #log.info(msg)
                set_val(raw, offset, q, v, big)
                

    #log.info('RCP1.Description = %s', val['RCP_1']['Description'])
    for _vkey in val: 
        if _vkey in qry['Tags']: 
            # new value also defined in tags_map
            v = val[_vkey]  # new value
            q = qry['Tags'][_vkey] # define of the tag

            if isinstance(v, dict): # type of value is a UserDefinedType (UDT)
                #log.info('write dict[%s]=%s', _vkey, jstr(v))
                (udtname, udtqry) = get_udt(q['type'], udt_dict)
                
                map_udt_to_mem(_vkey, q['byte_idx'], udtqry, v)
            else:
                set_val(raw,  0, q, v, big)
