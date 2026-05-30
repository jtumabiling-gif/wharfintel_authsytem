# app/auth.py
import os
import re
import bcrypt
from dotenv import load_dotenv

load_dotenv()

# The Pepper stays hidden on the server, never sent to the browser
SECRET_PEPPER = os.getenv("WHARF_PEPPER", "CyberSec@WharfIntel2026!Pepper")

# --- PASSWORD STRENGTH VALIDATION ---
def validate_password_strength(password: str) -> dict:
    """
    Validates password against security requirements:
    - At least 1 lowercase letter
    - At least 1 uppercase letter
    - At least 1 digit
    - At least 1 special character
    - Minimum 12 characters
    
    Returns: dict with 'valid' (bool) and 'strength' ('Weak', 'Medium', 'Strong')
    """
    requirements = {
        'lowercase': bool(re.search(r'[a-z]', password)),
        'uppercase': bool(re.search(r'[A-Z]', password)),
        'digit': bool(re.search(r'[0-9]', password)),
        'symbol': bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password)),
        'min_length': len(password) >= 12
    }
    
    # Count how many requirements are met
    met_requirements = sum(requirements.values())
    
    # Determine strength level
    if met_requirements == 5:
        strength = 'Strong'
        valid = True
    elif met_requirements >= 3:
        strength = 'Medium'
        valid = False  # Don't allow Medium strength passwords during registration
    else:
        strength = 'Weak'
        valid = False
    
    return {
        'valid': valid,
        'strength': strength,
        'requirements': requirements,
        'met_count': met_requirements
    }

def get_password_hash(password: str) -> dict:
    """
    Securely hashes password with salt and pepper.
    
    Process:
    1. Validate password strength
    2. Generate random salt
    3. Combine: password + salt + pepper
    4. Apply bcrypt hashing algorithm
    5. Return: hash and salt (pepper stays secret)
    
    Returns: dict with 'hash' and 'salt'
    """
    # Validate password strength first
    validation = validate_password_strength(password)
    if not validation['valid']:
        raise ValueError(f"Password does not meet requirements. Strength: {validation['strength']}")
    
    # Generate random salt (bcrypt handles this internally)
    salt = bcrypt.gensalt(rounds=12)
    
    # Combine password + pepper, then convert to bytes
    pwd_bytes = (password + SECRET_PEPPER).encode('utf-8')
    
    # Hash with bcrypt
    hashed_bytes = bcrypt.hashpw(pwd_bytes, salt)
    
    return {
        'hash': hashed_bytes.decode('utf-8'),
        'salt': salt.decode('utf-8')
    }

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password against a stored hash.
    
    Process:
    1. Combine login attempt with pepper
    2. Use bcrypt to safely compare with stored hash
    
    Returns: True if password matches, False otherwise
    """
    # Combine the login attempt with the pepper
    pwd_bytes = (plain_password + SECRET_PEPPER).encode('utf-8')
    
    # Convert the stored database hash back to bytes
    hash_bytes = hashed_password.encode('utf-8')
    
    # Let bcrypt safely compare them
    return bcrypt.checkpw(pwd_bytes, hash_bytes)