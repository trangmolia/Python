from memory_profiler import memory_usage
import os
from multiprocessing import Process, Queue

from compute_data import heavy_computation


queue = Queue()

class ProcessPool():
    def __init__(self, min_workers, max_workers, mem_usage, cpu_usage):
        self.min_workers = min_workers
        self.max_workers = max_workers
        self.mem_usage = mem_usage
        self.cpu_usage = cpu_usage

    def find_max_workers(self, max_memory):
        sum_workers = os.cpu_count()
        if sum_workers < self.min_workers:
            return -1

        return min(int(self.mem_usage / max_memory), self.max_workers)


    def map(self, func, data):
        queue.put(data[0])
        memory_max = memory_usage((func, (queue,)), max_usage=True)
        workers = ProcessPool.find_max_workers(self, memory_max[0])

        if workers == -1:
            return ("Not enough cells to running multiprocessing") 

        print('Can run %s workers at the same time.' % workers, '\n')

        # clear all jobs from queue
        while not queue.empty():
            queue.get()

        # put jobs into queue
        for job in(data[1:]):
            queue.put(job)

        processes = [Process(target=func, args=(queue,)) for _ in range(workers)]

        for process in processes:
            process.start()

        for process in processes:
            process.join() 
    
        results = [queue.get() for p in processes]
        print(results)

        return queue


if __name__ == "__main__":
    # MB is default unit of mem_usage
    pool = ProcessPool(min_workers=2, max_workers=10, mem_usage=100, cpu_usage=0.8)
    data = [i for i in range(5)]
    # heavy_computation(1) <= in parallel (1 GB)
    # heavy_computation(2) <= in parallel (1 GB)
    # ...
    # results = pool.map(lambda x: x*x, [1,2,3,4,5,6]) # [1 4 9 16 25 36]
    pool.map(heavy_computation, data)
    