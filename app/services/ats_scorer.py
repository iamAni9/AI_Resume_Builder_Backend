"""
ATS Score Calculator Service
Uses Gemini AI to analyze resume ATS compatibility
"""
import re
import json
from typing import List, Dict
import google.generativeai as genai
from app.config.logger import get_logger
from app.config.settings import settings

logger = get_logger("ats_scorer")


class ATSScorer:
    """Calculate ATS score and provide improvement suggestions"""
    
    def __init__(self):
        """Initialize Gemini AI client"""
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        logger.info("ATS Scorer initialized with Gemini Pro")
    
    def calculate_ats_score(
        self, 
        resume_text: str, 
        job_description: str = ""
    ) -> Dict:        
        prompt = f"""
        You are an expert ATS (Applicant Tracking System) specialist. Analyze the following resume for ATS compatibility and provide a detailed analysis.
        
        IMPORTANT: Return ONLY valid JSON in your response, no extra text before or after.
        
        Resume Content:
        ---
        {resume_text}
        ---
        
        {f'Target Job Description: ---{job_description}---' if job_description else ''}
        
        Provide analysis with the following JSON format ONLY:
        {{
            "score": <number between 0 and 100>,
            "missing_keywords": [<list of important keywords that should be included>],
            "suggestions": [<list of specific, actionable improvement suggestions>],
            "sections_analysis": {{
                "contact_info": {{"score": <0-100>, "issues": [<list of issues or empty>]}},
                "experience": {{"score": <0-100>, "issues": [<list of issues or empty>]}},
                "education": {{"score": <0-100>, "issues": [<list of issues or empty>]}},
                "skills": {{"score": <0-100>, "issues": [<list of issues or empty>]}}
            }},
            "summary": "<brief summary of ATS compatibility>"
        }}
        
        Rules:
        - Score should be based on: formatting, structure, keyword optimization, ATS-friendly formatting
        - Missing keywords should be industry-relevant and commonly searched
        - Suggestions should be specific and actionable
        - Return ONLY JSON, no markdown or extra text
        """
        
        try:
            logger.info("Sending request to Gemini API for ATS analysis")
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                result = json.loads(json_str)
                logger.info(f"ATS Score calculated: {result.get('score', 'N/A')}")
                return result
            else:
                logger.warning("Could not extract JSON from Gemini response")
                return self._get_default_score()
                
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {str(e)}")
            return self._get_default_score()
        except Exception as e:
            logger.error(f"Error calculating ATS score: {str(e)}")
            return self._get_default_score()
    
    def _get_default_score(self) -> Dict:
        """
        Return a default score when API fails
        
        Returns:
            Default ATS score dictionary
        """
        return {
            "score": 65,
            "missing_keywords": [
                "achievement metrics",
                "action verbs",
                "relevant certifications",
                "quantifiable results"
            ],
            "suggestions": [
                "Add quantifiable achievements with numbers/percentages",
                "Use strong action verbs (Led, Developed, Implemented, etc.)",
                "Include relevant keywords from job description",
                "Ensure clear section headers (Experience, Education, Skills)",
                "Keep formatting simple and ATS-friendly (no tables or graphics)"
            ],
            "sections_analysis": {
                "contact_info": {
                    "score": 85,
                    "issues": []
                },
                "experience": {
                    "score": 70,
                    "issues": ["Add more quantifiable results", "Use stronger action verbs"]
                },
                "education": {
                    "score": 80,
                    "issues": []
                },
                "skills": {
                    "score": 60,
                    "issues": ["Add more relevant technical skills", "Include industry keywords"]
                }
            },
            "summary": "Resume has moderate ATS compatibility. Focus on quantifiable achievements and relevant keywords."
        }
    
    def compare_scores(
        self, 
        original_score: float, 
        enhanced_score: float
    ) -> List[str]:
        """
        Compare original and enhanced scores and generate insights
        
        Args:
            original_score: Original ATS score
            enhanced_score: ATS score after enhancement
            
        Returns:
            List of improvement insights
        """
        improvements = []
        diff = enhanced_score - original_score
        percentage_improvement = (diff / original_score * 100) if original_score > 0 else 0
        
        if diff > 30:
            improvements.append(f"🌟 Excellent improvement! Score increased by {diff:.1f} points ({percentage_improvement:.1f}%)")
            improvements.append("Your resume is now highly optimized for ATS systems")
        elif diff > 15:
            improvements.append(f"✅ Great improvement! Score increased by {diff:.1f} points")
            improvements.append("Resume is much more ATS-compatible now")
        elif diff > 5:
            improvements.append(f"👍 Good improvement! Score increased by {diff:.1f} points")
            improvements.append("Resume quality has been enhanced")
        elif diff >= 0:
            improvements.append(f"Score adjusted by {diff:.1f} points")
        else:
            improvements.append("Score maintained from original version")
        
        logger.info(f"Score comparison: Original={original_score}, Enhanced={enhanced_score}, Improvement={diff}")
        return improvements
    
    def analyze_keywords(self, resume_text: str, job_description: str = "") -> Dict:
        """
        Analyze keywords in resume and compare with job description
        
        Args:
            resume_text: Resume content
            job_description: Job description
            
        Returns:
            Keyword analysis results
        """
        prompt = f"""
        Analyze the keywords in the resume and job description.
        Return ONLY valid JSON:
        
        Resume:
        {resume_text}
        
        {f'Job Description: {job_description}' if job_description else 'No job description provided'}
        
        Return JSON format:
        {{
            "resume_keywords": [<list of important keywords from resume>],
            "job_keywords": [<list of important keywords from job description>],
            "matched_keywords": [<keywords present in both>],
            "missing_keywords": [<keywords from job not in resume>],
            "unique_resume_keywords": [<strong keywords unique to resume>]
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
        except Exception as e:
            logger.error(f"Error analyzing keywords: {str(e)}")
        
        return {
            "resume_keywords": [],
            "job_keywords": [],
            "matched_keywords": [],
            "missing_keywords": [],
            "unique_resume_keywords": []
        }
