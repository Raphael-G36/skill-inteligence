import json
import requests
from typing import Dict, List, Optional
from collections import Counter
from app.services.skill_extraction_service import SkillExtractionService


class GitHubIngestionService:
    """Service for ingesting and analyzing data from GitHub repositories"""
    
    GITHUB_API_BASE = "https://api.github.com"
    USE_MOCK_DATA = True  # Set to False when ready to use real API
    
    def __init__(self, skill_extraction_service: Optional[SkillExtractionService] = None):
        """
        Initialize GitHub ingestion service
        
        Args:
            skill_extraction_service: Optional skill extraction service instance
        """
        self.skill_extractor = skill_extraction_service or SkillExtractionService()
    
    def search_repositories(self, role: str, industry: str, max_results: int = 10) -> Dict:
        """
        Search GitHub repositories based on role and industry keywords
        
        Args:
            role: Job role (e.g., "Backend Engineer")
            industry: Industry sector (e.g., "FinTech")
            max_results: Maximum number of repositories to fetch
        
        Returns:
            Dictionary with search results or mock data
        """
        if self.USE_MOCK_DATA:
            return self._get_mock_repositories(role, industry, max_results)
        
        # Build search query from role and industry
        search_query = self._build_search_query(role, industry)
        
        try:
            # GitHub Search API endpoint
            url = f"{self.GITHUB_API_BASE}/search/repositories"
            params = {
                'q': search_query,
                'sort': 'stars',
                'order': 'desc',
                'per_page': min(max_results, 100)  # GitHub API max is 100
            }
            
            # Make request (no authentication required for public repos)
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 403:
                # Rate limit or API error - fall back to mock
                return self._get_mock_repositories(role, industry, max_results)
            else:
                response.raise_for_status()
                
        except requests.RequestException:
            # Fallback to mock data on any error
            return self._get_mock_repositories(role, industry, max_results)
    
    def _build_search_query(self, role: str, industry: str) -> str:
        """
        Build GitHub search query from role and industry
        
        Args:
            role: Job role
            industry: Industry sector
        
        Returns:
            GitHub search query string
        """
        # Extract keywords from role and industry
        role_keywords = self._extract_keywords(role)
        industry_keywords = self._extract_keywords(industry)
        
        # Build query with language and topic filters
        query_parts = []
        
        # Add industry-specific topics
        if industry_keywords:
            for keyword in industry_keywords[:2]:  # Limit to 2 keywords
                query_parts.append(f'topic:{keyword.lower()}')
        
        # Add role-specific keywords to description/readme
        if role_keywords:
            role_query = ' OR '.join(role_keywords[:3])  # Limit to 3 keywords
            query_parts.append(f'({role_query})')
        
        return ' '.join(query_parts) if query_parts else 'stars:>100'
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract meaningful keywords from text"""
        if not text:
            return []
        
        # Simple keyword extraction - split and filter
        words = text.lower().split()
        # Filter out common words and keep meaningful terms
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        keywords = [w for w in words if len(w) > 2 and w not in stop_words]
        return keywords
    
    def extract_skills_from_repos(self, role: str, industry: str, max_repos: int = 10) -> Dict[str, int]:
        """
        Extract and aggregate skills from GitHub repositories
        
        Args:
            role: Job role for search context
            industry: Industry for search context
            max_repos: Maximum number of repositories to analyze
        
        Returns:
            Dictionary with skill names as keys and counts as values
        """
        # Search repositories
        search_results = self.search_repositories(role, industry, max_repos)
        
        if not search_results or 'items' not in search_results:
            return {}
        
        repositories = search_results.get('items', [])
        all_skills = []
        
        for repo in repositories:
            # Extract skills from repository data
            repo_skills = self._extract_skills_from_repo(repo)
            all_skills.extend(repo_skills)
        
        # Aggregate skill counts
        skill_counts = Counter(all_skills)
        
        # Convert to regular dict and sort by count
        return dict(sorted(skill_counts.items(), key=lambda x: x[1], reverse=True))
    
    def _extract_skills_from_repo(self, repo: Dict) -> List[str]:
        """
        Extract skills from a single repository
        
        Args:
            repo: Repository data from GitHub API
        
        Returns:
            List of normalized skill names found in the repository
        """
        skills_found = []
        
        # Combine text sources from repository
        text_sources = []
        
        # Repository name and description
        if repo.get('name'):
            text_sources.append(repo['name'])
        if repo.get('description'):
            text_sources.append(repo['description'])
        
        # Programming language
        if repo.get('language'):
            text_sources.append(repo['language'])
        
        # Topics/tags
        if repo.get('topics'):
            text_sources.extend(repo['topics'])
        
        # Full name (owner/repo format might contain keywords)
        if repo.get('full_name'):
            text_sources.append(repo['full_name'])
        
        # Combine all text and extract skills
        combined_text = ' '.join(text_sources)
        if combined_text:
            extracted = self.skill_extractor.extract_skills(combined_text)
            skills_found = [skill['skill'] for skill in extracted]
        
        return skills_found
    
    def _get_mock_repositories(self, role: str, industry: str, count: int) -> Dict:
        """
        Generate mock repository data for testing
        
        Args:
            role: Job role
            industry: Industry sector
            count: Number of mock repositories to generate
        
        Returns:
            Mock GitHub API response structure
        """
        # Mock repositories with realistic data
        mock_repos = []
        
        # Role and industry-based mock data
        role_lower = role.lower()
        industry_lower = industry.lower()
        
        # Define mock repos based on role/industry
        base_repos = [
            {
                'name': 'fintech-backend-api',
                'full_name': 'company/fintech-backend-api',
                'description': 'Backend API for financial services built with Python, FastAPI, and PostgreSQL',
                'language': 'Python',
                'topics': ['fintech', 'api', 'python', 'fastapi', 'postgresql', 'backend'],
                'stars': 450,
                'forks': 120
            },
            {
                'name': 'payment-processing-service',
                'full_name': 'fintech/payment-processing-service',
                'description': 'Microservices architecture with Node.js, Express.js, and Redis for payment processing',
                'language': 'JavaScript',
                'topics': ['microservices', 'nodejs', 'express', 'redis', 'payments', 'fintech'],
                'stars': 320,
                'forks': 85
            },
            {
                'name': 'react-fintech-dashboard',
                'full_name': 'fintech/react-dashboard',
                'description': 'Financial dashboard built with React, TypeScript, and Tailwind CSS',
                'language': 'TypeScript',
                'topics': ['react', 'typescript', 'frontend', 'dashboard', 'fintech'],
                'stars': 280,
                'forks': 65
            },
            {
                'name': 'backend-engineer-toolkit',
                'full_name': 'opensource/backend-toolkit',
                'description': 'Collection of backend tools and utilities using Python, Flask, Docker, and AWS',
                'language': 'Python',
                'topics': ['backend', 'python', 'flask', 'docker', 'aws', 'devops'],
                'stars': 210,
                'forks': 45
            },
            {
                'name': 'api-gateway-service',
                'full_name': 'company/api-gateway',
                'description': 'REST API gateway implementation with Java, Spring Boot, and Kubernetes',
                'language': 'Java',
                'topics': ['java', 'spring', 'kubernetes', 'api-gateway', 'microservices'],
                'stars': 180,
                'forks': 38
            },
            {
                'name': 'nextjs-finance-app',
                'full_name': 'fintech/nextjs-app',
                'description': 'Modern finance application with Next.js, React, and PostgreSQL',
                'language': 'TypeScript',
                'topics': ['nextjs', 'react', 'typescript', 'postgresql', 'finance'],
                'stars': 150,
                'forks': 32
            },
            {
                'name': 'backend-cache-layer',
                'full_name': 'backend/cache-service',
                'description': 'Distributed caching solution using Redis, Docker, and CI/CD pipelines',
                'language': 'Python',
                'topics': ['redis', 'docker', 'cicd', 'backend', 'caching'],
                'stars': 125,
                'forks': 28
            },
            {
                'name': 'graphql-api-server',
                'full_name': 'api/graphql-server',
                'description': 'GraphQL API server built with Node.js, Express.js, and MongoDB',
                'language': 'JavaScript',
                'topics': ['graphql', 'nodejs', 'express', 'mongodb', 'api'],
                'stars': 110,
                'forks': 25
            }
        ]
        
        # Filter and select based on role/industry keywords
        if 'backend' in role_lower or 'engineer' in role_lower:
            # Prefer backend-related repos
            selected = [r for r in base_repos if any(
                keyword in r['description'].lower() or keyword in ' '.join(r['topics'])
                for keyword in ['backend', 'api', 'service', 'server']
            )]
        elif 'frontend' in role_lower:
            selected = [r for r in base_repos if any(
                keyword in r['description'].lower() or keyword in ' '.join(r['topics'])
                for keyword in ['react', 'frontend', 'dashboard', 'ui']
            )]
        else:
            selected = base_repos
        
        # Industry filtering
        if 'fintech' in industry_lower or 'finance' in industry_lower:
            fintech_repos = [r for r in base_repos if 'fintech' in r['description'].lower() or 'fintech' in ' '.join(r['topics'])]
            selected = fintech_repos if fintech_repos else selected
        
        # Limit to requested count
        mock_repos = selected[:count] if selected else base_repos[:count]
        
        return {
            'total_count': len(mock_repos),
            'incomplete_results': False,
            'items': mock_repos
        }

