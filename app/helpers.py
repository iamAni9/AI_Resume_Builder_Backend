"""
Helper utility functions
"""
import re
from typing import List, Dict
from datetime import datetime
from app.config.logger import get_logger

logger = get_logger("helpers")

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent security issues
    
    Args:
        filename: Original filename
        
    Returns:
        Safe filename
    """
    # Remove any non-alphanumeric characters except . and -
    safe_name = re.sub(r'[^\w\s.-]', '', filename)
    # Replace spaces with underscores
    safe_name = safe_name.replace(' ', '_')
    # Limit length
    return safe_name[:255]


def extract_text_sections(text: str) -> Dict[str, str]:
    """
    Extract major sections from resume text
    
    Args:
        text: Resume text
        
    Returns:
        Dictionary with extracted sections
    """
    sections = {
        'summary': '',
        'experience': '',
        'education': '',
        'skills': '',
        'projects': '',
        'certifications': ''
    }
    
    section_patterns = {
        'summary': r'(?:professional\s+summary|objective|about|profile)(.*?)(?=(?:professional\s+experience|education|skills|projects|certification|$))',
        'experience': r'(?:professional\s+experience|work\s+history|employment)(.*?)(?=(?:education|skills|projects|certification|$))',
        'education': r'(?:education|academic)(.*?)(?=(?:skills|projects|certification|$))',
        'skills': r'(?:skills|technical\s+skills)(.*?)(?=(?:projects|certification|$))',
        'projects': r'(?:projects|portfolio|work\s+samples)(.*?)(?=(?:certification|$))',
        'certifications': r'(?:certification|license)(.*?)$'
    }
    
    for section, pattern in section_patterns.items():
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            sections[section] = match.group(1).strip()
    
    return sections


def count_keywords(text: str, keywords: List[str]) -> Dict[str, int]:
    """
    Count occurrences of keywords in text
    
    Args:
        text: Text to search in
        keywords: List of keywords to search for
        
    Returns:
        Dictionary with keyword counts
    """
    text_lower = text.lower()
    counts = {}
    
    for keyword in keywords:
        pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
        matches = re.findall(pattern, text_lower)
        counts[keyword] = len(matches)
    
    return counts


def get_keyword_density(text: str, keyword: str) -> float:
    """
    Calculate keyword density in text
    
    Args:
        text: Text to analyze
        keyword: Keyword to check
        
    Returns:
        Keyword density as percentage
    """
    words = text.lower().split()
    keyword_lower = keyword.lower()
    
    if len(words) == 0:
        return 0.0
    
    keyword_count = len([w for w in words if keyword_lower in w])
    density = (keyword_count / len(words)) * 100
    
    return round(density, 2)


def validate_email(email: str) -> bool:
    """
    Validate email address format
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """
    Validate phone number format
    
    Args:
        phone: Phone number to validate
        
    Returns:
        True if valid, False otherwise
    """
    # Remove common separators
    cleaned = re.sub(r'[\s\-\(\).]', '', phone)
    # Check if it's at least 10 digits
    return len(re.findall(r'\d', cleaned)) >= 10


def format_date(date_str: str) -> str:
    """
    Format date string to standard format
    
    Args:
        date_str: Date string to format
        
    Returns:
        Formatted date string
    """
    # Common date formats
    formats = [
        '%Y-%m-%d',
        '%m/%d/%Y',
        '%d/%m/%Y',
        '%B %Y',
        '%b %Y',
        '%Y',
    ]
    
    for fmt in formats:
        try:
            parsed = datetime.strptime(date_str.strip(), fmt)
            return parsed.strftime('%B %Y')
        except ValueError:
            continue
    
    # If no format matches, return original
    return date_str


def truncate_text(text: str, max_length: int, suffix: str = '...') -> str:
    """
    Truncate text to maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def merge_bullets(bullets: List[str]) -> str:
    """
    Merge bullet points into formatted text
    
    Args:
        bullets: List of bullet points
        
    Returns:
        Formatted bullet text
    """
    if not bullets:
        return ""
    
    return "\n".join([f"• {bullet}" for bullet in bullets if bullet.strip()])


def extract_ats_keywords(resume_text: str) -> Dict[str, List[str]]:
    """
    Extract common ATS keywords from resume
    
    Args:
        resume_text: Resume text to analyze
        
    Returns:
        Dictionary with categorized keywords
    """
    text_lower = resume_text.lower()
    
    # Common ATS keyword categories
    keywords = {
        'programming_languages': [
            'python', 'javascript', 'java', 'csharp', 'c++', 'ruby', 'php',
            'swift', 'kotlin', 'golang', 'rust', 'typescript', 'sql'
        ],
        'frameworks': [
            'react', 'angular', 'vue', 'django', 'flask', 'fastapi',
            'spring', 'express', 'laravel', 'asp.net'
        ],
        'databases': [
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'firebase',
            'dynamodb', 'elasticsearch', 'cassandra'
        ],
        'tools': [
            'git', 'docker', 'kubernetes', 'jenkins', 'gitlab', 'github',
            'jira', 'aws', 'azure', 'gcp', 'linux', 'unix'
        ],
        'soft_skills': [
            'leadership', 'communication', 'teamwork', 'problem solving',
            'project management', 'critical thinking', 'collaboration'
        ]
    }
    
    found_keywords = {}
    
    for category, keyword_list in keywords.items():
        found = []
        for keyword in keyword_list:
            if keyword in text_lower:
                found.append(keyword)
        found_keywords[category] = found
    
    return found_keywords


def generate_job_match_score(resume_data: Dict, job_description: str) -> float:
    """
    Generate a job match score based on resume and job description
    
    Args:
        resume_data: Resume data
        job_description: Job description text
        
    Returns:
        Match score (0-100)
    """
    if not job_description:
        return 0.0
    
    resume_text = " ".join([
        str(resume_data.get('personal_info', {}).get('name', '')),
        " ".join(resume_data.get('skills', [])),
        json.dumps(resume_data.get('experience', []))
    ])
    
    # Extract keywords from both
    job_words = set(job_description.lower().split())
    resume_words = set(resume_text.lower().split())
    
    # Calculate intersection
    common_words = job_words.intersection(resume_words)
    
    # Calculate match percentage
    if len(job_words) == 0:
        return 0.0
    
    match_score = (len(common_words) / len(job_words)) * 100
    
    return round(min(match_score, 100), 2)


import json
