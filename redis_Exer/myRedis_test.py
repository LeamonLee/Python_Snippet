import redis
# 加上decode_responses=True，写入的键值对中的value为str类型，不加这个参数写入的则为字节类型。
pool = redis.ConnectionPool(host='10.101.100.97', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)
# r = redis.Redis(host='10.101.100.97', port=6379, decode_responses=True)

# r.set('gender', 'male')     # key是"gender" value是"male" 将键值对存入redis缓存
print(r.get('EX86.Ex_Main.total_hours'))      # EX86.Ex_Main.total_hours 取出键male对应的值
print(r.mget(['EX86.Ex_Main.LSP', 'EX86.Ex_Main.ser_id']))
