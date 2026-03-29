"""
Format Router
API endpoints for document formatting
"""

import os
import uuid
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel

from ..models.schemas import FormatOptions, FormatResponse, FormattingIssue
from ..services.apa_formatter import APAFormatter, format_document
from ..services.citation_fixer import CitationFixer, analyze_citations
from ..services.reference_builder import ReferenceBuilder, format_references
from ..services.ai_enhancer import enhance_document, get_ai_enhancer


router = APIRouter(prefix="/api", tags=["format"])

# Configure upload and output directories
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)


class FormatRequest(BaseModel):
    """Request body for formatting options"""
    fix_title_page: bool = True
    fix_headings: bool = True
    fix_citations: bool = True
    fix_references: bool = True
    fix_spacing: bool = True
    use_ai_enhancement: bool = False


def cleanup_old_files():
    """Remove files older than 1 hour"""
    now = datetime.now()
    for directory in [UPLOAD_DIR, OUTPUT_DIR]:
        for file_path in directory.iterdir():
            if file_path.is_file():
                file_age = now - datetime.fromtimestamp(file_path.stat().st_mtime)
                if file_age.total_seconds() > 3600:  # 1 hour
                    file_path.unlink()


@router.post("/upload", response_model=dict)
async def upload_document(file: UploadFile = File(...)):
    """Upload a document for formatting"""
    # Validate file type
    if not file.filename.endswith('.docx'):
        raise HTTPException(
            status_code=400,
            detail="Only .docx files are supported"
        )
    
    # Check file size (10MB limit)
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds 10MB limit"
        )
    
    # Generate unique ID and save file
    file_id = str(uuid.uuid4())
    file_path = UPLOAD_DIR / f"{file_id}.docx"
    
    with open(file_path, "wb") as f:
        f.write(contents)
    
    return {
        "success": True,
        "file_id": file_id,
        "filename": file.filename,
        "size": len(contents)
    }


@router.post("/format/{file_id}", response_model=FormatResponse)
async def format_uploaded_document(
    file_id: str,
    background_tasks: BackgroundTasks,
    fix_title_page: bool = Form(True),
    fix_headings: bool = Form(True),
    fix_citations: bool = Form(True),
    fix_references: bool = Form(True),
    fix_spacing: bool = Form(True),
    generate_toc: bool = Form(True),
    use_ai_enhancement: bool = Form(False)
):
    """Format an uploaded document"""
    # Check if file exists
    input_path = UPLOAD_DIR / f"{file_id}.docx"
    if not input_path.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found. Please upload again."
        )
    
    # Prepare output path
    output_id = str(uuid.uuid4())
    output_path = OUTPUT_DIR / f"{output_id}.docx"
    
    # Build options
    options = {
        'fix_title_page': fix_title_page,
        'fix_headings': fix_headings,
        'fix_citations': fix_citations,
        'fix_references': fix_references,
        'fix_spacing': fix_spacing,
        'generate_toc': generate_toc,
        'use_ai_enhancement': use_ai_enhancement
    }
    
    try:
        # Format the document
        result = format_document(
            str(input_path),
            str(output_path),
            options
        )
        
        # Schedule cleanup
        background_tasks.add_task(cleanup_old_files)
        
        # Build response
        issues = [
            FormattingIssue(
                issue_type=issue.get('issue_type', 'unknown'),
                description=issue.get('description', ''),
                location=issue.get('location'),
                suggestion=issue.get('suggestion', '')
            )
            for issue in result.get('issues_found', [])
        ]
        
        return FormatResponse(
            success=True,
            message="Document formatted successfully",
            issues_found=issues,
            issues_fixed=result.get('issues_fixed', 0),
            download_url=f"/api/download/{output_id}"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Formatting failed: {str(e)}"
        )


@router.get("/download/{output_id}")
async def download_formatted_document(output_id: str):
    """Download the formatted document"""
    output_path = OUTPUT_DIR / f"{output_id}.docx"
    
    if not output_path.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found. It may have expired."
        )
    
    return FileResponse(
        path=str(output_path),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename="formatted_document.docx"
    )


@router.post("/analyze")
async def analyze_document(file: UploadFile = File(...)):
    """Analyze a document and return formatting issues without making changes"""
    # Validate and save file temporarily
    if not file.filename.endswith('.docx'):
        raise HTTPException(
            status_code=400,
            detail="Only .docx files are supported"
        )
    
    temp_id = str(uuid.uuid4())
    temp_path = UPLOAD_DIR / f"{temp_id}.docx"
    
    try:
        contents = await file.read()
        with open(temp_path, "wb") as f:
            f.write(contents)
        
        # Analyze the document
        from ..services.docx_parser import DocxParser
        parser = DocxParser(str(temp_path))
        
        # Get document info
        metadata = parser.get_metadata()
        paragraphs = parser.get_paragraphs()
        word_count = parser.get_word_count()
        
        # Find citations
        citation_analysis = analyze_citations(parser.get_all_text())
        
        # Find references
        ref_data = parser.find_references_section()
        ref_count = len(ref_data[1]) if ref_data else 0
        
        # Identify potential issues
        issues = []
        
        # Check for title page
        if not any(p.get('alignment') == 'CENTER' for p in paragraphs[:5]):
            issues.append({
                'type': 'missing_title_page',
                'description': 'Document may be missing a proper title page',
                'severity': 'warning'
            })
        
        # Check for references
        if not ref_data:
            issues.append({
                'type': 'missing_references',
                'description': 'No references section found',
                'severity': 'warning'
            })
        
        # Citation issues
        for issue in citation_analysis.get('issues', []):
            issues.append({
                'type': 'citation_format',
                'description': issue.get('description', ''),
                'severity': 'info'
            })
        
        return {
            'success': True,
            'metadata': metadata,
            'word_count': word_count,
            'paragraph_count': len(paragraphs),
            'citation_count': citation_analysis.get('citations_found', 0),
            'reference_count': ref_count,
            'issues': issues
        }
    
    finally:
        # Clean up temp file
        if temp_path.exists():
            temp_path.unlink()


@router.get("/ai-status")
async def get_ai_status():
    """Check if AI enhancement is available"""
    enhancer = get_ai_enhancer()
    return {
        'available': enhancer.is_available(),
        'message': 'AI enhancement is available' if enhancer.is_available() 
                   else 'Set OPENAI_API_KEY to enable AI enhancement'
    }
