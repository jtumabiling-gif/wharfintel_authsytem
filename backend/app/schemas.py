# app/schemas.py
from pydantic import BaseModel, Field, validator
import re

class UserRegister(BaseModel):
    """Schema for user registration with password validation"""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=12)
    
    @validator('username')
    def validate_username(cls, v):
        """Username must be alphanumeric with underscores/hyphens"""
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Username can only contain letters, numbers, underscores, and hyphens')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        """Password must meet security requirements"""
        # Lowercase letter
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        # Uppercase letter
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        # Digit
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one digit')
        # Special character
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', v):
            raise ValueError('Password must contain at least one special character')
        # Minimum 12 characters
        if len(v) < 12:
            raise ValueError('Password must be at least 12 characters long')
        return v


class UserLogin(BaseModel):
    """Schema for user login"""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)


class PasswordUpdate(BaseModel):
    """Schema for password update"""
    current_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=12)


class AccountDelete(BaseModel):
    """Schema for account deletion"""
    password: str = Field(..., min_length=8)


class PasswordStrengthResponse(BaseModel):
    """Response for password strength check"""
    strength: str  # "Weak", "Medium", "Strong"
    valid: bool
    requirements: dict
    met_count: int
    message: str


class UserResponse(BaseModel):
    """Response for user operations"""
    id: int
    username: str
    created_at: str
    
    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    """Response for login operations"""
    access_token: str
    token_type: str
    user: str
