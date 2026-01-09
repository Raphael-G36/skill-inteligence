from flask import Blueprint, jsonify
from flask_cors import cross_origin

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET', 'OPTIONS'])
@cross_origin()  # Allow CORS for health checks (needed for frontend monitoring)
def health_check():
    """
    Health check endpoint.
    
    Returns:
        {
            "status": "ok",
            "message": "Skill Intelligence API is running",
            "service": "Skill Intelligence API"
        }
    """
    return jsonify({
        'status': 'ok',
        'message': 'Skill Intelligence API is running',
        'service': 'Skill Intelligence API'
    }), 200

