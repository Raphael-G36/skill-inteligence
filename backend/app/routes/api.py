"""
API routes for Skill Intelligence application.

This module handles all REST API endpoints and ensures:
- Input validation and sanitization
- Error handling and logging
- No personal data storage or exposure
- Anonymized responses
- Proper CORS headers for cross-origin requests
"""
import logging
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from app.utils.response import error_response
from app.services.analysis_service import AnalysisService
from app.services.skill_extraction_service import SkillExtractionService
from app.services.github_ingestion_service import GitHubIngestionService
from app.services.job_posting_service import JobPostingIngestionService
from app.services.trend_engine_service import TrendEngineService
from app.routes.helpers import _sanitize_string_input, _validate_positive_integer

# Initialize logger for this module
logger = logging.getLogger(__name__)

# Initialize services (singleton pattern for better performance and resource management)
skill_extraction_service = SkillExtractionService()
github_ingestion_service = GitHubIngestionService(skill_extraction_service)
job_posting_service = JobPostingIngestionService(skill_extraction_service)
trend_engine_service = TrendEngineService()

api_bp = Blueprint('api', __name__)


@api_bp.route('/', methods=['GET', 'OPTIONS'])
@cross_origin()  # Explicitly allow CORS for this endpoint
def api_root():
    """
    API root endpoint.
    
    Returns:
        {
            "message": "Skill Intelligence API",
            "version": "1.0.0",
            "status": "active"
        }
    """
    return jsonify({
        'message': 'Skill Intelligence API',
        'version': '1.0.0',
        'status': 'active'
    }), 200


@api_bp.route('/analyze', methods=['POST', 'OPTIONS'])
@cross_origin()  # Explicitly allow CORS for this endpoint
def analyze():
    """
    Analyze skills based on role, industry, and region.
    
    Request body:
        {
            "role": "string",
            "industry": "string",
            "region": "string"
        }
    
    Returns:
        {
            "top_skills": ["skill1", "skill2", ...],
            "trending_skills": ["skill1", "skill2", ...],
            "recommended_skills": ["skill1", "skill2", ...]
        }
    
    Note: Input parameters are sanitized and not stored. No personal data is collected.
    """
    try:
        # Get and validate request data
        request_data = request.get_json()
        
        if not request_data:
            return error_response('Request body is required', 'ValidationError', 400)
        
        # Sanitize and validate required fields (strip whitespace, limit length)
        role = _sanitize_string_input(request_data.get('role'), max_length=100)
        industry = _sanitize_string_input(request_data.get('industry'), max_length=100)
        region = _sanitize_string_input(request_data.get('region'), max_length=100)
        
        if not role:
            return error_response('role is required', 'ValidationError', 400)
        if not industry:
            return error_response('industry is required', 'ValidationError', 400)
        if not region:
            return error_response('region is required', 'ValidationError', 400)
        
        # Validate field types (defense against type confusion attacks)
        if not isinstance(request_data.get('role'), str) or \
           not isinstance(request_data.get('industry'), str) or \
           not isinstance(request_data.get('region'), str):
            return error_response('role, industry, and region must be strings', 'ValidationError', 400)
        
        # Call service layer (business logic separated from route handling)
        analysis_result = AnalysisService.analyze_skills(role, industry, region)
        
        # Log request (anonymized - no personal data)
        logger.info(f'Skill analysis requested for role category and industry category')
        
        # Return anonymized response (no user identifiers, only aggregated data)
        return jsonify(analysis_result), 200
    
    except ValueError as e:
        # Handle validation errors specifically
        logger.warning(f'Validation error in analyze endpoint: {str(e)}')
        return error_response('Invalid input data provided', 'ValidationError', 400)
    except Exception as e:
        # Log error but don't expose internal details to client
        logger.error(f'Unexpected error in analyze endpoint: {str(e)}', exc_info=True)
        return error_response(
            'An error occurred while processing your request',
            'InternalError',
            500
        )


@api_bp.route('/extract-skills', methods=['POST', 'OPTIONS'])
@cross_origin()  # Explicitly allow CORS for this endpoint
def extract_skills():
    """
    Extract skills from raw text input.
    
    Request body:
        {
            "text": "string (job description, resume, etc.)"
        }
    
    Returns:
        {
            "skills": [
                {"skill": "Python", "category": "Programming Language"},
                ...
            ],
            "count": 5
        }
    
    Note: 
        - Input text is processed but NOT stored
        - No personal information is extracted or logged
        - Maximum text length: 10,000 characters (prevents abuse)
    """
    MAX_TEXT_LENGTH = 10000  # Prevent abuse with very large inputs
    
    try:
        request_data = request.get_json()
        
        if not request_data:
            return error_response('Request body is required', 'ValidationError', 400)
        
        # Validate and sanitize input text
        input_text = request_data.get('text')
        
        if input_text is None:
            return error_response('text field is required', 'ValidationError', 400)
        
        if not isinstance(input_text, str):
            return error_response('text must be a string', 'ValidationError', 400)
        
        # Sanitize: strip whitespace and limit length
        sanitized_text = input_text.strip()
        
        # Check length limit to prevent resource exhaustion
        if len(sanitized_text) > MAX_TEXT_LENGTH:
            return error_response(
                f'Text exceeds maximum length of {MAX_TEXT_LENGTH} characters',
                'ValidationError',
                400
            )
        
        # Handle empty input gracefully
        if not sanitized_text:
            return jsonify({
                'skills': [],
                'count': 0
            }), 200
        
        # Extract skills using service (text is processed but not stored)
        extracted_skills = skill_extraction_service.extract_skills(sanitized_text)
        
        # Log anonymized metrics (no text content, only counts)
        logger.info(f'Skills extracted: {len(extracted_skills)} skills found')
        
        # Return anonymized results (only skill names and categories, no input text)
        return jsonify({
            'skills': extracted_skills,
            'count': len(extracted_skills)
        }), 200
    
    except ValueError as e:
        logger.warning(f'Validation error in extract-skills endpoint: {str(e)}')
        return error_response('Invalid input data provided', 'ValidationError', 400)
    except Exception as e:
        logger.error(f'Unexpected error in extract-skills endpoint: {str(e)}', exc_info=True)
        return error_response(
            'An error occurred while extracting skills',
            'InternalError',
            500
        )


@api_bp.route('/github/ingest', methods=['POST', 'OPTIONS'])
@cross_origin()  # Explicitly allow CORS for this endpoint
def ingest_github_data():
    """
    Ingest data from GitHub repositories and extract aggregated skills.
    
    Request body:
        {
            "role": "string",
            "industry": "string",
            "max_repos": 10 (optional, 1-100)
        }
    
    Returns:
        {
            "search_criteria": {
                "role_category": "sanitized_role",
                "industry_category": "sanitized_industry"
            },
            "repositories_analyzed": 10,
            "skills": [{"skill": "Python", "count": 5}, ...],
            "total_skill_occurrences": 25,
            "unique_skills": 8
        }
    
    Note: 
        - Search criteria are sanitized and only used for matching
        - No repository URLs, user names, or personal data are stored or returned
        - Only aggregated skill counts are returned (fully anonymized)
    """
    try:
        request_data = request.get_json()
        
        if not request_data:
            return error_response('Request body is required', 'ValidationError', 400)
        
        # Sanitize and validate required fields
        role_query = _sanitize_string_input(request_data.get('role'), max_length=100)
        industry_query = _sanitize_string_input(request_data.get('industry'), max_length=100)
        
        if not role_query:
            return error_response('role is required', 'ValidationError', 400)
        if not industry_query:
            return error_response('industry is required', 'ValidationError', 400)
        
        # Validate field types
        if not isinstance(request_data.get('role'), str) or \
           not isinstance(request_data.get('industry'), str):
            return error_response('role and industry must be strings', 'ValidationError', 400)
        
        # Validate and sanitize max_repos parameter (prevent resource exhaustion)
        max_repositories = _validate_positive_integer(
            request_data.get('max_repos', 10),
            default=10,
            min_value=1,
            max_value=100
        )
        
        # Extract and aggregate skills from GitHub repositories
        # Note: This service uses mock data or public GitHub API (no auth required)
        # No personal data is collected or stored
        aggregated_skill_counts = github_ingestion_service.extract_skills_from_repos(
            role=role_query,
            industry=industry_query,
            max_repos=max_repositories
        )
        
        # Format response - only return aggregated, anonymized data
        anonymized_skills_list = [
            {
                'skill': skill_name,
                'count': occurrence_count
            }
            for skill_name, occurrence_count in aggregated_skill_counts.items()
        ]
        
        # Log anonymized metrics only (no user identifiers, no search terms logged)
        logger.info(
            f'GitHub ingestion completed: {max_repositories} repositories analyzed, '
            f'{len(aggregated_skill_counts)} unique skills extracted'
        )
        
        # Return anonymized response
        # Note: role_category and industry_category are just search query strings,
        # not personal identifiers. They represent general categories, not individual users.
        return jsonify({
            'search_criteria': {
                'role_category': role_query,
                'industry_category': industry_query
            },
            'repositories_analyzed': max_repositories,
            'skills': anonymized_skills_list,
            'total_skill_occurrences': sum(aggregated_skill_counts.values()),
            'unique_skills': len(aggregated_skill_counts)
        }), 200
    
    except ValueError as validation_error:
        logger.warning(f'Validation error in github/ingest endpoint: {str(validation_error)}')
        return error_response('Invalid input data provided', 'ValidationError', 400)
    except Exception as unexpected_error:
        logger.error(
            f'Unexpected error in github/ingest endpoint: {str(unexpected_error)}', 
            exc_info=True
        )
        return error_response(
            'An error occurred while processing GitHub data',
            'InternalError',
            500
        )


@api_bp.route('/job-postings/ingest', methods=['POST', 'OPTIONS'])
@cross_origin()  # Explicitly allow CORS for this endpoint
def ingest_job_postings():
    """
    Ingest job postings and extract aggregated skill frequency counts.
    
    Request body:
        {
            "use_mock": true (optional),
            "job_description": "string" (optional, if use_mock=false),
            "job_descriptions": ["string", ...] (optional, if use_mock=false),
            "role": "string" (optional, for mock data),
            "industry": "string" (optional, for mock data),
            "count": 5 (optional, 1-20, for mock data)
        }
    
    Returns:
        {
            "skills": [
                {"skill": "Python", "count": 5, "frequency": 0.83},
                ...
            ],
            "total_skill_occurrences": 25,
            "unique_skills": 8,
            "job_postings_analyzed": 6
        }
    
    Privacy Note:
        - Job description text is processed but NOT stored
        - Only aggregated skill counts are returned
        - No personal information, company names, or identifying details are extracted or stored
        - Input text is discarded after processing
    """
    MAX_JOB_DESCRIPTIONS = 100  # Prevent abuse
    MAX_TEXT_LENGTH = 50000  # Per description limit
    
    try:
        request_data = request.get_json()
        
        if not request_data:
            return error_response('Request body is required', 'ValidationError', 400)
        
        job_descriptions_to_process = []
        
        # Check if using mock data or real job descriptions
        use_mock_data = request_data.get('use_mock', False)
        
        if use_mock_data:
            # Use mock job descriptions (no user data)
            role_category = _sanitize_string_input(request_data.get('role'), max_length=100)
            industry_category = _sanitize_string_input(request_data.get('industry'), max_length=100)
            
            description_count = _validate_positive_integer(
                request_data.get('count', 5),
                default=5,
                min_value=1,
                max_value=20
            )
            
            job_descriptions_to_process = job_posting_service.get_mock_job_descriptions(
                role=role_category,
                industry=industry_category,
                count=description_count
            )
        else:
            # Process provided job descriptions
            single_description = request_data.get('job_description')
            multiple_descriptions = request_data.get('job_descriptions')
            
            if multiple_descriptions:
                # Multiple job descriptions provided
                if not isinstance(multiple_descriptions, list):
                    return error_response('job_descriptions must be an array', 'ValidationError', 400)
                
                # Limit number of descriptions to prevent abuse
                if len(multiple_descriptions) > MAX_JOB_DESCRIPTIONS:
                    return error_response(
                        f'Maximum {MAX_JOB_DESCRIPTIONS} job descriptions allowed',
                        'ValidationError',
                        400
                    )
                
                # Sanitize each description
                for idx, desc in enumerate(multiple_descriptions):
                    if not isinstance(desc, str):
                        return error_response(
                            f'job_descriptions[{idx}] must be a string',
                            'ValidationError',
                            400
                        )
                    
                    sanitized = desc.strip()[:MAX_TEXT_LENGTH]  # Truncate if too long
                    if sanitized:
                        job_descriptions_to_process.append(sanitized)
                        
            elif single_description:
                # Single job description provided
                if not isinstance(single_description, str):
                    return error_response('job_description must be a string', 'ValidationError', 400)
                
                sanitized = single_description.strip()[:MAX_TEXT_LENGTH]
                if sanitized:
                    job_descriptions_to_process = [sanitized]
                else:
                    return error_response('job_description cannot be empty', 'ValidationError', 400)
            else:
                return error_response(
                    'Either job_description, job_descriptions, or use_mock=true is required',
                    'ValidationError',
                    400
                )
        
        # Handle empty input gracefully
        if not job_descriptions_to_process:
            return jsonify({
                'skills': [],
                'total_skill_occurrences': 0,
                'unique_skills': 0,
                'job_postings_analyzed': 0
            }), 200
        
        # Extract and aggregate skills (input text is processed but not stored)
        aggregated_skill_counts = job_posting_service.aggregate_skill_counts(job_descriptions_to_process)
        
        # Format response with anonymized aggregated data only
        anonymized_skills_list = [
            {
                'skill': skill_name,
                'count': occurrence_count,
                'frequency': round(occurrence_count / len(job_descriptions_to_process), 2)
            }
            for skill_name, occurrence_count in aggregated_skill_counts.items()
        ]
        
        # Log anonymized metrics (no content, only counts)
        logger.info(
            f'Job posting ingestion completed: {len(job_descriptions_to_process)} descriptions, '
            f'{len(aggregated_skill_counts)} unique skills extracted'
        )
        
        # Return only aggregated, anonymized data (no job description content)
        return jsonify({
            'skills': anonymized_skills_list,
            'total_skill_occurrences': sum(aggregated_skill_counts.values()),
            'unique_skills': len(aggregated_skill_counts),
            'job_postings_analyzed': len(job_descriptions_to_process)
        }), 200
    
    except ValueError as validation_error:
        logger.warning(f'Validation error in job-postings/ingest endpoint: {str(validation_error)}')
        return error_response('Invalid input data provided', 'ValidationError', 400)
    except Exception as unexpected_error:
        logger.error(
            f'Unexpected error in job-postings/ingest endpoint: {str(unexpected_error)}',
            exc_info=True
        )
        return error_response(
            'An error occurred while processing job postings',
            'InternalError',
            500
        )


@api_bp.route('/trends/store', methods=['POST', 'OPTIONS'])
@cross_origin()  # Explicitly allow CORS for this endpoint
def store_trend_data():
    """
    Store aggregated skill frequency data for historical trend analysis.
    
    Request body:
        {
            "skill_counts": {"Python": 45, "JavaScript": 38, ...},
            "period": "2024-01-15" (optional, defaults to current date)
        }
    
    Returns:
        {
            "message": "Skill frequency data stored successfully",
            "period": "2024-01-15",
            "skills_count": 5,
            "total_occurrences": 168
        }
    
    Privacy Note:
        - Only aggregated skill counts are stored (no individual records)
        - No personal data or user identifiers are stored
        - Period identifiers are date-based only, not linked to users
    """
    try:
        request_data = request.get_json()
        
        if not request_data:
            return error_response('Request body is required', 'ValidationError', 400)
        
        skill_counts_raw = request_data.get('skill_counts')
        period_identifier = request_data.get('period')  # Optional: defaults to current date
        
        if not skill_counts_raw:
            return error_response('skill_counts is required', 'ValidationError', 400)
        
        if not isinstance(skill_counts_raw, dict):
            return error_response('skill_counts must be a dictionary', 'ValidationError', 400)
        
        # Validate and sanitize skill counts
        # Ensure all values are non-negative numbers
        validated_skill_counts = {}
        for skill_name, count_value in skill_counts_raw.items():
            # Validate count is a number and non-negative
            if not isinstance(count_value, (int, float)):
                return error_response(
                    f'Invalid count for skill "{skill_name}": must be a number',
                    'ValidationError',
                    400
                )
            
            if count_value < 0:
                return error_response(
                    f'Invalid count for skill "{skill_name}": must be non-negative',
                    'ValidationError',
                    400
                )
            
            # Convert to integer and sanitize skill name
            sanitized_skill_name = str(skill_name).strip()[:100]  # Limit length
            validated_skill_counts[sanitized_skill_name] = int(count_value)
        
        if not validated_skill_counts:
            return error_response('skill_counts cannot be empty', 'ValidationError', 400)
        
        # Save aggregated data (no personal identifiers)
        saved_period_identifier = trend_engine_service.save_skill_frequencies(
            validated_skill_counts, 
            period_identifier
        )
        
        # Log anonymized metrics
        logger.info(
            f'Trend data stored for period {saved_period_identifier}: '
            f'{len(validated_skill_counts)} skills, '
            f'{sum(validated_skill_counts.values())} total occurrences'
        )
        
        return jsonify({
            'message': 'Skill frequency data stored successfully',
            'period': saved_period_identifier,
            'skills_count': len(validated_skill_counts),
            'total_occurrences': sum(validated_skill_counts.values())
        }), 201
    
    except ValueError as validation_error:
        logger.warning(f'Validation error in trends/store endpoint: {str(validation_error)}')
        return error_response('Invalid input data provided', 'ValidationError', 400)
    except Exception as unexpected_error:
        logger.error(
            f'Unexpected error in trends/store endpoint: {str(unexpected_error)}',
            exc_info=True
        )
        return error_response(
            'An error occurred while storing trend data',
            'InternalError',
            500
        )


@api_bp.route('/trends/analyze', methods=['POST', 'OPTIONS'])
@cross_origin()  # Explicitly allow CORS for this endpoint
def analyze_trends():
    """
    Analyze skill trends by comparing current aggregated data with historical data.
    
    Request body:
        {
            "skill_counts": {"Python": 55, "JavaScript": 35, ...},
            "comparison_period": "2024-01-08" (optional, specific period to compare),
            "periods_back": 1 (optional, default: compare with most recent period)
        }
    
    Returns:
        {
            "skills": [
                {
                    "skill": "Python",
                    "current_count": 55,
                    "previous_count": 45,
                    "absolute_change": 10,
                    "percentage_change": 22.22,
                    "trend": "rising"
                },
                ...
            ],
            "summary": {
                "rising_count": 3,
                "stable_count": 1,
                "declining_count": 1,
                "rising": [...],
                "stable": [...],
                "declining": [...]
            },
            "total_skills_analyzed": 5
        }
    
    Privacy Note:
        - Only aggregated skill counts are used (no individual records)
        - Historical data contains only skill frequencies, no personal data
        - Trend analysis results are fully anonymized
    """
    try:
        request_data = request.get_json()
        
        if not request_data:
            return error_response('Request body is required', 'ValidationError', 400)
        
        current_skill_counts_raw = request_data.get('skill_counts')
        comparison_period_identifier = request_data.get('comparison_period')  # Optional
        lookback_periods = request_data.get('periods_back', 1)  # Default: 1 period back
        
        if not current_skill_counts_raw:
            return error_response('skill_counts is required', 'ValidationError', 400)
        
        if not isinstance(current_skill_counts_raw, dict):
            return error_response('skill_counts must be a dictionary', 'ValidationError', 400)
        
        # Validate and sanitize skill counts
        validated_current_counts = {}
        for skill_name, count_value in current_skill_counts_raw.items():
            if not isinstance(count_value, (int, float)) or count_value < 0:
                return error_response(
                    f'Invalid count for skill "{skill_name}": must be a non-negative number',
                    'ValidationError',
                    400
                )
            sanitized_skill_name = str(skill_name).strip()[:100]
            validated_current_counts[sanitized_skill_name] = int(count_value)
        
        if not validated_current_counts:
            return error_response('skill_counts cannot be empty', 'ValidationError', 400)
        
        # Validate periods_back parameter (prevent abuse)
        validated_lookback = _validate_positive_integer(
            lookback_periods,
            default=1,
            min_value=1,
            max_value=100  # Reasonable limit
        )
        
        # Analyze trends using historical aggregated data
        trend_analysis_results = trend_engine_service.analyze_trends(
            current_skill_counts=validated_current_counts,
            comparison_period=comparison_period_identifier,
            periods_back=validated_lookback
        )
        
        # Get trend summary grouped by classification
        trend_summary = trend_engine_service.get_trend_summary(trend_analysis_results)
        
        # Convert to list format and sort by absolute change magnitude
        sorted_trends_list = sorted(
            trend_analysis_results.values(),
            key=lambda trend_item: abs(trend_item['absolute_change']),
            reverse=True
        )
        
        # Log anonymized metrics
        logger.info(
            f'Trend analysis completed: {len(trend_analysis_results)} skills analyzed, '
            f'{len(trend_summary["rising"])} rising, {len(trend_summary["declining"])} declining'
        )
        
        return jsonify({
            'skills': sorted_trends_list,
            'summary': {
                'rising_count': len(trend_summary['rising']),
                'stable_count': len(trend_summary['stable']),
                'declining_count': len(trend_summary['declining']),
                'rising': trend_summary['rising'],
                'stable': trend_summary['stable'],
                'declining': trend_summary['declining']
            },
            'total_skills_analyzed': len(trend_analysis_results)
        }), 200
    
    except ValueError as validation_error:
        logger.warning(f'Validation error in trends/analyze endpoint: {str(validation_error)}')
        return error_response('Invalid input data provided', 'ValidationError', 400)
    except Exception as unexpected_error:
        logger.error(
            f'Unexpected error in trends/analyze endpoint: {str(unexpected_error)}',
            exc_info=True
        )
        return error_response(
            'An error occurred during trend analysis',
            'InternalError',
            500
        )


@api_bp.route('/trends/periods', methods=['GET', 'OPTIONS'])
@cross_origin()  # Explicitly allow CORS for this endpoint
def get_historical_periods():
    """
    Get list of available historical periods for trend comparison.
    
    Returns:
        {
            "periods": ["2024-01-15", "2024-01-08", ...],
            "count": 3
        }
    
    Privacy Note:
        - Only period identifiers (dates) are returned
        - No data content or personal information is exposed
        - Periods represent aggregated data snapshots, not individual records
    """
    try:
        available_periods = trend_engine_service.get_historical_periods()
        
        logger.info(f'Historical periods requested: {len(available_periods)} periods available')
        
        return jsonify({
            'periods': available_periods,
            'count': len(available_periods)
        }), 200
    
    except Exception as unexpected_error:
        logger.error(
            f'Unexpected error in trends/periods endpoint: {str(unexpected_error)}',
            exc_info=True
        )
        return error_response(
            'An error occurred while fetching historical periods',
            'InternalError',
            500
        )

