import asyncio
import random


async def coro(tag):
    print(">", tag)
    await asyncio.sleep(random.uniform(0.5, 5))
    print("<", tag)
    return tag


loop = asyncio.get_event_loop()

tasks = [coro(i) for i in range(1, 11)]

# 第一次wait 完成情況
print("Get first result:")
finished1, unfinished1 = loop.run_until_complete(
    asyncio.wait(tasks, return_when = asyncio.FIRST_COMPLETED)) # 第一個任務完全返回

for task in finished1:
    print("finished1: ", task.result())
print("unfinished1:", len(unfinished1))

# 繼續第一次未完成任務
print("Get more results in 2 seconds:")
finished2, unfinished2 = loop.run_until_complete(
    asyncio.wait(unfinished1, timeout=2)) # 超時2s 返回

for task in finished2:
    print("finished2: ", task.result())
print("unfinished2:", len(unfinished2))

# 繼續第2次未完成任務
print("Get all other results:")
finished3, unfinished3 = loop.run_until_complete(asyncio.wait(unfinished2)) # ALL_COMPLETED：所有任務完成返回 （默認項）

for task in finished3:
    print("finished3: ", task.result())

loop.close()