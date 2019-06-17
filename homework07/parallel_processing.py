from memory_profiler import memory_usage
import os
from joblib import Parallel, delayed
from compute_data import heavy_computation


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


    def map(self, func, lst):
        max_memory = memory_usage((func, (lst[0],)), max_usage=True)
        n_workers = ProcessPool.find_max_workers(self, max_memory[0])

        if n_workers == -1:
            return ("Not enough cells to running multiprocessing") 
        
        print('Maximum memory a function take %.2f MB' % max_memory[0])

        print('So we can run %s workers at the same time. \n' % n_workers) 
        
        results = Parallel(n_jobs=n_workers)(delayed(heavy_computation)(lst[i], id) for i in range(len(lst)))
        
        return results


if __name__ == "__main__":
    # MB is default unit of mem_usage
    pool = ProcessPool(min_workers=2, max_workers=10, mem_usage=120, cpu_usage=0.8)
    lst = [1]*5
    results = pool.map(heavy_computation, lst)
    print(results)
    