import argparse

from sympy import isprime

from src.cryptosystem import utils
from src.cryptosystem.unique_rabin_williams import (
    UniqueRabinWilliamsDecryptor,
    UniqueRabinWilliamsEncryptor,
    UniqueRabinWilliamsKeyGenerator,
)


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
    if not 0 < M < N / s:
        raise ValueError("M must be in the range (0, N/s).")
    if not utils.is_coprime(M, N):
        raise ValueError("M and N must be coprime.")
    return True


def main():
    args = parse_arguments()

    if args.p and args.q and args.s and args.M:
        p, q, s, M = args.p, args.q, args.s, args.M
        validate_inputs(p, q, s, M)
        N = p * q * q
    else:
        N, p, q, s = UniqueRabinWilliamsKeyGenerator.generate_keys()
        M = 500000  # Example message
        print(f"Generated N: {N}, p: {p}, q: {q}, s: {s}")

    D = UniqueRabinWilliamsEncryptor.encrypt(M, N)
    print(f"Encrypted message: {D}")

    decrypted_message = UniqueRabinWilliamsDecryptor.decrypt(D, p, q)
    print(f"Decrypted message: {decrypted_message}")


if __name__ == "__main__":
    main()
