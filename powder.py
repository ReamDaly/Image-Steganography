#!/usr/bin/env python3
"""
Powder - Image Steganography Tool
Hide and extract encrypted messages in images
"""

import sys
from encode import encode_image, aes_encrypt
from decode import decode_image, aes_decrypt


def print_usage():
    """Print usage instructions."""
    print("Usage:")
    print("  Encrypt: powder -e <input_image> <output_image> <password>")
    print("  Decrypt: powder -d <encrypted_image> <password>")
    print()
    print("Examples:")
    print("  powder -e original.png secret.png mypassword")
    print("  powder -d secret.png mypassword")
    sys.exit(1)


def encrypt_mode(input_image, output_image, password):
    """Encrypt and hide message in image."""
    print("Enter your message (press Enter twice to finish):")
    print("-" * 50)
    
    lines = []
    while True:
        line = input()
        if line == "" and len(lines) > 0 and lines[-1] == "":
            lines.pop()  # Remove last empty line
            break
        lines.append(line)
    
    message = "\n".join(lines)
    
    if not message:
        print("❌ Error: No message provided")
        sys.exit(1)
    
    try:
        # Encrypt message with password
        encrypted_message = aes_encrypt(message, password)
        
        # Hide encrypted message in image
        encode_image(input_image, encrypted_message, output_image)
        
        print("\n✅ Message encrypted & hidden successfully!")
        print(f"Output: {output_image}")
    except FileNotFoundError:
        print(f"❌ Error: Image file '{input_image}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def decrypt_mode(encrypted_image, password):
    """Extract and decrypt message from image."""
    try:
        encrypted_msg = decode_image(encrypted_image)
        decrypted = aes_decrypt(encrypted_msg, password)
        
        print("\n✅ Decrypted Message:")
        print("-" * 50)
        print(decrypted)
        print("-" * 50)
    except FileNotFoundError:
        print(f"❌ Error: Image file '{encrypted_image}' not found")
        sys.exit(1)
    except Exception:
        print("❌ Error: Wrong password or corrupted data")
        sys.exit(1)


def main():
    """Main entry point."""
    if len(sys.argv) < 3:
        print_usage()
    
    mode = sys.argv[1]
    
    if mode == "-e":
        if len(sys.argv) != 5:
            print("❌ Error: Encrypt mode requires 3 arguments")
            print_usage()
        
        input_image = sys.argv[2]
        output_image = sys.argv[3]
        password = sys.argv[4]
        
        encrypt_mode(input_image, output_image, password)
    
    elif mode == "-d":
        if len(sys.argv) != 4:
            print("❌ Error: Decrypt mode requires 2 arguments")
            print_usage()
        
        encrypted_image = sys.argv[2]
        password = sys.argv[3]
        
        decrypt_mode(encrypted_image, password)
    
    else:
        print(f"❌ Error: Unknown mode '{mode}'")
        print_usage()


if __name__ == "__main__":
    main()
