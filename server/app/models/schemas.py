from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


class FormatOptions(BaseModel):
    """Options for APA formatting"""
    fix_title_page: bool = True
    fix_headings: bool = True
    fix_citations: bool = True
    fix_references: bool = True
    fix_spacing: bool = True
    use_ai_enhancement: bool = False


class CitationType(str, Enum):
    PARENTHETICAL = "parenthetical"
    NARRATIVE = "narrative"
    BLOCK_QUOTE = "block_quote"


class Citation(BaseModel):
    """Represents a detected citation"""
    original_text: str
    formatted_text: str
    citation_type: CitationType
    authors: List[str]
    year: Optional[str] = None
    page: Optional[str] = None


class Reference(BaseModel):
    """Represents a reference entry"""
    original_text: str
    formatted_text: str
    authors: List[str]
    year: Optional[str] = None
    title: Optional[str] = None
    source: Optional[str] = None
    url: Optional[str] = None
    doi: Optional[str] = None


class HeadingLevel(int, Enum):
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3
    LEVEL_4 = 4
    LEVEL_5 = 5


class DocumentSection(BaseModel):
    """Represents a section of the document"""
    heading: Optional[str] = None
    heading_level: Optional[HeadingLevel] = None
    content: str
    citations: List[Citation] = []


class FormattingIssue(BaseModel):
    """Represents a formatting issue found"""
    issue_type: str
    description: str
    location: Optional[str] = None
    suggestion: str


class FormatResponse(BaseModel):
    """Response from the formatting endpoint"""
    success: bool
    message: str
    issues_found: List[FormattingIssue] = []
    issues_fixed: int = 0
    download_url: Optional[str] = None


class DocumentMetadata(BaseModel):
    """Metadata extracted from the document"""
    title: Optional[str] = None
    authors: List[str] = []
    institution: Optional[str] = None
    course: Optional[str] = None
    instructor: Optional[str] = None
    date: Optional[str] = None
    word_count: int = 0
    page_count: int = 0
