"""Tests for URL encryption utilities."""

import pytest
import os
from unittest.mock import patch
from cryptography.fernet import Fernet


class TestURLEncryption:
    """Test cases for URL encryption utilities."""
    
    @patch.dict(os.environ, {"FERNET_KEY": ""})
    def test_encrypt_decrypt_basic(self):
        """Test basic encrypt/decrypt functionality."""
        # Set a valid Fernet key for testing
        test_key = Fernet.generate_key().decode()
        
        with patch.dict(os.environ, {"FERNET_KEY": test_key}):
            # Import after setting environment variable
            from src.coworkly_partner_api.utils.encoding import (
                encrypt_for_url, decrypt_from_url
            )
            
            original = "space123"
            encrypted = encrypt_for_url(original)
            decrypted = decrypt_from_url(encrypted)
            
            assert decrypted == original
            assert encrypted != original  # Should be different
            assert len(encrypted) > len(original)  # Encrypted should be longer
    
    @patch.dict(os.environ, {"FERNET_KEY": ""})
    def test_encrypt_decrypt_email(self):
        """Test email encryption/decryption."""
        # Set a valid Fernet key for testing
        test_key = Fernet.generate_key().decode()
        
        with patch.dict(os.environ, {"FERNET_KEY": test_key}):
            # Import after setting environment variable
            from src.coworkly_partner_api.utils.encoding import (
                encrypt_email, decrypt_email
            )
            
            email = "partner@example.com"
            encrypted = encrypt_email(email)
            decrypted = decrypt_email(encrypted)
            
            assert decrypted == email
    
    @patch.dict(os.environ, {"FERNET_KEY": ""})
    def test_encrypt_decrypt_space_id(self):
        """Test space ID encryption/decryption."""
        # Set a valid Fernet key for testing
        test_key = Fernet.generate_key().decode()
        
        with patch.dict(os.environ, {"FERNET_KEY": test_key}):
            # Import after setting environment variable
            from src.coworkly_partner_api.utils.encoding import (
                encrypt_space_id, decrypt_space_id
            )
            
            space_id = "space_abc123"
            encrypted = encrypt_space_id(space_id)
            decrypted = decrypt_space_id(encrypted)
            
            assert decrypted == space_id
    
    def test_decrypt_invalid_data(self):
        """Test decrypting invalid data returns None."""
        from src.coworkly_partner_api.utils.encoding import decrypt_from_url
        result = decrypt_from_url("invalid_encrypted_data!")
        assert result is None
    
    def test_decrypt_empty_data(self):
        """Test decrypting empty data returns None."""
        from src.coworkly_partner_api.utils.encoding import decrypt_from_url
        result = decrypt_from_url("")
        assert result is None
    
    def test_encrypt_empty_data(self):
        """Test encrypting empty data returns empty string."""
        from src.coworkly_partner_api.utils.encoding import encrypt_for_url
        result = encrypt_for_url("")
        assert result == ""
    
    @patch.dict(os.environ, {"FERNET_KEY": ""})
    def test_url_safe_characters(self):
        """Test that encrypted data is URL-safe."""
        # Set a valid Fernet key for testing
        test_key = Fernet.generate_key().decode()
        
        with patch.dict(os.environ, {"FERNET_KEY": test_key}):
            # Import after setting environment variable
            from src.coworkly_partner_api.utils.encoding import encrypt_for_url
            
            original = "test data with spaces and symbols!@#"
            encrypted = encrypt_for_url(original)
            
            # Should not contain problematic URL characters
            assert " " not in encrypted  # No spaces
            assert "?" not in encrypted  # No query delimiters
            assert "&" not in encrypted  # No parameter separators
            assert "=" not in encrypted  # No assignment operators
    
    @patch.dict(os.environ, {"FERNET_KEY": ""})
    def test_real_world_example(self):
        """Test with a realistic example."""
        # Set a valid Fernet key for testing
        test_key = Fernet.generate_key().decode()
        
        with patch.dict(os.environ, {"FERNET_KEY": test_key}):
            # Import after setting environment variable
            from src.coworkly_partner_api.utils.encoding import (
                encrypt_email, decrypt_email,
                encrypt_space_id, decrypt_space_id
            )
            
            email = "john.doe@coworkly.com"
            space_id = "space_downtown_001"
            
            # Encrypt
            encrypted_email = encrypt_email(email)
            encrypted_space_id = encrypt_space_id(space_id)
            
            # Decrypt
            decrypted_email = decrypt_email(encrypted_email)
            decrypted_space_id = decrypt_space_id(encrypted_space_id)
            
            # Verify
            assert decrypted_email == email
            assert decrypted_space_id == space_id
            
            # Verify URL format
            url = f"http://localhost:8080/register?spaceName=CoWorkly&a={encrypted_space_id}&b={encrypted_email}"
            assert " " not in url
            assert "?" not in encrypted_email
            assert "?" not in encrypted_space_id
    
    def test_generate_fernet_key(self):
        """Test Fernet key generation."""
        from src.coworkly_partner_api.utils.encoding import generate_fernet_key
        key = generate_fernet_key()
        assert isinstance(key, str)
        assert len(key) > 0 