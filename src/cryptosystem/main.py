from src.cryptosystem import utils
from src.cryptosystem.unique_rabin_williams import UniqueRabinWilliamsKeyGenerator, \
    UniqueRabinWilliamsEncryptor, UniqueRabinWilliamsDecryptor


def main():
    N, p, q = UniqueRabinWilliamsKeyGenerator.generate_keys()
    print(f"Generated N: {N}, p: {p}, q: {q}")

    M = 500000  # Example message
    if utils.is_coprime(M, N):
        D = UniqueRabinWilliamsEncryptor.encrypt(M, N)
        print(f"Encrypted message: {D}")

        decrypted_message = UniqueRabinWilliamsDecryptor.decrypt(D, p, q)
        print(f"Decrypted message: {decrypted_message}")
    else:
        raise ValueError("M and N are not coprime")


if __name__ == "__main__":
    main()
