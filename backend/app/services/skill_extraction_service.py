"""
Skill extraction service for parsing and normalizing skill mentions from text.

This service:
- Extracts skill keywords from unstructured text
- Normalizes variations (e.g., "postgres" -> "PostgreSQL")
- Returns structured skill data with categories

Privacy: Input text is processed in-memory only, never stored.
"""
import json
import re
import logging
from typing import List, Dict
from pathlib import Path

logger = logging.getLogger(__name__)


class SkillExtractionService:
    """
    Service for extracting and normalizing skills from raw text input.
    
    Uses a predefined keyword list to identify and normalize skill mentions.
    All text processing is done in-memory - no input data is stored.
    """
    
    def __init__(self):
        """Initialize the service by loading skill definitions and building lookup maps."""
        try:
            self.skills_data = self._load_skills_data()
            self.skill_map = self._build_skill_map()
            logger.info(f'SkillExtractionService initialized with {len(self.skills_data)} skills')
        except Exception as e:
            logger.error(f'Failed to initialize SkillExtractionService: {str(e)}', exc_info=True)
            raise
    
    def _load_skills_data(self) -> Dict:
        """
        Load skills data from JSON configuration file.
        
        Returns:
            Dictionary mapping normalized skill names to skill metadata
        
        Raises:
            FileNotFoundError: If skills data file is missing
            ValueError: If JSON file is malformed
        """
        # Construct path to skills data file relative to this module
        current_dir = Path(__file__).parent
        skills_data_file = current_dir.parent / 'data' / 'skills.json'
        
        try:
            with open(skills_data_file, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
                skills_dict = json_data.get('skills', {})
                
                if not skills_dict:
                    logger.warning('Skills data file is empty or missing skills key')
                
                return skills_dict
                
        except FileNotFoundError:
            error_msg = f"Skills data file not found at {skills_data_file}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)
        except json.JSONDecodeError as json_error:
            error_msg = f"Invalid JSON in skills data file: {json_error}"
            logger.error(error_msg)
            raise ValueError(error_msg)
    
    def _build_skill_map(self) -> Dict[str, str]:
        """
        Build a lookup map from skill variations to normalized skill names.
        
        This map enables fast skill matching regardless of how the skill is mentioned
        (e.g., "postgres", "PostgreSQL", "pg" all map to "PostgreSQL").
        
        Algorithm:
        1. For each normalized skill name, add it to the map
        2. Add all variations (aliases) for that skill
        3. All keys are lowercased for case-insensitive matching
        
        Returns:
            Dictionary mapping lowercase variations to normalized skill names
            Example: {"python": "Python", "py": "Python", "postgres": "PostgreSQL", ...}
        """
        variation_to_normalized_map = {}
        
        for normalized_skill_name, skill_metadata in self.skills_data.items():
            # Get list of all variations/aliases for this skill
            skill_variations = skill_metadata.get('variations', [])
            
            # Add the normalized name itself (for exact matches)
            variation_to_normalized_map[normalized_skill_name.lower()] = normalized_skill_name
            
            # Add all variations (aliases) that map to this normalized name
            for variation in skill_variations:
                variation_lowercase = variation.lower()
                # Note: If duplicate variations exist, last one wins (shouldn't happen with clean data)
                variation_to_normalized_map[variation_lowercase] = normalized_skill_name
        
        logger.debug(f'Built skill map with {len(variation_to_normalized_map)} variations')
        return variation_to_normalized_map
    
    def extract_skills(self, input_text: str) -> List[Dict[str, str]]:
        """
        Extract and normalize skills from raw text input.
        
        This method:
        1. Normalizes input text (lowercase, whitespace cleanup)
        2. Searches for skill keywords using word boundary matching
        3. Normalizes found skills to standard names
        4. Returns structured results with categories
        
        Args:
            input_text: Raw text to search for skills (e.g., job description, resume)
                       This text is processed but NOT stored
        
        Returns:
            List of dictionaries, each containing:
                - 'skill': Normalized skill name (e.g., "PostgreSQL")
                - 'category': Skill category (e.g., "Database")
            
            Results are sorted alphabetically by skill name for consistency.
        
        Privacy Note:
            Input text is processed in-memory only and discarded after extraction.
            No text content is logged, stored, or returned to the caller.
        """
        # Validate input
        if not input_text or not isinstance(input_text, str):
            return []
        
        # Normalize input text for matching
        # - Convert to lowercase for case-insensitive matching
        # - Collapse multiple whitespace characters to single spaces
        # - Remove leading/trailing whitespace
        normalized_input_text = re.sub(r'\s+', ' ', input_text.lower().strip())
        
        # Track which normalized skills we've already found (prevents duplicates)
        discovered_skills_set = set()
        extracted_skills_list = []
        
        # Sort skills by variation length (longest first)
        # This ensures "Node.js" matches before "Node" to avoid false positives
        sorted_skill_variations = sorted(
            self.skill_map.items(), 
            key=lambda item: len(item[0]), 
            reverse=True
        )
        
        # Search for each skill variation in the text
        for skill_variation, normalized_skill_name in sorted_skill_variations:
            # Skip if we've already found this normalized skill
            if normalized_skill_name in discovered_skills_set:
                continue
            
            # Use word boundaries to match whole words only
            # This prevents matching "JavaScript" inside "TypeScript"
            # Pattern: \b ensures we match word boundaries, not substring matches
            word_boundary_pattern = r'\b' + re.escape(skill_variation) + r'\b'
            
            # Search for this variation in the normalized text
            if re.search(word_boundary_pattern, normalized_input_text, re.IGNORECASE):
                # Found a match - add to results
                discovered_skills_set.add(normalized_skill_name)
                
                # Get skill category from metadata
                skill_category = self.skills_data[normalized_skill_name].get('category', 'Unknown')
                
                extracted_skills_list.append({
                    'skill': normalized_skill_name,
                    'category': skill_category
                })
        
        # Sort results alphabetically by skill name for consistent output
        extracted_skills_list.sort(key=lambda skill_dict: skill_dict['skill'])
        
        return extracted_skills_list
    
    def normalize_skill(self, skill: str) -> str:
        """
        Normalize a single skill name to its standard form
        
        Args:
            skill: Skill name or variation to normalize
        
        Returns:
            Normalized skill name, or original if not found
        """
        if not skill or not isinstance(skill, str):
            return skill
        
        normalized = self.skill_map.get(skill.lower().strip())
        return normalized if normalized else skill
    
    def get_all_skills(self) -> List[str]:
        """
        Get list of all normalized skill names
        
        Returns:
            List of all normalized skill names
        """
        return sorted(list(self.skills_data.keys()))

