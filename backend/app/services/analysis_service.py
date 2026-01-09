"""
Analysis service for skill intelligence.

This service provides mock skill analysis based on role, industry, and region.
All data is anonymized - no personal information is used or stored.
"""
from typing import Dict, List


class AnalysisService:
    """
    Service layer for skill analysis logic.
    
    This service provides skill recommendations based on:
    - Job role category (e.g., "Backend Engineer", "Frontend Developer")
    - Industry sector (e.g., "FinTech", "E-commerce")
    - Geographic region (e.g., "Global", "North America")
    
    Note: All inputs are treated as categories/strings, not personal identifiers.
    No user data is stored or tracked.
    """
    
    @staticmethod
    def analyze_skills(role_category: str, industry_category: str, region_category: str) -> Dict[str, any]:
        """
        Analyze skills based on role, industry, and region categories.
        
        Args:
            role_category: Job role category string (e.g., "Backend Engineer")
                          Used for matching skill sets, not personal identification
            industry_category: Industry sector string (e.g., "FinTech")
                             Used for industry-specific skill filtering
            region_category: Geographic region string (e.g., "Global")
                           Used for region-specific trend analysis
        
        Returns:
            Dictionary containing:
                - top_skills: List of most in-demand skills
                - trending_skills: List of trending/emerging skills
                - recommended_skills: List of recommended skills for career growth
                - role_recognized: Boolean indicating if the role was matched to a known pattern
                - message: Optional message about data availability
        
        Note: 
            - This is mock data for MVP purposes
            - In production, this would query aggregated, anonymized data from a database
            - No personal data is used or returned
        """
        # Check if role is recognized (matches known patterns)
        role_recognized = AnalysisService._is_role_recognized(role_category)
        
        # Extract top skills based on role and industry matching
        top_skills = AnalysisService._get_top_skills(role_category, industry_category)
        
        # Get trending skills based on market trends (includes region-specific data)
        trending_skills = AnalysisService._get_trending_skills(
            role_category, 
            industry_category, 
            region_category
        )
        
        # Get recommended skills for career advancement
        recommended_skills = AnalysisService._get_recommended_skills(role_category, industry_category)
        
        # Build response with metadata
        response = {
            'top_skills': top_skills,
            'trending_skills': trending_skills,
            'recommended_skills': recommended_skills,
            'role_recognized': role_recognized
        }
        
        # Add helpful message if role wasn't recognized
        if not role_recognized:
            response['message'] = (
                f"The role '{role_category}' doesn't match our known patterns. "
                "Showing generic skills. Try roles like 'Backend Engineer', 'Frontend Developer', "
                "or 'Full Stack Developer' for more specific results."
            )
        
        return response
    
    @staticmethod
    def _is_role_recognized(role_category: str) -> bool:
        """
        Check if the role category matches known patterns.
        
        Args:
            role_category: Job role category string
        
        Returns:
            True if role matches known patterns, False otherwise
        """
        role_keywords = role_category.lower()
        
        # Known role patterns
        known_patterns = [
            'backend', 'engineer', 'frontend', 'ui', 'full', 'stack',
            'data scientist', 'data engineer', 'devops', 'qa', 'tester',
            'product manager', 'designer', 'architect'
        ]
        
        return any(pattern in role_keywords for pattern in known_patterns)
    
    @staticmethod
    def _get_top_skills(role_category: str, industry_category: str) -> List[str]:
        """
        Get top skills for the given role and industry categories.
        
        Uses keyword matching on role and industry strings to determine skill sets.
        This is a simplified mock implementation for MVP.
        
        Args:
            role_category: Job role category string (lowercased for matching)
            industry_category: Industry category string (lowercased for matching)
        
        Returns:
            List of top skill names (limited to 5 for MVP)
        """
        role_keywords = role_category.lower()
        industry_keywords = industry_category.lower()
        
        # Match role patterns to determine base skill set
        # Priority: specific matches first, then generic fallback
        if 'backend' in role_keywords or ('engineer' in role_keywords and 'frontend' not in role_keywords):
            base_skills = ['Python', 'JavaScript', 'Java', 'API Development', 'Database Design']
            
            # Add industry-specific skills if FinTech detected
            if 'fintech' in industry_keywords or 'finance' in industry_keywords:
                base_skills.extend(['Security Best Practices', 'Financial APIs', 'Compliance'])
            
            return base_skills[:5]
        elif 'frontend' in role_keywords or 'ui' in role_keywords:
            return ['React', 'TypeScript', 'CSS', 'JavaScript', 'Next.js']
        elif 'full' in role_keywords or 'stack' in role_keywords:
            return ['Node.js', 'React', 'Python', 'PostgreSQL', 'Docker']
        elif 'data' in role_keywords and ('scientist' in role_keywords or 'analyst' in role_keywords):
            return ['Python', 'SQL', 'Machine Learning', 'Data Visualization', 'Statistics']
        elif 'devops' in role_keywords or 'sre' in role_keywords:
            return ['Docker', 'Kubernetes', 'CI/CD', 'Cloud Platforms', 'Monitoring']
        elif 'qa' in role_keywords or 'tester' in role_keywords or 'test' in role_keywords:
            return ['Test Automation', 'Quality Assurance', 'Selenium', 'API Testing', 'Bug Tracking']
        else:
            # Generic/default skill set for unmatched roles
            return ['Python', 'SQL', 'Git', 'Problem Solving', 'Communication']
    
    @staticmethod
    def _get_trending_skills(role_category: str, industry_category: str, region_category: str) -> List[str]:
        """
        Get trending skills based on current market trends.
        
        Combines global, industry-specific, role-specific, and region-specific trends.
        This is mock data representing typical market trends.
        
        Args:
            role_category: Job role category for role-specific trends
            industry_category: Industry category for industry-specific trends
            region_category: Region category for region-specific trends
        
        Returns:
            List of trending skill names (limited to 5 for MVP)
        """
        trending_skills = []
        
        # Universal trending skills across all tech roles
        trending_skills.extend(['AI/ML Integration', 'Cloud Architecture', 'DevOps'])
        
        # Industry-specific trending skills
        industry_keywords = industry_category.lower()
        if 'fintech' in industry_keywords or 'finance' in industry_keywords:
            trending_skills.extend(['Blockchain Basics', 'RegTech'])
        
        # Role-specific trending skills
        role_keywords = role_category.lower()
        if 'backend' in role_keywords or 'engineer' in role_keywords:
            trending_skills.extend(['Microservices', 'Container Orchestration'])
        
        # Region-specific trends (mock implementation)
        region_keywords = region_category.lower()
        if 'global' in region_keywords:
            trending_skills.append('Remote Collaboration Tools')
        
        # Return top 5 trending skills
        return trending_skills[:5]
    
    @staticmethod
    def _get_recommended_skills(role_category: str, industry_category: str) -> List[str]:
        """
        Get recommended skills for career growth and advancement.
        
        Provides skills that complement the role and industry, focusing on:
        - Technical depth and breadth
        - Industry-specific knowledge
        - Career advancement skills
        
        Args:
            role_category: Job role category for role-specific recommendations
            industry_category: Industry category for industry-specific recommendations
        
        Returns:
            List of recommended skill names (limited to 5 for MVP)
        """
        recommended_skills = []
        role_keywords = role_category.lower()
        industry_keywords = industry_category.lower()
        
        # Backend/Engineering role recommendations
        if 'backend' in role_keywords or 'engineer' in role_keywords:
            # Core technical skills for advancement
            recommended_skills.extend([
                'System Design', 
                'Performance Optimization', 
                'Testing Frameworks'
            ])
            
            # Industry-specific additions for FinTech
            if 'fintech' in industry_keywords or 'finance' in industry_keywords:
                recommended_skills.extend(['Financial Regulations', 'Payment Systems'])
            
            # DevOps and operational skills
            recommended_skills.extend(['CI/CD', 'Monitoring & Observability'])
        else:
            # Generic recommendations for other roles
            recommended_skills.extend([
                'Agile Methodologies', 
                'Code Review Practices', 
                'Documentation'
            ])
        
        # Return top 5 recommended skills
        return recommended_skills[:5]

