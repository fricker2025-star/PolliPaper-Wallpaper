"""Security module - API key obfuscation

SETUP INSTRUCTIONS:
1. Replace YOUR_API_KEY_HERE below with your actual Pollinations API key
2. The key will be XOR encrypted for basic obfuscation in the compiled EXE
3. Get your API key from: https://pollinations.ai
"""

import base64

def _get_key():
    """Obfuscated API key - harder to extract from compiled EXE"""
    # Split and encode the API key in parts (example only)
    parts = [
        'WU9VUl9BUElfS0VZ',
        'X0hFUkU='
    ]
    
    # Decode and combine
    decoded = ''.join([base64.b64decode(p).decode() for p in parts])
    return decoded

# XOR cipher for additional obfuscation
def _xor_cipher(data: str, key: int = 42) -> str:
    """Simple XOR cipher"""
    return ''.join(chr(ord(c) ^ key) for c in data)

# Store encrypted version - REPLACE YOUR_API_KEY_HERE WITH YOUR ACTUAL KEY
_encrypted_key = _xor_cipher("YOUR_API_KEY_HERE", 42)

def get_api_key() -> str:
    """Get the API key - decrypted at runtime"""
    return _xor_cipher(_encrypted_key, 42)
