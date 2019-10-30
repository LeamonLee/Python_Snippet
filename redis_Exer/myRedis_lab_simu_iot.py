import redis
import csv
import os

# 加上decode_responses=True，写入的键值对中的value为str类型，不加这个参数写入的则为字节类型。
pool = redis.ConnectionPool(host='10.101.100.97', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)

_r_filename = os.getcwd() + "/Ex_Main.csv"
_w_filename = os.getcwd() + "/Ex_Main_readFromRedis.csv"
strPrefix = "EX86.Ex_Main."

try:
    with open(_r_filename, 'r') as _read_f:
        _csv_reader = csv.DictReader(_read_f)
        with open(_w_filename, 'w') as _write_f:
            _fieldnames = ['Tag', 'Value']
            _csv_writer = csv.DictWriter(_write_f, fieldnames=_fieldnames, delimiter=',')
            _csv_writer.writeheader()
            for row in _csv_reader:
                _keyName = strPrefix + row["name"]
                print(_keyName + ': ', r.get(_keyName))
                _csv_writer.writerow({"Tag": _keyName, 
                                    "Value": r.get(_keyName)})
except Exception as e:
    print("Exception occurred")
    print(e)        

finally:
    print("Job Done!")

# print(r.mget(['EX86.Ex_Main.LSP', 'EX86.Ex_Main.ser_id']))
