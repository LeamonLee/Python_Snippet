import asyncio
from threading import Thread
from collections import deque
import random
import time

def start_thread_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

def consumer():
    while True:
        if dq:
            msg = dq.pop()
            if msg:
                asyncio.run_coroutine_threadsafe(thread_example('Zarten'+ msg), new_loop)


async def thread_example(name):
    print('正在執行name:', name)
    await asyncio.sleep(2)
    return '返回結果：' + name



dq = deque()

# 提示：若想主線程退出時，子線程也隨之退出，需要將子線程設置爲守護線程，函數 setDaemon(True)

new_loop = asyncio.new_event_loop()
loop_thread = Thread(target= start_thread_loop, args=(new_loop,))
loop_thread.setDaemon(True)
loop_thread.start()

consumer_thread = Thread(target= consumer)
consumer_thread.setDaemon(True)
consumer_thread.start()

while True:
    i = random.randint(1, 10)
    dq.appendleft(str(i))
    time.sleep(2)