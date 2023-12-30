import argparse
import pprint
from tabulate import tabulate

from sympy import isprime

from src import utils
import logging
from src.signature.unique_rabin_williams import (
    UniqueRabinWilliamsSigner,
    UniqueRabinWilliamsVerifier,
)
from src.utils import legendre_symbol

from src.experiment.log_config import setup_logger

logger = setup_logger(__file__)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Unique Rabin-Williams Cryptosystem")
    parser.add_argument("--p", type=int, help="Prime number p")
    parser.add_argument("--q", type=int, help="Prime number q")
    parser.add_argument("--s", type=int, help="Integer s")
    return parser.parse_args()


def create_plaintext_space(p: int, q: int) -> list[int]:
    N = p * q * q
    logger.debug(f"Creating plaintext space for p: {p}, q: {q}, N: {N}...")
    plaintexts = []
    upper = min(N, 100000)
    logger.debug(f"Upper: {upper}")
    for M in range(1, upper):
        if legendre_symbol(M, p) == 1 and legendre_symbol(M, q) == 1 and utils.is_coprime(M, N):
            # logger.debug(f"Found M: {M}")
            plaintexts.append(M)
        if M % 1000000 == 0:
            logger.debug(f"Progress: Checking M = {M} / {upper}")
    logger.debug(f"Plaintext space: {plaintexts}")
    return plaintexts


def validate_inputs(p: int, q: int, s: int, M: int) -> bool:
    if not isprime(p) or not isprime(q):
        raise ValueError("Both p and q must be prime numbers.")
    if p % 4 != 3 or q % 4 != 3:
        raise ValueError("Both p and q must be congruent to 3 mod 4.")
    if not 1 < s < q ** 0.5:
        raise ValueError("s must be greater than 1 and less than sqrt(q).")
    return True


def main():
    args = parse_arguments()
    p = args.p or 1187
    q = args.q or 2351
    s = args.s or 4
    validate_inputs(p, q, s, 0)
    logger.debug("params are valid")

    plaintexts = create_plaintext_space(p, q)
    results_all = []
    results_valid = []

    for M in plaintexts:
        # logger.debug(f"Signing M: {M}...")
        try:
            signer = UniqueRabinWilliamsSigner(p=p, q=q, s=s)
            signature = signer.sign(M=M)
            verifier = UniqueRabinWilliamsVerifier()
            verification = verifier.verify(signature=signature, p=p, q=q, M=M)
            logger.debug(f"M: {M}, Signature: {signature}, Verification: {verification}")
            results_all.append({"M": M, "Signature": signature, "Verification": verification})
            if verification:
                results_valid.append(
                    {f"M: {M}, Signature: {signature}, Verification: {verification}"})
        except ValueError as e:
            logger.error(e)

    # pprint.pprint(results)
    # logger.info(results)
    # print(tabulate(results, headers="keys", tablefmt="latex"))
    logger.info(f"All signatures:")
    logger.info(tabulate(results_all, headers="keys", tablefmt="latex"))
    logger.info(f"All signatures: {len(results_all)}")
    logger.info(f"Valid signatures:")
    logger.info(tabulate(results_valid, headers="keys", tablefmt="latex"))
    logger.info(f"Valid signatures: {len(results_valid)} / {len(results_all)}")


if __name__ == "__main__":
    main()
