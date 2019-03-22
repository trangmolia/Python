import psutil
from memory_profiler import memory_usage
import os

from compute_bigdata import heavy_computation

class ProcessPool():
    def __init__(self, min_workers, max_workers, mem_usage, cpu_usage):
        self.min_workers = min_workers
        self.max_workers = max_workers
        self.mem_usage = mem_usage
        self.cpu_usage = cpu_usage

    def process(self, memory_max):
        sum_workers = os.cpu_count()
        if sum_workers < self.min_workers:
            return -1

        result = self.mem_usage / memory_max

        return min(int(result), self.max_workers)

    def map(self, func, data):
        memory_max = memory_usage((func, (data,)), max_usage=True)
        result = ProcessPool.process(self, memory_max[0])

        if result == -1:
            return ("Not enough cells for running multiprocessing")

        return result


if __name__ == "__main__":
    # MB is default unit of mem_usage
    pool = ProcessPool(min_workers=2, max_workers=10, mem_usage=1000, cpu_usage = 0.8)
    data = [i for i in range(10)]
    results = pool.map(heavy_computation, data)

    print(results)

    process_name = "python.exe"
    for proc in psutil.process_iter():
        process = psutil.Process(proc.pid)# Get the process info using PID
        pname = process.name()    # Here is the process name
        if pname == process_name:
            results = pool.map(heavy_computation, data)
            print(process.cpu_percent())