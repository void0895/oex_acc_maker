from os import urandom
from eth_keys import keys
import argparse


def gen(filename, num):
    with open(filename, "w") as f:
        for _ in range(num):
            b = urandom(32)
            private_key = keys.PrivateKey(b)
            f.write(str(private_key))
            eth_address = private_key.public_key.to_checksum_address()
            f.write("   ")
            f.write(str(eth_address))
            f.write("\n")


def main():
    parser = argparse.ArgumentParser(
        description='generate eth priv key and eth address\nUsage : python keygen.py filename num_of_keys\npython keygen.py keys.txt 500')
    parser.add_argument('filename', type=str, help="filename")
    parser.add_argument("num", type=int, help="number of keys to generate")
    args = parser.parse_args()
    gen(args.filename, args.num)


main()
