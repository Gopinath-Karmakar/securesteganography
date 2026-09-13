import base64
import hashlib

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


class AESCipher:
    def __init__(self, password):
        self.key = hashlib.sha256(password.encode()).digest()

    def encrypt(self, plaintext):
        iv = get_random_bytes(16)

        cipher = AES.new(
            self.key,
            AES.MODE_CBC,
            iv
        )

        encrypted_data = cipher.encrypt(
            pad(
                plaintext.encode('utf-8'),
                AES.block_size
            )
        )

        return base64.b64encode(
            iv + encrypted_data
        ).decode('utf-8')

    def decrypt(self, ciphertext):
        raw_data = base64.b64decode(ciphertext)

        iv = raw_data[:16]
        encrypted_data = raw_data[16:]

        cipher = AES.new(
            self.key,
            AES.MODE_CBC,
            iv
        )

        decrypted_data = unpad(
            cipher.decrypt(encrypted_data),
            AES.block_size
        )

        return decrypted_data.decode('utf-8')