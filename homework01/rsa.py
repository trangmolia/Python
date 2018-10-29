from math import *

def is_prime(n):
    value = int(sqrt(n))
    for i in range(2,value + 1,1):
        if (n % i == 0):
            return(False)
    return(True)

def gcd(a, b):
    value = min(a,b)
    for i in range (value, 2, -1):
        if (b % i == 0) and (a % i == 0):
            return i
    return 1

def multiplicative_inverse(e, phi):
    i = 1
    while i >= 1:
        value = i*e - 1
        if value % phi == 0:
            return i
        i += 1

def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')

    n = q * p
    phi = (p-1) * (q-1)
    e = random.randrange(1, phi)
    
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    d = multiplicative_inverse(e, phi)
    
    return ((e, n), (d, n))
