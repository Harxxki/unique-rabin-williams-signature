# from random import randint
from typing import Tuple
from ..log_config import logging

from utils import chrem, generate_prime
logger = logging.getLogger(__name__)


class UniqueRabinWilliamsKeyGenerator:
    @staticmethod
    def generate_keys() -> Tuple[int, int, int, int]:
        p = generate_prime(3)
        q = generate_prime(3)
        # s = randint(2, int(q**0.5))
        s = 2  # とりあえず2に固定
        N = p**2 * q
        return N, p, q, s


class UniqueRabinWilliamsEncryptor:
    @staticmethod
    def encrypt(M: int, N: int) -> int:
        return pow(M, 2, N)


class UniqueRabinWilliamsDecryptor:
    @staticmethod
    def decrypt(D: int, p: int, q: int) -> int:
        R1 = pow(D, (p + 1) // 4, p)
        R2 = pow(D, (q + 1) // 4, q)
        logger.debug(f"R1: {R1}, R2: {R2}")
        M = [chrem([R1, R2], [p, q]), chrem([R1, -R2], [p, q]), chrem([-R1, R2], [p, q]), chrem([-R1, -R2], [p, q])]
        logger.debug(f"M: {M}")
        print()
        return min(M)
