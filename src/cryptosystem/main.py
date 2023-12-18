from src.cryptosystem import utils
from src.cryptosystem.unique_rabin_williams import (
    UniqueRabinWilliamsDecryptor,
    UniqueRabinWilliamsEncryptor,
    UniqueRabinWilliamsKeyGenerator,
)


def main():
    N, p, q, s = UniqueRabinWilliamsKeyGenerator.generate_keys()
    print(f"Generated N: {N}, p: {p}, q: {q}, s: {s}")

    M = 500000  # Example message
    if 0 < M < N / s:
        if utils.is_coprime(M, N):
            D = UniqueRabinWilliamsEncryptor.encrypt(M, N)
            print(f"Encrypted message: {D}")

            decrypted_message = UniqueRabinWilliamsDecryptor.decrypt(D, p, q)
            print(f"Decrypted message: {decrypted_message}")
        else:
            raise ValueError("M and N are not coprime")
    else:
        raise ValueError("M is not in the range (0, N/s)")


if __name__ == "__main__":
    main()
