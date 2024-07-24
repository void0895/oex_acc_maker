from os import urandom
from eth_keys import keys


with open("keys.txt", "w") as f:
    for _ in range(100):
        b = urandom(32)
        private_key = keys.PrivateKey(b)
        f.write(str(private_key))
        eth_address = private_key.public_key.to_checksum_address()
        f.write("   ")
        f.write(str(eth_address))
        f.write("\n")
