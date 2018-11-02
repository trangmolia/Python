from math import sqrt
import random


def is_prime(n):
    value = int(sqrt(n))
    for i in range(2, value + 1, 1):
        if n % i == 0:
            return False
    return True


def multiplicative_inverse(e, phi):
    s1, s2 = 1, 0
    t1, t2 = 0, 1
    while phi != 0:
        q = e // phi
        r = e % phi
        e, phi = phi, r
        s = s1 - q * s2
        s1, s2 = s2, s
        t = t1 - q * t2
        t1, t2 = t2, t
    return s1 % s2


def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')

    # n = pq
    n = p * q

    # phi = (p-1)(q-1)
    phi = (p - 1) * (q - 1)

    # Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)

    # Use Euclid's Algorithm to verify that e and phi(n) are comprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)
    # Return public and private keypair
    # Public key is (e, n) and private key is (d, n)
    return (e, n), (d, n)
