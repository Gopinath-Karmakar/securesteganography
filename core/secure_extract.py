from crypto.aes_cipher import AESCipher
from steganography.extract import extract_data


def secure_extract(image_path, password):
    """
    Extract encrypted message from image
    and decrypt it using AES-256.
    """

    encrypted_message = extract_data(image_path)

    aes = AESCipher(password)

    decrypted_message = aes.decrypt(encrypted_message)

    return decrypted_message