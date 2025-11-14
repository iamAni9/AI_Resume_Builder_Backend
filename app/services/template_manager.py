"""
Template Manager Service
Manages LaTeX resume templates
"""
import os
from typing import Dict, List
from app.config.logger import get_logger

logger = get_logger("template_manager")

class TemplateManager:
    """Manage LaTeX resume templates"""
    
    TEMPLATES_DIR = "templates"
    
    @staticmethod
    def get_template(template_name: str) -> str:
        """
        Load LaTeX template by name
        
        Args:
            template_name: Name of the template (e.g., 'template1')
            
        Returns:
            Template content or default template
        """
        template_path = os.path.join(TemplateManager.TEMPLATES_DIR, f"{template_name}.tex")
        
        try:
            if os.path.exists(template_path):
                with open(template_path, 'r', encoding='utf-8') as f:
                    template = f.read()
                logger.info(f"Loaded template: {template_name}")
                return template
            else:
                logger.warning(f"Template not found: {template_name}, using default")
                return TemplateManager.get_default_template()
        except Exception as e:
            logger.error(f"Error loading template: {str(e)}")
            return TemplateManager.get_default_template()
    
    @staticmethod
    def get_default_template() -> str:
        """
        Return default ATS-friendly LaTeX template
        
        Returns:
            Default LaTeX template
        """
        return r"""
\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[margin=0.75in]{geometry}
\usepackage{enumitem}
\usepackage{hyperref}
\usepackage{titlesec}
\usepackage{xcolor}

% Define colors
\definecolor{headercolor}{RGB}{25, 118, 210}
\definecolor{sectioncolor}{RGB}{25, 118, 210}

% Section formatting
\titleformat{\section}{\large\bfseries\color{sectioncolor}}{}{0em}{}[\titlerule]
\titleformat{\subsection}{\bfseries}{}{0em}{}
\titlespacing{\section}{0pt}{12pt}{6pt}
\titlespacing{\subsection}{0pt}{6pt}{3pt}

% List formatting
\setlist[itemize]{leftmargin=*,nosep,before=\vspace{-0.5\baselineskip},after=\vspace{-0.5\baselineskip}}

\begin{document}

% Header - Name
\begin{center}
    {\Large\bfseries\color{headercolor} NAME}\\[0.2cm]
    \normalsize EMAIL | PHONE | LOCATION\\
    \small WEBSITE
\end{center}

\section*{Professional Summary}
Professional summary goes here.

\section*{Professional Experience}

\subsection*{Job Title at Company}
\textit{Start Date - End Date | Location}
\begin{itemize}
    \item Achievement or responsibility with metrics
    \item Key accomplishment with quantifiable result
    \item Leadership or impact demonstration
\end{itemize}

\section*{Education}

\subsection*{Degree in Field}
Institution | Start Date - End Date | GPA: X.XX

\section*{Skills}
Skill1, Skill2, Skill3, Skill4, Skill5, Skill6

\section*{Projects}

\subsection*{Project Name}
Brief project description here.
\textit{Technologies: Tech1, Tech2, Tech3}

\section*{Certifications}
\begin{itemize}
    \item Certification Name - Issuing Body (Year)
    \item Another Certification - Issuing Body (Year)
\end{itemize}

\end{document}
"""
    
    @staticmethod
    def populate_template(template: str, data: Dict) -> str:
        """
        Populate template with resume data
        
        Args:
            template: Template string
            data: Dictionary with resume data
            
        Returns:
            Populated template
        """
        populated = template
        
        # Simple string replacement (basic implementation)
        # In production, use proper templating engine like Jinja2
        replacements = {
            'NAME': data.get('personal_info', {}).get('name', 'Your Name'),
            'EMAIL': data.get('personal_info', {}).get('email', ''),
            'PHONE': data.get('personal_info', {}).get('phone', ''),
            'LOCATION': data.get('personal_info', {}).get('location', ''),
            'WEBSITE': data.get('personal_info', {}).get('website', ''),
        }
        
        for key, value in replacements.items():
            populated = populated.replace(key, str(value))
        
        logger.info("Template populated with resume data")
        return populated
    
    @staticmethod
    def list_available_templates() -> List[str]:
        """
        List all available templates
        
        Returns:
            List of available template names
        """
        try:
            if os.path.exists(TemplateManager.TEMPLATES_DIR):
                templates = [
                    f[:-4] for f in os.listdir(TemplateManager.TEMPLATES_DIR)
                    if f.endswith('.tex')
                ]
                logger.info(f"Found {len(templates)} templates")
                return sorted(templates)
            else:
                logger.warning(f"Templates directory not found: {TemplateManager.TEMPLATES_DIR}")
                return ['template1', 'template2']
        except Exception as e:
            logger.error(f"Error listing templates: {str(e)}")
            return ['template1', 'template2']
    
    @staticmethod
    def create_template(template_name: str, content: str) -> bool:
        """
        Create/save a new template
        
        Args:
            template_name: Name for the template
            content: LaTeX template content
            
        Returns:
            True if successful, False otherwise
        """
        try:
            os.makedirs(TemplateManager.TEMPLATES_DIR, exist_ok=True)
            
            template_path = os.path.join(
                TemplateManager.TEMPLATES_DIR,
                f"{template_name}.tex"
            )
            
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"Template created: {template_name}")
            return True
        except Exception as e:
            logger.error(f"Error creating template: {str(e)}")
            return False
