from threading import Thread
import asyncio
import time

def start_thread_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

new_loop = asyncio.new_event_loop()
loop_thread = Thread(target=start_thread_loop, args=(new_loop,))
loop_thread.setDaemon(True)
loop_thread.start()


# 定義一個異步任務
async def do_some_work(x):
    print("waiting... ", x)
    # 模擬io阻塞
    await asyncio.sleep(x)
    return "Done after {}s".format(x)


async def exec_muliTasks(loop):
    """
    :param loop: loop.create_task（需要傳進loop參數）
    :return: None
    """
    coroutine1 = do_some_work(1)
    coroutine2 = do_some_work(2)
    coroutine3 = do_some_work(4)
    
    # 不轉為Task對象 
    # tasks = [
    #     coroutine1,
    #     coroutine2,
    #     coroutine3
    # ]

    # asyncio.ensure_future 轉為Task對象
    tasks = [
        asyncio.ensure_future(coroutine1),
        asyncio.ensure_future(coroutine2),
        asyncio.ensure_future(coroutine3)
    ]
    
    # loop.create_task（需要傳進loop參數）
    # tasks = [
    #     loop.create_task(coroutine1),
    #     loop.create_task(coroutine2),
    #     loop.create_task(coroutine3)
    # ]
    
    # 返回 完成的 task object，需要手動調用task.result()去獲取結果
    dones, pendings = await asyncio.wait(tasks)
    print(dones, pendings)
    for task in dones:
        print("Task ret:", task.result())

    # 返回 task 方法的 返回值，返回值就是 return的結果 ，不用再task.result()來獲取
    # results = await asyncio.gather(*tasks)
    # for result in results:
    #     print("Task ret:",result)


async def exec_coroutine(x):
    print('Number:', x)
    return x

loop = asyncio.get_event_loop()

# ===============================

coroutine1 = exec_coroutine(1)
print('Coroutine1:', coroutine1)
print('After calling exec_coroutine')
loop.run_until_complete(coroutine1)
print('After calling loop\n')

# ===============================
coroutine2 = exec_coroutine(2)
task2 = loop.create_task(coroutine2)
print('Task2:', task2)
loop.run_until_complete(task2)
print('Task2:', task2)

print('After calling loop\n')

# ======================================

coroutine3 = exec_coroutine(3)

print("Coroutine3: ", coroutine3)
print('After calling execute')

task3 = asyncio.ensure_future(coroutine3)
print("Task3: ", task3)
loop.run_until_complete(task3)
print("Task3: ", task3)
print('After calling loop\n')


nStart = time.time()
loop.run_until_complete(exec_muliTasks(loop))
print("Time:", time.time() - nStart)


