import argparse

from sympy import isprime

from src import utils
from src.log_config import logging
from src.signature.unique_rabin_williams import (
    UniqueRabinWilliamsKeyGenerator,
    UniqueRabinWilliamsSigner,
    UniqueRabinWilliamsVerifier,
)

logger = logging.getLogger(__name__)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Unique Rabin-Williams Cryptosystem")
    parser.add_argument("--p", type=int, help="Prime number p")
    parser.add_argument("--q", type=int, help="Prime number q")
    parser.add_argument("--s", type=int, help="Integer s")
    parser.add_argument("--M", type=int, help="Message M")
    return parser.parse_args()


def validate_inputs(p: int, q: int, s: int, M: int) -> bool:
    if not isprime(p) or not isprime(q):
        raise ValueError("Both p and q must be prime numbers.")
    if p % 4 != 3 or q % 4 != 3:
        raise ValueError("Both p and q must be congruent to 3 mod 4.")
    if not 1 < s < q**0.5:
        raise ValueError("s must be greater than 1 and less than sqrt(q).")
    N = p * p * q
    if utils.legendre_symbol(M, p) * utils.legendre_symbol(M, q) != 1:
        raise ValueError(f"M({M}) must be a quadratic residue mod pq({p*q}).")
    if not utils.is_coprime(M, N):
        raise ValueError("M and N must be coprime.")
    return True


def main():
    args = parse_arguments()

    if args.p and args.q and args.s and args.M:
        p, q, s, M = args.p, args.q, args.s, args.M
        validate_inputs(p, q, s, M)
        logger.debug("params are valid")
        N = p * q * q
        print(f"Inputs: N: {N}, p: {p}, q: {q}, s: {s}, M: {M}")
    else:
        N, p, q, s = UniqueRabinWilliamsKeyGenerator.generate_keys()
        M = 500000  # Example message
        print(f"Generated N: {N}, p: {p}, q: {q}, s: {s}, M: {M}")

    signer = UniqueRabinWilliamsSigner(p=p, q=q, s=s)
    signature = signer.sign(M=M)
    print(f"Signature: {signature}")

    verifier = UniqueRabinWilliamsVerifier()
    verification = verifier.verify(signature=signature, p=p, q=q, M=M)
    print(f"Verification: {verification}")


if __name__ == "__main__":
    main()
