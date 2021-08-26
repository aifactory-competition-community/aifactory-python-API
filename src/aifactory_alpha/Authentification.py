from Cryptodome import Random
from Cryptodome.Cipher import AES
from random import random
from hashlib import blake2b

BLOCK_SIZE=16

class AFCrypto():
    LENGTH_PREFIX = 6
    def __init__(self):
        self.iv = bytes([0x00] * 16) #pycryptodomex 기준

    def encrypt_aes(self, data: str, key: str):
        key += '0'*(16 - (len(key) % 16))
        key = key.encode()
        crypto = AES.new(key, AES.MODE_CBC, self.iv)
        len_data = str(len(data))
        data = len_data.zfill(6) + data
        while len(data) % 16 != 0:
            data += str(int(random()))
        data = data.encode()
        enc = crypto.encrypt(data)
        del crypto
        return enc.hex()

    def decrypt_aes(self, enc: str, key: str):
        key += '0'*(16 - (len(key) % 16))
        key = key.encode()
        crypto = AES.new(key, AES.MODE_CBC, self.iv)
        enc = bytes.fromhex(enc)
        dec = crypto.decrypt(enc).decode()
        len_dec = int(dec[:self.LENGTH_PREFIX])
        dec = dec[self.LENGTH_PREFIX:self.LENGTH_PREFIX+len_dec]
        del crypto
        return dec

    def encrypt_hash(self, data: str):
        return blake2b(data.encode()).hexdigest()



if __name__ == "__main__":
    a = AFCrypto()
    target = "The key is how I think of you."
    sample_key = 'i_love_you_:)'
    print("Target pattern to encrypt: %s" % target)
    print("A key for encryption: %s" % sample_key)
    b = a.encrypt_aes(target, sample_key)
    print("Encrypted Message: %s" % b)
    c = a.decrypt_aes(b, sample_key)
    print("Decrypt again: %s" % c)
