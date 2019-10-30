from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed, wait, ALL_COMPLETED, FIRST_COMPLETED
import time


def get_html(nSleepTime):
    time.sleep(nSleepTime)
    print("get page {}s finished".format(nSleepTime))
    return nSleepTime

# 建立一個大小為2的執行緒池
thd_pool = ThreadPoolExecutor(max_workers=2)

# 將上個任務提交到執行緒池，因為執行緒池的大小是2，所以必須等task1和task2中有一個完成之後才會將第三個任務提交到執行緒池
task1 = thd_pool.submit(get_html, 3)
task2 = thd_pool.submit(get_html, 1)
task3 = thd_pool.submit(get_html, 1)

# 列印該任務是否執行完畢
print("task1.done(): ", task1.done())

# 只有未被提交的到執行緒池（在等待提交的佇列中）的任務才能夠取消
print("task3.cancel(): ", task3.cancel())

# 休眠4秒鐘之後，執行緒池中的任務全部執行完畢，可以列印狀態
time.sleep(4)
print("task1.done(): ", task1.done())

# 該任務的return 返回值  該方法是阻塞的。
print("task1.result(): ", task1.result())

# =====================================================

urls = [2,1,3]
lstAllTasks = [thd_pool.submit(get_html, url) for url in urls]

for future in as_completed(lstAllTasks):
    data = future.result()
    print("in main: get page {}s success".format(data))

print("main...")

# ======================================================

for data in thd_pool.map(get_html, urls): 
		print("in main: get page {}s success".format(data))

print("main...")

# ======================================================

lstAllTasks = [thd_pool.submit(get_html, url) for url in urls] 
wait(lstAllTasks, return_when=ALL_COMPLETED) 
print("main...")


