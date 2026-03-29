"""
Reference Builder Service
Parses and formats reference lists according to APA 7th edition
"""

import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class ParsedReference:
    """Represents a parsed reference entry"""
    original: str
    authors: List[str]
    year: Optional[str]
    title: Optional[str]
    source: Optional[str]
    volume: Optional[str]
    issue: Optional[str]
    pages: Optional[str]
    doi: Optional[str]
    url: Optional[str]
    ref_type: str  # journal, book, website, etc.


class ReferenceBuilder:
    """Service for building and formatting APA 7th edition references"""
    
    def __init__(self):
        self.references = []
        self.issues = []
    
    def parse_reference(self, text: str) -> ParsedReference:
        """Parse a reference string into components"""
        # Try to detect reference type and parse accordingly
        text = text.strip()
        
        # Initialize with defaults
        parsed = ParsedReference(
            original=text,
            authors=[],
            year=None,
            title=None,
            source=None,
            volume=None,
            issue=None,
            pages=None,
            doi=None,
            url=None,
            ref_type='unknown'
        )
        
        # Extract DOI if present
        doi_match = re.search(r'https?://doi\.org/[\w./\-]+|doi:\s*[\w./\-]+', text, re.IGNORECASE)
        if doi_match:
            parsed.doi = doi_match.group()
            if not parsed.doi.startswith('http'):
                parsed.doi = 'https://doi.org/' + parsed.doi.replace('doi:', '').strip()
        
        # Extract URL if present (and not DOI)
        url_match = re.search(r'https?://(?!doi\.org)[^\s]+', text)
        if url_match:
            parsed.url = url_match.group().rstrip('.,')
        
        # Extract year
        year_match = re.search(r'\((\d{4}[a-z]?)\)', text)
        if year_match:
            parsed.year = year_match.group(1)
        
        # Extract authors (text before year)
        if year_match:
            authors_text = text[:year_match.start()].strip()
            parsed.authors = self._parse_authors(authors_text)
        
        # Try to determine type and extract remaining fields
        if 'Retrieved from' in text or parsed.url:
            parsed.ref_type = 'website'
            self._parse_website(parsed, text)
        elif re.search(r'\d+\(\d+\)', text):  # Volume(Issue) pattern
            parsed.ref_type = 'journal'
            self._parse_journal(parsed, text)
        else:
            parsed.ref_type = 'book'
            self._parse_book(parsed, text)
        
        return parsed
    
    def _parse_authors(self, text: str) -> List[str]:
        """Parse author names from text"""
        # Remove trailing punctuation
        text = text.rstrip('.,')
        
        # Split by common separators
        # Handle "Author, A. A., & Author, B. B." format
        authors = []
        
        # Split by '&' or 'and'
        parts = re.split(r'\s*[&]\s*|\s+and\s+', text)
        
        for part in parts:
            part = part.strip()
            if part:
                # Handle comma-separated multiple authors
                sub_parts = part.split(',')
                if len(sub_parts) >= 2:
                    # "LastName, F. M." format
                    i = 0
                    while i < len(sub_parts):
                        if i + 1 < len(sub_parts):
                            # Check if next part looks like initials
                            next_part = sub_parts[i + 1].strip()
                            if re.match(r'^[A-Z]\.(\s*[A-Z]\.)*$', next_part):
                                authors.append(f"{sub_parts[i].strip()}, {next_part}")
                                i += 2
                                continue
                        authors.append(sub_parts[i].strip())
                        i += 1
                else:
                    authors.append(part)
        
        return [a for a in authors if a]
    
    def _parse_journal(self, parsed: ParsedReference, text: str):
        """Parse journal article reference"""
        # Extract volume and issue
        vol_match = re.search(r'(\d+)\((\d+)\)', text)
        if vol_match:
            parsed.volume = vol_match.group(1)
            parsed.issue = vol_match.group(2)
        
        # Extract pages
        pages_match = re.search(r'(\d+)\s*[-–]\s*(\d+)', text)
        if pages_match:
            parsed.pages = f"{pages_match.group(1)}-{pages_match.group(2)}"
        
        # Extract title (italicized part after year, before journal name)
        year_match = re.search(r'\(\d{4}[a-z]?\)', text)
        if year_match:
            after_year = text[year_match.end():].strip()
            # Title is typically the first sentence after year
            title_match = re.match(r'\.?\s*([^.]+?)(?:\.|$)', after_year)
            if title_match:
                parsed.title = title_match.group(1).strip()
    
    def _parse_book(self, parsed: ParsedReference, text: str):
        """Parse book reference"""
        year_match = re.search(r'\(\d{4}[a-z]?\)', text)
        if year_match:
            after_year = text[year_match.end():].strip()
            # For books, title typically ends with period followed by publisher
            parts = after_year.split('.')
            if parts:
                parsed.title = parts[0].strip()
                if len(parts) > 1:
                    parsed.source = parts[1].strip()  # Publisher
    
    def _parse_website(self, parsed: ParsedReference, text: str):
        """Parse website reference"""
        year_match = re.search(r'\(\d{4}[a-z]?\)', text)
        if year_match:
            after_year = text[year_match.end():].strip()
            # Website title before URL
            url_pos = text.find('http')
            if url_pos > 0:
                title_text = text[year_match.end():url_pos].strip()
                parsed.title = title_text.strip('., ')
    
    def format_reference(self, parsed: ParsedReference) -> str:
        """Format a parsed reference into APA 7th edition format"""
        parts = []
        
        # Authors
        if parsed.authors:
            author_str = self._format_authors(parsed.authors)
            parts.append(author_str)
        
        # Year
        if parsed.year:
            parts.append(f"({parsed.year}).")
        else:
            parts.append("(n.d.).")
        
        # Title
        if parsed.title:
            if parsed.ref_type == 'journal':
                # Article title - not italicized, sentence case
                parts.append(f"{self._to_sentence_case(parsed.title)}.")
            else:
                # Book/website title - italicized (marked with asterisks for now)
                parts.append(f"*{self._to_sentence_case(parsed.title)}*.")
        
        # Source (journal name or publisher)
        if parsed.source:
            if parsed.ref_type == 'journal':
                parts.append(f"*{parsed.source}*,")
            else:
                parts.append(parsed.source + ".")
        
        # Volume, issue, pages (for journals)
        if parsed.ref_type == 'journal':
            if parsed.volume:
                vol_str = f"*{parsed.volume}*"
                if parsed.issue:
                    vol_str += f"({parsed.issue})"
                if parsed.pages:
                    vol_str += f", {parsed.pages}"
                parts.append(vol_str + ".")
        
        # DOI or URL
        if parsed.doi:
            parts.append(parsed.doi)
        elif parsed.url:
            parts.append(parsed.url)
        
        return ' '.join(parts)
    
    def _format_authors(self, authors: List[str]) -> str:
        """Format author list according to APA rules"""
        if not authors:
            return ""
        
        if len(authors) == 1:
            return authors[0] + "."
        elif len(authors) == 2:
            return f"{authors[0]}, & {authors[1]}."
        elif len(authors) <= 20:
            return ', '.join(authors[:-1]) + f", & {authors[-1]}."
        else:
            # More than 20 authors: first 19, ..., last
            return ', '.join(authors[:19]) + f", ... {authors[-1]}."
    
    def _to_sentence_case(self, text: str) -> str:
        """Convert to sentence case (capitalize first letter only)"""
        if not text:
            return ""
        # Preserve capitalization of proper nouns (basic heuristic)
        words = text.split()
        result = []
        for i, word in enumerate(words):
            if i == 0:
                result.append(word.capitalize())
            elif word[0].isupper() and len(word) > 1 and word[1:].islower():
                # Likely a proper noun, keep it
                result.append(word)
            else:
                result.append(word.lower())
        return ' '.join(result)
    
    def sort_references(self, references: List[str]) -> List[str]:
        """Sort references alphabetically by first author's last name"""
        def sort_key(ref: str) -> str:
            # Extract first word (usually author's last name)
            match = re.match(r'([A-Za-z]+)', ref)
            return match.group(1).lower() if match else ref.lower()
        
        return sorted(references, key=sort_key)
    
    def check_reference(self, text: str) -> List[Dict]:
        """Check a reference for APA formatting issues"""
        issues = []
        parsed = self.parse_reference(text)
        
        # Check for missing year
        if not parsed.year:
            issues.append({
                'issue_type': 'missing_year',
                'description': 'Reference is missing publication year',
                'suggestion': 'Add year in parentheses after author names'
            })
        
        # Check for missing authors
        if not parsed.authors:
            issues.append({
                'issue_type': 'missing_authors',
                'description': 'Could not identify authors',
                'suggestion': 'Format authors as: LastName, F. M.'
            })
        
        # Check for DOI (should be present for journal articles)
        if parsed.ref_type == 'journal' and not parsed.doi:
            issues.append({
                'issue_type': 'missing_doi',
                'description': 'Journal article should include DOI if available',
                'suggestion': 'Add DOI as https://doi.org/xxxxx'
            })
        
        # Check URL format
        if parsed.url and not parsed.url.startswith('https://'):
            issues.append({
                'issue_type': 'url_format',
                'description': 'URLs should use https when available',
                'suggestion': 'Update URL to https if possible'
            })
        
        return issues


def format_references(references: List[str]) -> Tuple[List[str], List[Dict]]:
    """Format a list of references and return issues"""
    builder = ReferenceBuilder()
    formatted = []
    all_issues = []
    
    for ref in references:
        parsed = builder.parse_reference(ref)
        formatted_ref = builder.format_reference(parsed)
        formatted.append(formatted_ref)
        
        issues = builder.check_reference(ref)
        for issue in issues:
            issue['reference'] = ref
            all_issues.append(issue)
    
    # Sort alphabetically
    formatted = builder.sort_references(formatted)
    
    return formatted, all_issues
