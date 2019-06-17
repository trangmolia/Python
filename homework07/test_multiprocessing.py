import unittest
from multiprocessing import Pool

from parallel_processing import ProcessPool
from compute_data import heavy_computation


class TestProcessPool(unittest.TestCase):

    def test_parallel_processing(self):
        lst = [i for i in range(5)]

        pool = ProcessPool(min_workers=2, max_workers=10, mem_usage=100, cpu_usage=0.8)
        result_1 = pool.map(heavy_computation, lst)
        print('First result: \n', result_1, '\n\n')

        with Pool(3) as p:
           result_2 = (p.map(heavy_computation, lst))
        print('Second result: \n', result_2)
        
        self.assertEqual(result_1, result_2)


if __name__ == '__main__':
    unittest.main()