import math
import random
from math import gcd

from sympy import isprime
from src.log_config import logging
logger = logging.getLogger(__name__)


def generate_prime(mod4: int) -> int:
    """
    Generate a prime number p such that p ≡ mod4 (mod 4).
    """
    while True:
        p = random.randint(2**10, 2**11)  # or a suitable range
        if p % 4 == mod4 and isprime(p):
            return p


def chrem(R: list[int], M: list[int]) -> int:
    """
    @param R: list of residue
    @param M: list of moduli
    Solve the congruence equations:
    X[i] ≡ R[i] (mod M[i])
    Usage:
    >>> chrem([2, 3, 2], [3, 5, 7])
    23
    """
    logger.debug(f"R: {R}")
    logger.debug(f"M: {M}")
    assert len(R) == len(M)
    n = len(R)
    M_prod = 1
    for i in range(n):
        M_prod *= M[i]
    M_i = [M_prod // M[i] for i in range(n)]
    logger.debug(f"M_i: {M_i}")
    M_i_inv = [pow(M_i[i], -1, M[i]) for i in range(n)]
    logger.debug(f"M_i_inv: {M_i_inv}")
    X = 0
    for i in range(n):
        logger.debug(f"i: {i}, R[i]: {R[i]}, M_i[i]: {M_i[i]}, M_i_inv[i]: {M_i_inv[i]}")
        X += R[i] * M_i[i] * M_i_inv[i]
        logger.debug(f"X: {X}")
    return X % M_prod


def is_coprime(a: int, b: int) -> bool:
    return gcd(a, b) == 1


def quadratic_residue(a: int, p: int) -> bool:
    """
    Returns True if a is a quadratic residue mod p.
    """
    return pow(a, (p - 1) // 2, p) == 1


def legendre_symbol(a: int, p: int) -> int:
    if math.gcd(a, p) != 1:
        return 0
    if quadratic_residue(a, p):
        return 1
    else:
        return -1
