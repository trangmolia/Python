import math
import os


def is_prime(n: int) -> bool:
    if n == 0 or n == 1:
        return False

    if n == 2 or n == 3:
        return True

    flag = int(math.sqrt(n))
    for number in range(2, flag + 1):
        if n % number == 0:
            return False

    return True


def heavy_computation(data_chunk, id=-1):
    # print(os.getpid(),"working")
    # while (not queue.empty()):
    #     data_chunk = queue.get()
    # print(os.getpid(), "got", id)
    result = []
    for _ in range(data_chunk):
        prime_number_list = []
        for number in range(10):
            if is_prime(number):
                prime_number_list.append(number)
        result.append(prime_number_list)
    return result
