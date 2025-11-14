"""
PDF Resume Parser Service
Extracts text and structured data from PDF resumes
"""
import fitz  # PyMuPDF
import re
from typing import Dict, List
from app.config.logger import get_logger

logger = get_logger("pdf_parser")

class PDFParser:
    """Parse PDF resumes and extract structured data"""
    
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        """
        Extract all text from a PDF file
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Extracted text from all pages
            
        Raises:
            Exception: If PDF parsing fails
        """
        try:
            doc = fitz.open(file_path)
            text = ""
            
            for page_num, page in enumerate(doc):
                text += page.get_text()
                logger.info(f"Extracted text from page {page_num + 1}")
            
            doc.close()
            logger.info(f"Successfully extracted text from PDF: {file_path}")
            return text
            
        except Exception as e:
            logger.error(f"Error parsing PDF: {str(e)}")
            raise Exception(f"Error parsing PDF: {str(e)}")
    
    @staticmethod
    def extract_email(text: str) -> str:
        """
        Extract email address from text
        
        Args:
            text: Text content to search
            
        Returns:
            First email found or empty string
        """
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        
        if emails:
            logger.info(f"Found email: {emails[0]}")
            return emails[0]
        
        logger.warning("No email found in text")
        return ""
    
    @staticmethod
    def extract_phone(text: str) -> str:
        """
        Extract phone number from text
        
        Args:
            text: Text content to search
            
        Returns:
            First phone number found or empty string
        """
        # Matches international and local phone formats
        phone_pattern = r'\+?[\d\s\-\(\)]{10,}'
        phones = re.findall(phone_pattern, text)
        
        if phones:
            phone = phones[0].strip()
            logger.info(f"Found phone: {phone}")
            return phone
        
        logger.warning("No phone found in text")
        return ""
    
    @staticmethod
    def extract_sections(text: str) -> Dict[str, str]:
        """
        Extract different sections from resume
        
        Args:
            text: Full resume text
            
        Returns:
            Dictionary with extracted sections
        """
        sections = {
            'education': '',
            'experience': '',
            'skills': '',
            'projects': '',
            'certifications': '',
            'summary': ''
        }
        
        text_lower = text.lower()
        lines = text.split('\n')
        
        # Section keywords mapping
        section_keywords = {
            'education': ['education', 'academic', 'qualification', 'degree', 'university'],
            'experience': ['experience', 'work history', 'employment', 'professional experience'],
            'skills': ['skills', 'technical skills', 'competencies', 'abilities'],
            'projects': ['projects', 'portfolio', 'work samples'],
            'certifications': ['certifications', 'certificates', 'licenses', 'awards'],
            'summary': ['summary', 'objective', 'professional summary', 'about', 'profile']
        }
        
        current_section = None
        section_content = []
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check if this line starts a new section
            section_found = False
            for section, keywords in section_keywords.items():
                if any(keyword in line_lower for keyword in keywords) and len(line_lower) < 50:
                    # Save previous section
                    if current_section and section_content:
                        sections[current_section] = '\n'.join(section_content)
                    
                    current_section = section
                    section_content = []
                    section_found = True
                    break
            
            # If we're in a section, add the line to content
            if current_section and not section_found and line.strip():
                section_content.append(line)
        
        # Save last section
        if current_section and section_content:
            sections[current_section] = '\n'.join(section_content)
        
        logger.info("Successfully extracted resume sections")
        return sections
    
    @staticmethod
    def parse_resume(file_path: str) -> Dict:
        """
        Parse complete resume and return structured data
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Dictionary with parsed resume data
        """
        try:
            text = PDFParser.extract_text_from_pdf(file_path)
            
            parsed_data = {
                'raw_text': text,
                'email': PDFParser.extract_email(text),
                'phone': PDFParser.extract_phone(text),
                'sections': PDFParser.extract_sections(text),
                'word_count': len(text.split()),
                'page_count': len(text.split('\n\n'))  # Approximate page count
            }
            
            logger.info("Resume parsing completed successfully")
            return parsed_data
            
        except Exception as e:
            logger.error(f"Error parsing resume: {str(e)}")
            raise
