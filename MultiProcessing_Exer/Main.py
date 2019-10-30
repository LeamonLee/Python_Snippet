import multiprocessing as mp
import time


def job1(arg1, arg2):
    print("Job1: ", str(arg1+arg2))


def job2(q):
    nRet = 0
    for i in range(1000):
        nRet = i + i**2 + i**3
    q.put(nRet)                 # Queue cannot use return, only can use put() method to store value first, and use get() method to take the data back.


def job3(arg1):
    return arg1 * arg1          # Pool can return the data back directly.


def job4(v, lk, arg1):
    lk.acquire()
    for _ in range(5):
        time.sleep(0.1)
        v.value += arg1
        print("job4:", v.value)
    lk.release()


def job5(nNumbers, arrResult):
    for idx, num in enumerate(nNumbers):
        arrResult[idx] = num * num


if __name__ == "__main__":
    
    '''
    Map-reduce method 
    '''
    pl = mp.Pool()
    lstResult = pl.map(job3, range(10000)) 
    print("Pool Result: ", lstResult)
    # array = [10,20,30,40,50]
    # lstResult = pl.map(job3, array)

    '''
    Only one core will be used
    '''
    async_result = pl.apply_async(job3,(9,))
    print("async_result.get(): ", async_result.get())

    '''
    If you still want to use apply_async() method, 
    and want multi cores to be used at the same time,
    can try the following appraoch.
    '''
    multi_async_result = [pl.apply_async(job3,(i,)) for i in range(10)]
    print("multi_async_result.get(): ",[rst.get() for rst in multi_async_result])

    pl.close()
    pl.join()

    # -----------------------------------------

    q = mp.Queue()
    p1 = mp.Process(target=job1, args=(6,2))
    p2 = mp.Process(target=job2, args=(q,))     # Queue cannot use return, only can use put() method to store value first, and use get() method to take the data back.
    p1.start()
    p2.start()
    p1.join()
    p2.join()

    print("Job2:", q.get())

    # ------------------------------------------

    # Shared memory "Single Value" approach
    vMain = mp.Value('i', 0)
    lk = mp.Lock()
    p3 = mp.Process(target=job4, args=(vMain,lk,5))
    p4 = mp.Process(target=job4, args=(vMain,lk,1))
    p3.start()
    p4.start()
    p3.join()
    p4.join()

    print("vMain.value: ", vMain.value)

    # Shared memory "Array Value" approach
    arrNumbers = [5,10,20]
    arrMainResults = mp.Array('i', 5)
    p5 = mp.Process(target=job5, args=(arrNumbers, arrMainResults))

    p5.start()
    p5.join()

    print(arrMainResults[:])
