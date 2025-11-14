"""
AI Resume Enhancement Service
Uses Gemini AI to improve resume content
"""
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Dict, List
import json
import re
from app.config.logger import get_logger
from app.config.settings import settings

logger = get_logger("ai_enhancer")


class AIEnhancer:
    """Enhance resume content using Gemini AI"""
    
    def __init__(self):
        """Initialize Gemini AI client"""
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        logger.info("AI Enhancer initialized with Gemini Pro")
    
    def enhance_resume_content(
        self, 
        resume_data: Dict, 
        job_description: str = ""
    ) -> Dict:
        """
        Enhance resume content with AI
        
        Args:
            resume_data: Complete resume data dictionary
            job_description: Optional job description for targeted enhancement
            
        Returns:
            Enhanced resume data
        """
        
        prompt = f"""
        You are an expert resume writer and ATS optimization specialist. Enhance the provided resume to:
        1. Improve grammar, syntax, and professional language
        2. Optimize keywords for ATS systems
        3. Make achievements more impactful using strong action verbs
        4. Quantify results wherever possible
        5. Maintain professional tone and readability
        6. Highlight leadership and impact
        
        Resume Data to Enhance:
        {json.dumps(resume_data, indent=2)}
        
        {f'Target Job Description (for keyword optimization): {job_description} if job_description else No specific job description provided'}
        
        IMPORTANT: Return the enhanced resume in the same JSON structure as above, with improved content.
        Preserve all fields and structure. Return ONLY valid JSON, no extra text.
        
        Enhanced Resume (JSON only):
        """
        
        try:
            logger.info("Sending enhancement request to Gemini API")
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                enhanced_data = json.loads(json_str)
                logger.info("Resume content enhanced successfully")
                return enhanced_data
            else:
                logger.warning("Could not extract JSON from enhancement response")
                return resume_data
                
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error during enhancement: {str(e)}")
            return resume_data
        except Exception as e:
            logger.error(f"Error enhancing resume: {str(e)}")
            return resume_data
    
    def enhance_section(
        self, 
        section_name: str, 
        content: str,
        context: str = ""
    ) -> str:
        """
        Enhance a specific section of the resume
        
        Args:
            section_name: Name of the section (e.g., 'experience', 'summary')
            content: Content to enhance
            context: Additional context or job description
            
        Returns:
            Enhanced section content
        """
        
        prompt = f"""
        You are an expert resume writer. Enhance the following {section_name} section of a resume:
        
        Original Content:
        {content}
        
        {f'Context/Job Description: {context}' if context else ''}
        
        Improvements needed:
        - Use stronger action verbs (Led, Developed, Implemented, Optimized, etc.)
        - Include quantifiable metrics and results (numbers, percentages, improvements)
        - Keep it concise and impactful
        - Use keywords relevant to the role
        - Maintain professional tone
        
        Return ONLY the enhanced content without any explanation.
        """
        
        try:
            response = self.model.generate_content(prompt)
            enhanced_content = response.text.strip()
            logger.info(f"Section '{section_name}' enhanced successfully")
            return enhanced_content
        except Exception as e:
            logger.error(f"Error enhancing {section_name}: {str(e)}")
            return content
    
    def generate_summary(self, resume_data: Dict) -> str:
        """
        Generate a professional summary from resume data
        
        Args:
            resume_data: Complete resume data
            
        Returns:
            Generated professional summary (2-3 sentences)
        """
        
        prompt = f"""
        Create a compelling professional summary (2-3 sentences) based on this resume data:
        {json.dumps(resume_data, indent=2)}
        
        The summary should:
        - Highlight key strengths and years of experience
        - Be concise and impactful
        - Use professional language and power words
        - Include relevant keywords
        - Showcase unique value proposition
        - Be suitable for ATS systems
        
        Return ONLY the professional summary text, no additional explanation.
        """
        
        try:
            response = self.model.generate_content(prompt)
            summary = response.text.strip()
            logger.info("Professional summary generated")
            return summary
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            return "Experienced professional with strong technical background and proven track record of delivering results."
    
    def enhance_bullet_points(self, bullet_points: List[str]) -> List[str]:
        """
        Enhance a list of bullet points/responsibilities
        
        Args:
            bullet_points: List of bullet points to enhance
            
        Returns:
            Enhanced list of bullet points
        """
        
        prompt = f"""
        Enhance these bullet points to be more impactful and ATS-friendly:
        
        {json.dumps(bullet_points, indent=2)}
        
        For each bullet point:
        - Start with a strong action verb
        - Include quantifiable results if possible (numbers, percentages, improvements)
        - Keep it concise (one line)
        - Use professional language
        
        Return ONLY a JSON array of enhanced bullet points, no explanation:
        ["enhanced point 1", "enhanced point 2", ...]
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Extract JSON array from response
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if json_match:
                enhanced_points = json.loads(json_match.group(0))
                logger.info(f"Enhanced {len(enhanced_points)} bullet points")
                return enhanced_points
            else:
                return bullet_points
                
        except json.JSONDecodeError:
            logger.warning("Could not parse enhanced bullet points JSON")
            return bullet_points
        except Exception as e:
            logger.error(f"Error enhancing bullet points: {str(e)}")
            return bullet_points
    
    def suggest_improvements(self, resume_text: str) -> List[str]:
        """
        Get specific improvement suggestions for resume
        
        Args:
            resume_text: Complete resume text
            
        Returns:
            List of improvement suggestions
        """
        
        prompt = f"""
        Analyze this resume and provide 5-7 specific, actionable improvement suggestions:
        
        {resume_text}
        
        Suggestions should be:
        - Specific and actionable
        - Ranked by impact (most important first)
        - Focused on ATS optimization and impact
        - Practical to implement
        
        Return ONLY a JSON array of strings:
        ["suggestion 1", "suggestion 2", ...]
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Extract JSON array
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if json_match:
                suggestions = json.loads(json_match.group(0))
                logger.info(f"Generated {len(suggestions)} improvement suggestions")
                return suggestions
            else:
                return [
                    "Add more quantifiable achievements with metrics",
                    "Use stronger action verbs for better impact",
                    "Include relevant industry keywords",
                    "Keep formatting simple and ATS-friendly",
                    "Tailor content to target position"
                ]
                
        except json.JSONDecodeError:
            logger.warning("Could not parse suggestions JSON")
            return []
        except Exception as e:
            logger.error(f"Error generating suggestions: {str(e)}")
            return []
    
    def generate_cover_letter_snippet(self, resume_data: Dict) -> str:
        """
        Generate a brief cover letter opening based on resume
        
        Args:
            resume_data: Complete resume data
            
        Returns:
            Cover letter opening (2-3 sentences)
        """
        
        prompt = f"""
        Generate a compelling cover letter opening (2-3 sentences) based on this resume:
        {json.dumps(resume_data, indent=2)}
        
        The opening should:
        - Be engaging and professional
        - Highlight key strengths
        - Show enthusiasm and motivation
        - Be suitable for tailoring to different roles
        
        Return ONLY the cover letter opening, no extra text.
        """
        
        try:
            response = self.model.generate_content(prompt)
            cover_letter = response.text.strip()
            logger.info("Cover letter snippet generated")
            return cover_letter
        except Exception as e:
            logger.error(f"Error generating cover letter: {str(e)}")
            return "Highly motivated professional with strong technical background seeking to leverage expertise in innovative projects."
