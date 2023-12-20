# from random import randint
from typing import Tuple

from src.utils import chrem, generate_prime

from ..log_config import logging

logger = logging.getLogger(__name__)


class UniqueRabinWilliamsSigner:
    def __init__(self, p: int, q: int, s: int):
        self.p = p
        self.q = q
        self.N = p * p * q
        self.s = s

    def sign(self, M: int) -> int:
        # if not 0 < M < self.N / self.s:
        #     raise ValueError("M must be in the range (0, N/s).")
        return self._sign(M)

    def _sign(self, M: int) -> int:
        _signature = pow(M, 2, self.p * self.q)
        logger.debug(f"_signature: {_signature}")
        R1 = pow(_signature, (self.p + 1) // 4, self.p)
        R2 = pow(_signature, (self.q + 1) // 4, self.q)
        logger.debug(f"R1: {R1}, R2: {R2}")
        _signatures = chrem([R1, R2], [self.p, self.q]), chrem([R1, -R2], [self.p, self.q]), \
            chrem([-R1, R2], [self.p, self.q]), chrem([-R1, -R2], [self.p, self.q])
        logger.debug(f"_signatures: {_signatures}")
        logger.debug(f"min(_signatures): {min(_signatures)}")
        return min(_signatures)


class UniqueRabinWilliamsVerifier:
    @staticmethod
    def verify(signature: int, p: int, q: int, M: int) -> bool:
        _M = pow(signature, 2, p * p * q)
        logger.debug(f"p^2 * q: {p * p * q}")
        logger.debug(f"_M = signature ^2 mod p^2*q = {signature}^2 mod {p * p * q} = {_M}")
        return _M == M


class UniqueRabinWilliamsKeyGenerator:
    @staticmethod
    def generate_keys() -> Tuple[int, int, int, int]:
        p = generate_prime(3)
        q = generate_prime(3)
        # s = randint(2, int(q**0.5))
        s = 2  # とりあえず2に固定
        N = p ** 2 * q
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
        M = [chrem([R1, R2], [p, q]), chrem([R1, -R2], [p, q]), chrem([-R1, R2], [p, q]),
             chrem([-R1, -R2], [p, q])]
        logger.debug(f"M: {M}")
        print()
        return min(M)
