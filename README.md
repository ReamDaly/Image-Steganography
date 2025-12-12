# Image Steganography with AES Encryption

## Project Overview

This project allows you to hide secret messages inside images using LSB steganography, and also encrypts the message with AES-256 for added security.
It demonstrates the combination of steganography (hiding data) and cryptography (protecting data) in a beginner-friendly Python project.

## Features

- Hide text inside PNG or other lossless image formats.
- Automatically encrypts the message using AES-256 with password-based key derivation (PBKDF2).
- No key files saved - uses password for encryption/decryption.
- Extract and decrypt the hidden message with your password.
- Simple command-line interface (CLI) with secure password input.

## Installation / Setup

1.  **Clone this repository:**

    ```bash
    git clone https://github.com/<your-username>/<repo-name>.git
    cd <repo-name>
    ```

2.  **Install the package:**

    ```bash
    pip install -e .
    ```

    This will install `powder` as a command-line tool along with all dependencies (Pillow, Cryptography).

3.  **Activate your virtual environment (if using one):**

    ```bash
    # On Windows PowerShell
    .\.venv\Scripts\Activate.ps1

    # On Linux/Mac
    source .venv/bin/activate
    ```

## Usage Examples

### 1. Hide a Message (Encrypt)

```bash
powder -e <input_image> <output_image> <password>
```

After running the command, type your message and press **Enter twice** to finish.

**Example:**

```bash
powder -e original.png secret.png mypassword
```

```
Enter your message (press Enter twice to finish):
--------------------------------------------------
This is my secret message!
It can be multiple lines.

✅ Message encrypted & hidden successfully!
Output: secret.png
```

### 2. Extract a Message (Decrypt)

```bash
powder -d <encrypted_image> <password>
```

**Example:**

```bash
powder -d secret.png mypassword
```

```
✅ Decrypted Message:
--------------------------------------------------
This is my secret message!
It can be multiple lines.
--------------------------------------------------
```

## Project Structure

```
image_stego/
│
├── powder.py             # Main CLI tool (command-line interface)
├── encode.py             # Encoding and encryption functions
├── decode.py             # Decoding and decryption functions
├── pyproject.toml        # Package configuration and dependencies
└── README.md             # This file
```

## Dependencies

- Python 3.7+
- Pillow (automatically installed)
- Cryptography (automatically installed)

All dependencies are automatically installed when you run `pip install -e .`

## How It Works

1.  The user inputs a message to hide in an image.
2.  The message is encrypted using AES-256-GCM.
3.  The encrypted message is converted to its binary representation.
4.  The binary message is hidden in the Least Significant Bit (LSB) of the image's color pixels (RGB).
5.  A special marker (`==END==`) is appended to the message to signify the end of the hidden data.
6.  During extraction, the binary data is read from the LSB of each pixel until the end marker is found.
7.  The extracted binary is converted back to text and then decrypted using the provided password.

## Limitations

- Primarily designed for lossless image formats like PNG. Using lossy formats (like JPEG) will corrupt the hidden data.
- The maximum message size is limited by the image's resolution and number of color channels.
- If you forget your password, the hidden message cannot be decrypted.

## Future Work

- A Graphical User Interface (GUI) for easier usage.
- Support for hiding other file types (e.g., PDF, TXT).
- A function to automatically check if an image has enough capacity to hold a given message.
