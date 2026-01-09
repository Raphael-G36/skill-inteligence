"""
Helper functions for API route validation and sanitization.

These utilities ensure:
- Input sanitization to prevent injection attacks
- Data validation
- No personal data leakage
"""
import re
from typing import Optional


def _sanitize_string_input(input_value: Optional[str], max_length: int = 255) -> Optional[str]:
    """
    Sanitize string input by trimming whitespace and limiting length.
    
    Args:
        input_value: The input string to sanitize
        max_length: Maximum allowed length (default: 255)
    
    Returns:
        Sanitized string or None if input is invalid
    
    Note: This function does NOT store or log the input value.
    """
    if input_value is None:
        return None
    
    if not isinstance(input_value, str):
        return None
    
    # Remove leading/trailing whitespace
    sanitized = input_value.strip()
    
    # Remove any control characters that could be used for injection
    sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', sanitized)
    
    # Limit length to prevent abuse
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized if sanitized else None


def _validate_positive_integer(value: any, default: int, min_value: int = 1, max_value: int = 100) -> int:
    """
    Validate and return a positive integer within bounds.
    
    Args:
        value: Value to validate
        default: Default value if validation fails
        min_value: Minimum allowed value
        max_value: Maximum allowed value
    
    Returns:
        Validated integer within bounds
    """
    try:
        if not isinstance(value, int):
            return default
        
        if value < min_value or value > max_value:
            return default
        
        return value
    except (TypeError, ValueError):
        return default

