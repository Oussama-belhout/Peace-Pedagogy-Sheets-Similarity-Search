"""
PDF Parser for Peace Pedagogy Pedagogical Sheets
Extracts metadata from PDF files and converts to ontology format
"""

import os
import re
import json
from pathlib import Path
import pdfplumber
from typing import Dict, List, Optional


class PedagogicalSheetParser:
    """
    Parses pedagogical sheets from PDF files
    Extracts metadata from filename and content
    """
    
    def __init__(self):
        # Domain mappings
        self.domain_map = {
            'SC': 'Sciences',
            'ET': 'Ethics',
            'A': 'Arts',
            'L': 'Languages'
        }
        
        # Subdomain mappings
        self.subdomain_map = {
            'EN': 'environmental_science',
            'SVT': 'life_sciences',
            'MAT': 'mathematics',
            'PC': 'physics_chemistry',
            'SCP': 'socio_emotional',
            'C': 'citizenship',
            'T': 'theater',
            'TM': 'craft',
            'PD': 'drawing',
            'EX': 'expression',
            'CO': 'communication',
            'CEC': 'reading_writing'
        }
        
        # Keywords for detecting pedagogical elements
        self.virtue_keywords = {
            'gratitude': ['gratitude', 'reconnaissance', 'remerci'], 
            'empathy': ['empathie', 'empathy', 'compassion'],
            'responsibility': ['responsabilité', 'responsibility', 'responsable'],
            'patience': ['patience', 'patient'],
            'benevolence': ['bienveillance', 'benevolence', 'bienveillant'],
            'compassion': ['compassion', 'compatissant'],
            'cooperation': ['coopération', 'cooperation', 'collabor'],
            'humility': ['humilité', 'humility', 'humble'],
            'sharing': ['partage', 'sharing', 'partager'],
            'respect': ['respect', 'respectueux']
        }
        
        self.tool_keywords = {
            'cevq': ['cevq', 'cercle', 'éveil', 'vertus', 'qualités'],
            'meditation': ['méditation', 'meditation', 'pleine conscience', 'mindfulness'],
            'project_based_learning': ['projet', 'project', 'réalisation'],
            'artistic_expression': ['artistique', 'art', 'créatif', 'expression'],
            'solution_oriented_learning': ['problème', 'solution', 'résolution']
        }
        
        self.axes_keywords = {
            'peace_with_self': ['soi', 'self', 'intérieur', 'émotions', 'emotions', 'inner'],
            'peace_with_others': ['autres', 'others', 'groupe', 'équipe', 'collaboration', 'entraide', 'partage'],
            'peace_with_environment': ['environnement', 'environment', 'nature', 'écologie', 'ecology', 'planète']
        }
    
    def extract_metadata_from_filename(self, filename: str) -> Dict:
        """
        Extract metadata from the filename pattern
        Example: "Séance - Mandala d'une assiette de riz  FR-SC-EN-6-14-4.pdf"
        """
        metadata = {}
        
        # Remove .pdf extension
        name = filename.replace('.pdf', '')
        
        # Extract title (everything before the language code pattern)
        # Pattern: FR-XX-XXX-numbers
        pattern = r'(.+?)\s+(FR|TU)-([A-Z]+)-([A-Z_]+)-(.+?)$'
        match = re.search(pattern, name)
        
        if match:
            title_part = match.group(1).strip()
            # Remove "Séance -" or "Séquence -" prefix
            title = re.sub(r'^(Séance|Séquence)\s*-?\s*', '', title_part).strip()
            metadata['title'] = title
            
            # Extract domain
            domain_code = match.group(3)
            metadata['domain'] = self.domain_map.get(domain_code, 'Unknown')
            
            # Extract subdomain/discipline
            subdomain_code = match.group(4)
            metadata['discipline'] = self.subdomain_map.get(subdomain_code, subdomain_code.lower())
            
            # Extract age range
            age_part = match.group(5)
            age_match = re.search(r'(\d+)p?-(\d+)', age_part)
            if age_match:
                metadata['target_age_min'] = int(age_match.group(1))
                metadata['target_age_max'] = int(age_match.group(2))
            else:
                # Try single age with 'p' (e.g., "8p" means 8+)
                single_age = re.search(r'(\d+)p', age_part)
                if single_age:
                    age = int(single_age.group(1))
                    metadata['target_age_min'] = age
                    metadata['target_age_max'] = age + 6  # Assume 6 year range
        else:
            # Fallback: use full filename as title
            metadata['title'] = re.sub(r'^(Séance|Séquence)\s*-?\s*', '', name).strip()
        
        return metadata
    
    def extract_content_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text content from PDF
        """
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                # Read first 3 pages (usually contain the main info)
                for page in pdf.pages[:3]:
                    text += page.extract_text() or ""
                return text.lower()
        except Exception as e:
            print(f"Error reading {pdf_path}: {e}")
            return ""
    
    def detect_virtues(self, text: str) -> List[str]:
        """
        Detect virtues mentioned in the text
        """
        virtues = []
        for virtue, keywords in self.virtue_keywords.items():
            if any(keyword in text for keyword in keywords):
                virtues.append(virtue)
        return virtues 
    
    def detect_tools(self, text: str) -> List[str]:
        """
        Detect pedagogical tools mentioned in the text
        """
        tools = []
        for tool, keywords in self.tool_keywords.items():
            if any(keyword in text for keyword in keywords):
                tools.append(tool)
        return tools
    
    def detect_axes(self, text: str, title: str) -> List[str]:
        """
        Detect peace axes based on content and title
        """
        axes = []
        combined_text = (title + " " + text).lower()
        
        for axis, keywords in self.axes_keywords.items():
            if any(keyword in combined_text for keyword in keywords):
                axes.append(axis)
        
        # If no axes detected, default based on domain
        if not axes:
            axes = ['peace_with_others']  # Default
        
        return axes
    
    def estimate_duration(self, text: str) -> float:
        """
        Estimate lesson duration from content
        Look for patterns like "durée", "duration", time mentions
        """
        # Look for explicit duration
        duration_match = re.search(r'(?:durée|duration)[:\s]*(\d+)[:\s]*(?:h|heures?|hours?)', text)
        if duration_match:
            return float(duration_match.group(1))
        
        # Look for session length
        session_match = re.search(r'(\d+)[:\s]*(?:minutes|min)', text)
        if session_match:
            minutes = int(session_match.group(1))
            return minutes / 60.0
        
        # Default estimates based on content length
        if len(text) > 5000:
            return 3.0
        elif len(text) > 3000:
            return 2.0
        else:
            return 1.5
    
    def parse_pdf(self, pdf_path: str) -> Dict:
        """
        Parse a single PDF file and extract all metadata
        """
        filename = os.path.basename(pdf_path)
        
        # Extract from filename
        metadata = self.extract_metadata_from_filename(filename)
        
        # Extract from PDF content
        content = self.extract_content_from_pdf(pdf_path)
        
        # Create lesson ID from title
        lesson_id = re.sub(r'[^a-z0-9]+', '_', metadata.get('title', filename).lower())
        lesson_id = lesson_id.strip('_')
        
        # Detect pedagogical elements
        virtues = self.detect_virtues(content)
        tools = self.detect_tools(content)
        axes = self.detect_axes(content, metadata.get('title', ''))
        
        # Build complete lesson data
        lesson_data = {
            'id': lesson_id,
            'title': metadata.get('title', 'Untitled'),
            'description': f"Lesson from {filename}",
            'domain': metadata.get('domain', 'Unknown'),
            'discipline': metadata.get('discipline', ''),
            'axes': axes,
            'tools': tools if tools else ['project_based_learning'],  # Default tool
            'virtues': virtues if virtues else ['responsibility'],  # Default virtue
            'strategies': ['experiential_learning'],  # Default strategy
            'objectives': [],
            'target_age_min': metadata.get('target_age_min', 6),
            'target_age_max': metadata.get('target_age_max', 14),
            'duration': self.estimate_duration(content),
            'group_size_min': 15,
            'group_size_max': 30,
            'pdf_path': pdf_path
        }
        
        return lesson_data
    
    def parse_directory(self, directory_path: str) -> List[Dict]:
        """
        Parse all PDF files in a directory and subdirectories
        """
        lessons = []
        directory = Path(directory_path)
        
        # Find all PDF files
        pdf_files = list(directory.rglob('*.pdf'))
        
        print(f"Found {len(pdf_files)} PDF files")
        
        for pdf_file in pdf_files:
            print(f"Parsing: {pdf_file.name}")
            try:
                lesson_data = self.parse_pdf(str(pdf_file))
                lessons.append(lesson_data)
            except Exception as e:
                print(f"Error parsing {pdf_file.name}: {e}")
        
        return lessons
    
    def save_to_json(self, lessons: List[Dict], output_path: str):
        """
        Save parsed lessons to JSON file
        """
        data = {'lessons': lessons}
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(lessons)} lessons to {output_path}")


def main():
    """
    Parse all pedagogical sheets and create JSON data
    """
    print("="*80)
    print("PEDAGOGICAL SHEET PARSER")
    print("="*80)
    
    parser = PedagogicalSheetParser()
    
    # Parse all PDFs in FICHES PEDAGOGIQUES
    print("\nParsing PDF files...")
    lessons = parser.parse_directory("FICHES PEDAGOGIQUES")
    
    print(f"\n{'='*80}")
    print(f"PARSED {len(lessons)} LESSONS")
    print(f"{'='*80}\n")
    
    # Display summary
    domains = {}
    for lesson in lessons:
        domain = lesson['domain']
        domains[domain] = domains.get(domain, 0) + 1
    
    print("Lessons by domain:")
    for domain, count in domains.items():
        print(f"  {domain}: {count} lessons")
    
    # Save to JSON
    output_path = "data/pedagogical_sheets.json"
    parser.save_to_json(lessons, output_path)
    
    print(f"\n{'='*80}")
    print("NEXT STEP: Load into ontology")
    print(f"{'='*80}")
    print(f"Run: python src/data_loader.py")
    
    return lessons


if __name__ == "__main__":
    lessons = main()

