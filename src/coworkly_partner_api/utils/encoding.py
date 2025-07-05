"""URL encryption utilities for partner registration flow using Fernet."""

import os
from typing import Optional
from cryptography.fernet import Fernet, InvalidToken
from .config import settings


# Get the encryption key from environment variable
# You should set this in your environment: FERNET_KEY=your_generated_key
FERNET_KEY = settings.FERNET_KEY
if not FERNET_KEY:
    # Fallback for development - generate a key if not set
    # In production, always set FERNET_KEY environment variable
    FERNET_KEY = Fernet.generate_key().decode()
    print(f"WARNING: FERNET_KEY not set. Generated temporary key: {FERNET_KEY}")

# Initialize Fernet cipher
try:
    cipher = Fernet(FERNET_KEY.encode())
except Exception as e:
    raise ValueError(f"Invalid FERNET_KEY: {e}")


def encrypt_for_url(data: str) -> str:
    """Encrypt data for safe use in URL parameters using Fernet."""
    if not data:
        return ""
    try:
        encrypted = cipher.encrypt(data.encode('utf-8'))
        return encrypted.decode('utf-8')
    except Exception as e:
        raise ValueError(f"Encryption failed: {e}")


def decrypt_from_url(encrypted_data: str) -> Optional[str]:
    """Decrypt data from Fernet encryption."""
    if not encrypted_data:
        return None
    
    try:
        decrypted = cipher.decrypt(encrypted_data.encode('utf-8'))
        return decrypted.decode('utf-8')
    except InvalidToken:
        # Invalid or tampered token
        print(f"Invalid token: {encrypted_data}")
        return None
    except Exception as e:
        # Other decryption errors
        print(f"Other decryption errors: {e}")
        return None


def encrypt_space_id(space_id: str) -> str:
    """Encrypt space ID for URL parameter 'a'."""
    return encrypt_for_url(space_id)


def encrypt_email(email: str) -> str:
    """Encrypt email for URL parameter 'b'."""
    return encrypt_for_url(email)


def decrypt_space_id(encrypted_space_id: str) -> Optional[str]:
    """Decrypt space ID from URL parameter 'a'."""
    return decrypt_from_url(encrypted_space_id)


def decrypt_email(encrypted_email: str) -> Optional[str]:
    """Decrypt email from URL parameter 'b'."""
    return decrypt_from_url(encrypted_email)


# Utility function to generate a new key (run this once to get your key)
def generate_fernet_key() -> str:
    """Generate a new Fernet key for use in environment variables."""
    return Fernet.generate_key().decode() 