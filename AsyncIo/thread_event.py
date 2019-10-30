import asyncio
from threading import Thread, Event
import time

now = lambda: time.time()


def start_new_loop(loop, t_stop):
    asyncio.set_event_loop(loop)    
    loop.run_forever()

# XXXXXXXXXXXXXXXXXX 看起來不應該用time.sleep這樣寫 XXXXXXXXXXXXXXXXXXX
def do_work(x):
    print('Do work {}'.format(x))
    time.sleep(x)
    print('Finished synchronous work after {}s'.format(x))

async def do_async_work(x):
    print('Waiting... {}'.format(x))
    await asyncio.sleep(x)
    print('Done asynchronous work after {}s'.format(x))

t_stop = Event()
start = now()
new_loop = asyncio.new_event_loop()

loop_thread = Thread(target=start_new_loop, args=(new_loop, t_stop,))
# loop_thread.setDaemon(True)
loop_thread.start()
print('Created a new event loop with TIME: {}'.format(time.time() - start))

try:
    # task1 = new_loop.call_soon_threadsafe(do_work, 6)
    # task2 = new_loop.call_soon_threadsafe(do_work, 3)
    # print("task1: ", task1)
    # print("task2: ", task2)
    # print('Executed event synchronously...')

    task3 = asyncio.run_coroutine_threadsafe(do_async_work(6), new_loop)
    task4 = asyncio.run_coroutine_threadsafe(do_async_work(4), new_loop)
    print("task3: ", task3)
    print("task4: ", task4)
    print('Executed event asynchronously...')

    while True:
        time.sleep(100)

except KeyboardInterrupt as e:
    print("received KeyboardInterrupt event")

    t_stop.set()

    print("asyncio.Task.all_tasks(): ", asyncio.Task.all_tasks(new_loop))    
    for task in asyncio.Task.all_tasks(new_loop):
        print("task.cancel(): ", task.cancel())
    
    
    new_loop.call_soon_threadsafe(new_loop.stop)

    print("All event loops are closed")

    loop_thread.join()

    print("Goodbye")


