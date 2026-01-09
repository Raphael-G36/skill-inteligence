from typing import Dict, List, Optional
from collections import Counter
from app.services.skill_extraction_service import SkillExtractionService


class JobPostingIngestionService:
    """Service for ingesting and analyzing job postings"""
    
    def __init__(self, skill_extraction_service: Optional[SkillExtractionService] = None):
        """
        Initialize job posting ingestion service
        
        Args:
            skill_extraction_service: Optional skill extraction service instance
        """
        self.skill_extractor = skill_extraction_service or SkillExtractionService()
    
    def extract_skills_from_job_description(self, job_description: str) -> List[Dict[str, str]]:
        """
        Extract skills from a single job description
        
        Args:
            job_description: Raw job description text
        
        Returns:
            List of dictionaries containing normalized skill name and category
        """
        if not job_description or not isinstance(job_description, str):
            return []
        
        # Extract skills using the skill extraction service
        extracted_skills = self.skill_extractor.extract_skills(job_description)
        return extracted_skills
    
    def aggregate_skill_counts(self, job_descriptions: List[str]) -> Dict[str, int]:
        """
        Extract and aggregate skill counts from multiple job descriptions
        
        Args:
            job_descriptions: List of job description texts
        
        Returns:
            Dictionary with skill names as keys and frequency counts as values
        """
        all_skills = []
        
        for job_description in job_descriptions:
            if not job_description or not isinstance(job_description, str):
                continue
            
            # Extract skills from each job description
            extracted_skills = self.extract_skills_from_job_description(job_description)
            skill_names = [skill['skill'] for skill in extracted_skills]
            all_skills.extend(skill_names)
        
        # Aggregate skill counts
        skill_counts = Counter(all_skills)
        
        # Convert to regular dict and sort by count (descending)
        return dict(sorted(skill_counts.items(), key=lambda x: x[1], reverse=True))
    
    def get_mock_job_descriptions(self, role: str = None, industry: str = None, count: int = 5) -> List[str]:
        """
        Generate mock job descriptions for testing
        
        Args:
            role: Optional job role to filter mock data
            industry: Optional industry to filter mock data
            count: Number of mock job descriptions to generate
        
        Returns:
            List of mock job description texts
        """
        # Base mock job descriptions
        mock_jobs = [
            """Backend Engineer - FinTech Startup

We are seeking an experienced Backend Engineer to join our growing FinTech team. 
You will be responsible for building scalable backend services using Python and FastAPI.

Requirements:
- 3+ years of experience with Python
- Strong knowledge of REST API design
- Experience with PostgreSQL databases
- Familiarity with Docker and containerization
- Understanding of microservices architecture
- Knowledge of CI/CD pipelines
- Experience with cloud platforms (AWS preferred)

Nice to have:
- Experience with Redis for caching
- GraphQL API development
- Experience in the financial services industry""",
            
            """Senior Full Stack Developer - E-commerce Platform

Join our dynamic team building the next-generation e-commerce platform. 
We're looking for a Full Stack Developer with expertise in modern web technologies.

Required Skills:
- JavaScript and TypeScript
- React.js for frontend development
- Node.js and Express.js for backend
- PostgreSQL database experience
- REST API development
- Git version control

Additional Skills:
- Next.js framework experience
- Docker and Kubernetes
- AWS cloud services
- HTML and CSS expertise
- Experience with Tailwind CSS""",
            
            """Backend Developer - Cloud Services

We're hiring a Backend Developer to build robust cloud-based solutions. 
You'll work on distributed systems and API services.

Technical Requirements:
- Java programming experience
- Spring Boot framework
- Microservices architecture
- Docker containerization
- Kubernetes orchestration
- REST API design
- Database design with MySQL or PostgreSQL
- Git and version control

Bonus:
- AWS or Azure cloud experience
- CI/CD implementation experience
- GraphQL knowledge""",
            
            """Frontend Engineer - SaaS Product

Looking for a Frontend Engineer to help build beautiful, responsive user interfaces 
for our SaaS platform.

Required:
- React.js and TypeScript
- HTML5 and CSS3
- Next.js framework
- JavaScript (ES6+)
- REST API integration
- Git workflow

Preferred:
- Tailwind CSS or SASS
- Vue.js experience
- GraphQL client experience
- Docker basics""",
            
            """DevOps Engineer - Infrastructure Team

We need a DevOps Engineer to help maintain and scale our infrastructure.

Must Have:
- Docker containerization
- Kubernetes experience
- CI/CD pipeline setup
- AWS cloud platform
- Git version control
- Linux system administration

Nice to Have:
- Azure or GCP experience
- Microservices deployment experience
- Infrastructure as Code (IaC)
- Monitoring and observability tools""",
            
            """Python Developer - Data Platform

Join our data platform team building scalable data processing systems.

Requirements:
- Python programming (Python 3.x)
- PostgreSQL database
- REST API development
- Docker containerization
- Git version control
- API design and development

Additional:
- FastAPI or Flask framework
- Redis caching
- AWS services
- Microservices architecture""",
            
            """Node.js Developer - Real-time Applications

We're building real-time communication features and need a skilled Node.js developer.

Technical Skills:
- Node.js runtime
- Express.js framework
- JavaScript and TypeScript
- REST API and GraphQL
- PostgreSQL or MongoDB
- Docker containers
- Git workflow

Preferred:
- Microservices experience
- Redis caching
- AWS cloud services
- CI/CD pipelines""",
            
            """React Developer - Financial Dashboard

Build beautiful financial dashboards and data visualization tools.

Required Skills:
- React.js framework
- TypeScript
- JavaScript
- HTML and CSS
- REST API integration
- Git version control

Additional:
- Next.js experience
- Tailwind CSS
- PostgreSQL knowledge
- Docker basics""",
            
            """Java Backend Developer - Enterprise Software

Develop robust enterprise-grade backend services using Java.

Must Have:
- Java programming (Java 8+)
- Spring Boot framework
- REST API development
- PostgreSQL or MySQL
- Docker and Kubernetes
- Git version control
- Microservices architecture

Preferred:
- AWS cloud experience
- CI/CD experience
- API gateway experience
- GraphQL knowledge""",
            
            """Full Stack Engineer - Startup

Fast-growing startup seeking a Full Stack Engineer to build our core product.

Tech Stack:
- JavaScript and TypeScript
- React.js frontend
- Node.js backend
- Express.js framework
- PostgreSQL database
- Docker containers
- AWS cloud platform
- Git version control

Additional:
- Next.js framework
- REST API design
- CI/CD pipelines
- Microservices architecture"""
        ]
        
        # Filter based on role if provided
        filtered_jobs = mock_jobs
        if role:
            role_lower = role.lower()
            if 'backend' in role_lower or 'engineer' in role_lower:
                filtered_jobs = [job for job in mock_jobs if 'backend' in job.lower() or 'engineer' in job.lower()]
            elif 'frontend' in role_lower:
                filtered_jobs = [job for job in mock_jobs if 'frontend' in job.lower()]
            elif 'full' in role_lower or 'stack' in role_lower:
                filtered_jobs = [job for job in mock_jobs if 'full' in job.lower() or 'stack' in job.lower()]
            elif 'devops' in role_lower:
                filtered_jobs = [job for job in mock_jobs if 'devops' in job.lower()]
        
        # Filter based on industry if provided
        if industry:
            industry_lower = industry.lower()
            if 'fintech' in industry_lower or 'finance' in industry_lower:
                filtered_jobs = [job for job in filtered_jobs if 'fintech' in job.lower() or 'financial' in job.lower()]
        
        # If filtering resulted in empty list, use original list
        if not filtered_jobs:
            filtered_jobs = mock_jobs
        
        # Return requested count
        return filtered_jobs[:count]

