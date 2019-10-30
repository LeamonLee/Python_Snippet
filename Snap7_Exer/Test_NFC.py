import snap7.client
import mySnap7, byte_array


nameKey = "name"
dataTypeKey = "datatype"
offsetKey = "offset"

if __name__ == "__main__":
    
    # ===================  Connection  ======================
    plc = snap7.client.Client()
    plc.connect('10.101.100.41', 0, 0)

    # ===================  Load Config  ======================
    with open('NFC_DB_format.csv', 'r', encoding="utf-8") as f_read:
        strContent = f_read.read()
    
    dictSortedDB_items = mySnap7.csv2dict(strContent)
    
    # ===================  Read the whole DB  ======================

    # get the max length(offset value) in datablock
    nLength = mySnap7.get_db_size(dictSortedDB_items, dataTypeKey, offsetKey)
    
    print("nLength: ", nLength)
    # Read the whole db value
    objDB_Results = mySnap7.DBRead(plc, 1, nLength, dictSortedDB_items)

    for tag_name, value in objDB_Results.__dict__.items():
        print(tag_name,": ", value)

    

    plc.disconnect()