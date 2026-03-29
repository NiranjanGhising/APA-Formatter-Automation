"""
Citation Fixer Service
Detects and reformats in-text citations to APA 7th edition format
"""

import re
from typing import List, Dict, Tuple, Optional


class CitationFixer:
    """Service for fixing in-text citations to APA 7th edition format"""
    
    # Regex patterns for citation detection
    PATTERNS = {
        # (Author, Year) - basic parenthetical
        'paren_basic': r'\(([A-Z][a-z]+),?\s*(\d{4})\)',
        
        # (Author, Year, p. X) - with page number
        'paren_page': r'\(([A-Z][a-z]+),?\s*(\d{4}),?\s*p+\.?\s*(\d+(?:-\d+)?)\)',
        
        # (Author & Author, Year) - two authors
        'paren_two': r'\(([A-Z][a-z]+)\s*(?:&|and)\s*([A-Z][a-z]+),?\s*(\d{4})\)',
        
        # (Author et al., Year) - three or more authors
        'paren_etal': r'\(([A-Z][a-z]+)\s*et\s*al\.?,?\s*(\d{4})\)',
        
        # Author (Year) - narrative
        'narrative_basic': r'([A-Z][a-z]+)\s*\((\d{4})\)',
        
        # Author and Author (Year) - narrative two authors
        'narrative_two': r'([A-Z][a-z]+)\s*(?:&|and)\s*([A-Z][a-z]+)\s*\((\d{4})\)',
        
        # Author et al. (Year) - narrative multiple authors
        'narrative_etal': r'([A-Z][a-z]+)\s*et\s*al\.?\s*\((\d{4})\)',
    }
    
    def __init__(self, text: str):
        self.text = text
        self.citations_found = []
        self.citations_fixed = []
    
    def find_citations(self) -> List[Dict]:
        """Find all citations in the text"""
        citations = []
        
        for pattern_name, pattern in self.PATTERNS.items():
            for match in re.finditer(pattern, self.text):
                citation = {
                    'original': match.group(),
                    'type': pattern_name,
                    'start': match.start(),
                    'end': match.end(),
                    'groups': match.groups()
                }
                citations.append(citation)
        
        # Remove duplicates (overlapping matches)
        citations = self._remove_overlapping(citations)
        self.citations_found = citations
        return citations
    
    def _remove_overlapping(self, citations: List[Dict]) -> List[Dict]:
        """Remove overlapping citation matches, keeping the longest"""
        if not citations:
            return []
        
        # Sort by start position
        sorted_citations = sorted(citations, key=lambda x: x['start'])
        result = [sorted_citations[0]]
        
        for citation in sorted_citations[1:]:
            last = result[-1]
            # Check for overlap
            if citation['start'] < last['end']:
                # Keep the longer one
                if citation['end'] - citation['start'] > last['end'] - last['start']:
                    result[-1] = citation
            else:
                result.append(citation)
        
        return result
    
    def fix_citation(self, citation: Dict) -> str:
        """Fix a single citation to proper APA format"""
        ctype = citation['type']
        groups = citation['groups']
        
        if ctype == 'paren_basic':
            # (Author, Year) - ensure comma and proper spacing
            author, year = groups
            return f"({author}, {year})"
        
        elif ctype == 'paren_page':
            # (Author, Year, p. X)
            author, year, page = groups
            if '-' in page:
                return f"({author}, {year}, pp. {page})"
            return f"({author}, {year}, p. {page})"
        
        elif ctype == 'paren_two':
            # (Author & Author, Year)
            author1, author2, year = groups
            return f"({author1} & {author2}, {year})"
        
        elif ctype == 'paren_etal':
            # (Author et al., Year)
            author, year = groups
            return f"({author} et al., {year})"
        
        elif ctype == 'narrative_basic':
            # Author (Year)
            author, year = groups
            return f"{author} ({year})"
        
        elif ctype == 'narrative_two':
            # Author and Author (Year)
            author1, author2, year = groups
            return f"{author1} and {author2} ({year})"
        
        elif ctype == 'narrative_etal':
            # Author et al. (Year)
            author, year = groups
            return f"{author} et al. ({year})"
        
        return citation['original']
    
    def fix_all_citations(self) -> Tuple[str, List[Dict]]:
        """Fix all citations in the text and return corrected text"""
        if not self.citations_found:
            self.find_citations()
        
        # Sort by position (reverse to maintain positions while replacing)
        sorted_citations = sorted(self.citations_found, 
                                 key=lambda x: x['start'], 
                                 reverse=True)
        
        fixed_text = self.text
        
        for citation in sorted_citations:
            fixed = self.fix_citation(citation)
            if fixed != citation['original']:
                self.citations_fixed.append({
                    'original': citation['original'],
                    'fixed': fixed,
                    'position': citation['start']
                })
            fixed_text = (fixed_text[:citation['start']] + 
                         fixed + 
                         fixed_text[citation['end']:])
        
        return fixed_text, self.citations_fixed
    
    def identify_issues(self) -> List[Dict]:
        """Identify citation formatting issues"""
        issues = []
        
        if not self.citations_found:
            self.find_citations()
        
        for citation in self.citations_found:
            original = citation['original']
            fixed = self.fix_citation(citation)
            
            if original != fixed:
                issues.append({
                    'issue_type': 'citation_format',
                    'description': f'Citation needs reformatting',
                    'original': original,
                    'suggestion': fixed,
                    'location': citation['start']
                })
        
        return issues
    
    def detect_potential_citations(self) -> List[Dict]:
        """Detect text that might be citations but aren't properly formatted"""
        potential = []
        
        # Look for year in parentheses without author
        year_only = re.finditer(r'\((\d{4})\)', self.text)
        for match in year_only:
            potential.append({
                'text': match.group(),
                'type': 'year_only',
                'position': match.start(),
                'suggestion': 'Add author name before year: (Author, YEAR)'
            })
        
        # Look for "according to X" without citation
        according_to = re.finditer(r'according to ([A-Z][a-z]+)(?!\s*\(\d{4}\))', 
                                   self.text, re.IGNORECASE)
        for match in according_to:
            potential.append({
                'text': match.group(),
                'type': 'missing_year',
                'position': match.start(),
                'suggestion': f'Add year: {match.group(1)} (YEAR)'
            })
        
        return potential


def fix_citations_in_text(text: str) -> Tuple[str, List[Dict]]:
    """Convenience function to fix all citations in text"""
    fixer = CitationFixer(text)
    return fixer.fix_all_citations()


def analyze_citations(text: str) -> Dict:
    """Analyze citations in text and return report"""
    fixer = CitationFixer(text)
    citations = fixer.find_citations()
    issues = fixer.identify_issues()
    potential = fixer.detect_potential_citations()
    
    return {
        'citations_found': len(citations),
        'citations': citations,
        'issues': issues,
        'potential_citations': potential
    }
