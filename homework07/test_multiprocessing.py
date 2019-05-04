import unittest
from tracking_memory import ProcessPool
from compute_data import heavy_computation

class TestProcessPool(unittest.TestCase):

    def test_max_workers(self):
        pool = ProcessPool(min_workers=2, max_workers=10, mem_usage=1000, cpu_usage=0.8)
        data = [i for i in range(10)]
        result = pool.map(heavy_computation, data)
        self.assertEqual(10, result)


if __name__ == '__main__':
    unittest.main()