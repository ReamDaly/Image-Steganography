from PIL import Image
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
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


def aes_decrypt(encoded_data, password):
    """Decrypt a message using AES-256-GCM with password-derived key."""
    data = base64.b64decode(encoded_data)
    
    salt = data[:16]
    nonce = data[16:28]
    ciphertext = data[28:]
    
    key = derive_key_from_password(password, salt)
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)

    return plaintext.decode()


def bits_to_message(bits):
    """Convert binary representation to a message string."""
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        chars.append(chr(int(byte, 2)))
    return ''.join(chars)


def decode_image(image_path):
    """Extract hidden message from an image using LSB steganography."""
    img = Image.open(image_path)
    width, height = img.size

    bits = ""

    for y in range(height):
        for x in range(width):
            pixel = img.getpixel((x, y))
            for i in range(3):
                bits += str(pixel[i] & 1)

    extracted = bits_to_message(bits)

    return extracted.split("==END==")[0]
