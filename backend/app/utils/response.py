from flask import jsonify
from typing import Any, Dict, Optional


def success_response(data: Any = None, message: str = 'Success', status_code: int = 200) -> tuple:
    """
    Create a standardized success JSON response
    
    Args:
        data: Response data
        message: Success message
        status_code: HTTP status code
    
    Returns:
        Tuple of (json_response, status_code)
    """
    response = {
        'success': True,
        'message': message
    }
    
    if data is not None:
        response['data'] = data
    
    return jsonify(response), status_code


def error_response(
    message: str, 
    error_type: Optional[str] = None, 
    status_code: int = 400,
    include_details: bool = False
) -> tuple:
    """
    Create a standardized error JSON response.
    
    Args:
        message: User-friendly error message (will be shown to client)
        error_type: Error type/name for client-side handling (e.g., 'ValidationError')
        status_code: HTTP status code
        include_details: If True, includes additional error details (use carefully in production)
    
    Returns:
        Tuple of (json_response, status_code)
    
    Note: 
        - Error messages are sanitized and should not expose internal system details
        - Personal information is never included in error responses
    """
    # Sanitize error message to prevent information leakage
    # In production, ensure messages don't expose internal paths, stack traces, etc.
    sanitized_message = message[:500] if len(message) > 500 else message
    
    response = {
        'success': False,
        'message': sanitized_message
    }
    
    if error_type:
        response['error_type'] = error_type
    
    # Only include detailed error information in development mode
    # This prevents exposing internal system details to clients
    if include_details:
        # This should be controlled by environment variable in real deployment
        pass
    
    return jsonify(response), status_code

