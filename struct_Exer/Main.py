import struct
import sys

byte_arr = bytearray(b'\x06\x00\x00\x00')
print(byte_arr)
print("type(byte_arr): ", type(byte_arr))
x = byte_arr[0:4]
print(x)

bytesPacked_data = struct.pack('4B', *x)
print(bytesPacked_data)
print(bytesPacked_data.decode("utf-8"))
print("type(struct.pack('4B', *x)): ", type(bytesPacked_data))
print("type(struct.pack('4B', *x).decode('utf-8')): ", type(bytesPacked_data.decode("utf-8")))
print(struct.calcsize('4B'))

print(struct.unpack('4b',struct.pack('4B', *x)))
print(struct.unpack('4B',struct.pack('4B', *x)))
print(struct.unpack('>i',struct.pack('4B', *x)))
print(struct.unpack('>I',struct.pack('4B', *x)))
print(struct.unpack('<i',struct.pack('4B', *x)))

# packed_data = struct.pack('iif', 6, 105, 1.11)
packed_data = struct.pack('4i', 6,10, 30, 49)
print("struct.pack(), packed_data: ", packed_data)
print("struct.pack(), bytearray(packed_data0: ", bytearray(packed_data))
# print("struct.pack(), packed_data.decode('utf-8'): ", packed_data.decode("utf-8"))

print("struct.calcsize('i'): ",struct.calcsize('i'))
print("struct.calcsize('f'): ",struct.calcsize('f'))

origin_data = struct.unpack('iif', packed_data)
print("struct.unpack(), origin_data: ", origin_data)

print("sys.byteorder: ", sys.byteorder)

print('='*50)


fd_out = open("myBin_File", 'wb')

# [2-byte ID][4-byte value]...

id = 0
val = id

for i in range(50):
    entry = struct.pack('<HI', id, val)
    id+=1
    val = id

    fd_out.write(entry)
    fd_out.flush()

fd_out.close()