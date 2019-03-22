import math


def IsPrime(n: int) -> bool:
    if n == 0 or n == 1:
        return False

    if n == 2 or n == 3:
        return True

    flag = int(math.sqrt(n))
    for number in range(2, flag + 1):
        if n % number == 0:
            return False

    return True


def heavy_computation(data_chunk):
    # value = times to find all prime numbers within range 10000000
    for value in data_chunk:
        for _ in range(value + 1):
            prime_number_list = []
            for number in range(1000000):
                if IsPrime(number):
                    prime_number_list.append(number)
