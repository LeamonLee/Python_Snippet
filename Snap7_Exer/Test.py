import snap7.client
import mySnap7, byte_array


nameKey = "name"
dataTypeKey = "datatype"
offsetKey = "offset"

if __name__ == "__main__":
    
    # ===================  Connection  ======================
    plc = snap7.client.Client()
    plc.connect('10.101.100.45', 0, 0)

    # ===================  Load Config  ======================
    with open('DB_format.csv', 'r', encoding="utf-8") as f_read:
        strContent = f_read.read()
    
    dictSortedDB_items = mySnap7.csv2dict(strContent)
    
    # ===================  Read the whole DB  ======================

    # get the max length(offset value) in datablock
    nLength = mySnap7.get_db_size(dictSortedDB_items, dataTypeKey, offsetKey)
    
    print("nLength: ", nLength)
    # Read the whole db value
    objDB_Results = mySnap7.DBRead(plc, 7, nLength, dictSortedDB_items)

    for tag_name, value in objDB_Results.__dict__.items():
        print(tag_name,": ", value)

    # ===================  Read one single tag from DB ======================
    value = mySnap7.DBReadTag(plc, 7, 0, "Real")
    print("value: ", value)

    value = mySnap7.DBReadTag(plc, 7, 4, "Bool")
    print("value: ", value)
    
    value = mySnap7.DBReadTag(plc, 7, 4.1, "Bool")
    print("value: ", value)

    value = mySnap7.DBReadTag(plc, 7, 6, "Int")
    print("value: ", value)

    value = mySnap7.DBReadTag(plc, 7, 8, "String")
    print("value: ", value)

    value = mySnap7.DBReadTag(plc, 7, 264, "DInt")
    print("value: ", value)

    value = mySnap7.DBReadTag(plc, 7, 268, "UDInt")
    print("value: ", value)

    value = mySnap7.DBReadTag(plc, 7, 272, "Int")
    print("value: ", value)

    value = mySnap7.DBReadTag(plc, 7, 274, "UInt")
    print("value: ", value)

    value = mySnap7.DBReadTag(plc, 7, 276, "SInt")
    print("value: ", value)

    value = mySnap7.DBReadTag(plc, 7, 277, "USInt")
    print("value: ", value)

    value = mySnap7.DBReadTag(plc, 7, 278, "Byte")
    print("value: ", value)

    value = mySnap7.DBReadTag(plc, 7, 280, "DTL")
    print("value: ", value)

    # ===================  Write one single value to DB by tag ======================

    mySnap7.DBWriteByTag(plc, 7, dictSortedDB_items["Temperature"], 1111)
    mySnap7.DBWriteByTag(plc, 7, dictSortedDB_items["Cold"], 1)
    mySnap7.DBWriteByTag(plc, 7, dictSortedDB_items["Hot"], 0)
    mySnap7.DBWriteByTag(plc, 7, dictSortedDB_items["Rpis_to_Buy"], 9)
    mySnap7.DBWriteByTag(plc, 7, dictSortedDB_items["Notes"], "hiHiHi")
    mySnap7.DBWriteByTag(plc, 7, dictSortedDB_items["var_DINT"], -1234567)
    mySnap7.DBWriteByTag(plc, 7, dictSortedDB_items["var_UDINT"], 1234567)
    mySnap7.DBWriteByTag(plc, 7, dictSortedDB_items["var_INT"], -1234)
    mySnap7.DBWriteByTag(plc, 7, dictSortedDB_items["var_UINT"], 1234)
    mySnap7.DBWriteByTag(plc, 7, dictSortedDB_items["var_SINT"], -123)
    mySnap7.DBWriteByTag(plc, 7, dictSortedDB_items["var_USINT"], 123)
    mySnap7.DBWriteByTag(plc, 7, dictSortedDB_items["var_Byte"], 101)
    
    import datetime
    mySnap7.DBWriteByTag(plc, 7, dictSortedDB_items["var_DTL"], datetime.datetime.now())

    # ===================  Write one single value to DB by offset ======================
    mySnap7.DBWriteByOffset(plc, 7, 0, "Real", 1111)
    # mySnap7.DBWriteByOffset(plc, 7, 4, "Bool", 1)
    # mySnap7.DBWriteByOffset(plc, 7, 4.1, "Bool", 0)
    mySnap7.DBWriteByOffset(plc, 7, 6, "Int", 100)
    mySnap7.DBWriteByOffset(plc, 7, 8, "String", "Hello Snap7")
    mySnap7.DBWriteByOffset(plc, 7, 264, "DInt", -765443321)
    mySnap7.DBWriteByOffset(plc, 7, 268, "UDInt", 765443321)
    mySnap7.DBWriteByOffset(plc, 7, 272, "Int", -9876)
    mySnap7.DBWriteByOffset(plc, 7, 274, "UInt", 9876)
    mySnap7.DBWriteByOffset(plc, 7, 276, "SInt", -125)
    mySnap7.DBWriteByOffset(plc, 7, 277, "USInt", 125)
    mySnap7.DBWriteByOffset(plc, 7, 278, "Byte", 100)
    mySnap7.DBWriteByOffset(plc, 7, 280, "DTL", datetime.datetime.now())

    plc.disconnect()