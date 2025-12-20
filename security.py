"""Security module - API key obfuscation"""
import base64

def _get_key():
    """Obfuscated API key - harder to extract from compiled EXE"""
    # Split and encode the API key in parts
    parts = [
        'c2tfa3RoS00yMnFqUjlkZUdZU1',
        'ZERYZEFReEV3eVNHN080bA=='
    ]
    
    # Decode and combine
    decoded = ''.join([base64.b64decode(p).decode() for p in parts])
    return decoded

# XOR cipher for additional obfuscation
def _xor_cipher(data: str, key: int = 42) -> str:
    """Simple XOR cipher"""
    return ''.join(chr(ord(c) ^ key) for c in data)

# Store encrypted version
_encrypted_key = _xor_cipher("sk_kthKM22qjR9deGYSVDXdAQxEwySG7O4l", 42)

def get_api_key() -> str:
    """Get the API key - decrypted at runtime"""
    return _xor_cipher(_encrypted_key, 42)
