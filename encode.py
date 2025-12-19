from PIL import Image
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import os
import base64


def derive_key_from_password(password, salt):
    """Derive a 256-bit key from password using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return kdf.derive(password.encode())


def aes_encrypt(message, password):
    """Encrypt a message using AES-256-GCM with password-derived key."""
    salt = os.urandom(16)
    key = derive_key_from_password(password, salt)
    
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, message.encode(), None)

    # Combine salt + nonce + ciphertext and encode
    return base64.b64encode(salt + nonce + ciphertext).decode()


def message_to_bits(message):
    """Convert a message string to binary representation."""
    return ''.join([format(ord(c), '08b') for c in message])


def encode_image(input_image, encrypted_message, output_image):
    """Hide encrypted message in an image using LSB steganography."""
    img = Image.open(input_image)
    encoded = img.copy()
    width, height = img.size

    encrypted_message += "==END=="
    message_bits = message_to_bits(encrypted_message)

    bit_index = 0
    total_bits = len(message_bits)

    for y in range(height):
        for x in range(width):
            pixel = list(img.getpixel((x, y)))

            for i in range(3):  # modify R, G, B
                if bit_index < total_bits:
                    pixel[i] = pixel[i] & ~1 | int(message_bits[bit_index])
                    bit_index += 1

            encoded.putpixel((x, y), tuple(pixel))

            if bit_index >= total_bits:
                encoded.save(output_image)
                return True

    raise ValueError("Image too small to hold encrypted message")