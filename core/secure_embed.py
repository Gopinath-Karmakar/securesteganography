from crypto.aes_cipher import AESCipher
from steganography.embed import embed_data


def secure_embed(image_path, message, password, output_path):
    """
    Encrypt the message using AES-256 and embed it
    into the cover image using LSB steganography.
    """

    aes = AESCipher(password)

    encrypted_message = aes.encrypt(message)

    embed_data(
        image_path=image_path,
        secret_data=encrypted_message,
        output_path=output_path
    )

    return True