"""
AI Enhancement Service
Optional AI-powered improvements using OpenAI or other LLMs
"""

import os
from typing import List, Dict, Optional
import httpx
from openai import OpenAI


class AIEnhancer:
    """Service for AI-powered document enhancement"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = None
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
    
    def is_available(self) -> bool:
        """Check if AI enhancement is available"""
        return self.client is not None
    
    async def enhance_academic_tone(self, text: str) -> str:
        """Improve the academic tone of the text"""
        if not self.is_available():
            return text
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """You are an academic writing assistant. 
                        Improve the academic tone of the text while preserving its meaning.
                        - Use formal language
                        - Avoid contractions
                        - Use passive voice where appropriate
                        - Maintain clarity and precision
                        Return only the improved text, no explanations."""
                    },
                    {"role": "user", "content": text}
                ],
                max_tokens=2000,
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"AI enhancement failed: {e}")
            return text
    
    async def suggest_citations(self, text: str) -> List[Dict]:
        """Identify claims that might need citations"""
        if not self.is_available():
            return []
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """You are an academic citation expert.
                        Analyze the text and identify statements that should have citations.
                        For each statement, explain why it needs a citation.
                        Return a JSON array of objects with 'statement' and 'reason' fields.
                        Only identify clear cases where citations are needed."""
                    },
                    {"role": "user", "content": text}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            # Parse the response
            import json
            content = response.choices[0].message.content
            try:
                suggestions = json.loads(content)
                return suggestions
            except json.JSONDecodeError:
                return []
        except Exception as e:
            print(f"Citation suggestion failed: {e}")
            return []
    
    async def fix_grammar(self, text: str) -> str:
        """Fix grammar and spelling errors"""
        if not self.is_available():
            return text
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a grammar and spelling expert.
                        Fix any grammar, spelling, or punctuation errors in the text.
                        Preserve the original meaning and style.
                        Return only the corrected text."""
                    },
                    {"role": "user", "content": text}
                ],
                max_tokens=2000,
                temperature=0.1
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Grammar fix failed: {e}")
            return text
    
    async def generate_abstract(self, text: str, max_words: int = 250) -> str:
        """Generate an abstract for the document"""
        if not self.is_available():
            return ""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"""You are an academic writing expert.
                        Generate a concise abstract for the following academic document.
                        The abstract should:
                        - Be between 150-{max_words} words
                        - Summarize the purpose, method, results, and conclusions
                        - Be written in a single paragraph
                        - Not include citations or references
                        Return only the abstract text."""
                    },
                    {"role": "user", "content": text[:10000]}  # Limit input
                ],
                max_tokens=500,
                temperature=0.5
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Abstract generation failed: {e}")
            return ""
    
    async def analyze_structure(self, paragraphs: List[str]) -> List[Dict]:
        """Analyze document structure and suggest improvements"""
        if not self.is_available():
            return []
        
        try:
            text = "\n\n".join(paragraphs[:20])  # First 20 paragraphs
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """You are an academic document structure expert.
                        Analyze the document structure and identify issues:
                        - Missing sections (introduction, methods, results, discussion, conclusion)
                        - Unclear headings
                        - Logical flow problems
                        - Paragraph organization issues
                        Return a JSON array of objects with 'issue', 'location', and 'suggestion' fields."""
                    },
                    {"role": "user", "content": text}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            import json
            content = response.choices[0].message.content
            try:
                suggestions = json.loads(content)
                return suggestions
            except json.JSONDecodeError:
                return []
        except Exception as e:
            print(f"Structure analysis failed: {e}")
            return []


# Singleton instance
_enhancer = None

def get_ai_enhancer() -> AIEnhancer:
    """Get or create the AI enhancer singleton"""
    global _enhancer
    if _enhancer is None:
        _enhancer = AIEnhancer()
    return _enhancer


async def enhance_document(text: str, options: Dict) -> Dict:
    """Main function to enhance a document with AI"""
    enhancer = get_ai_enhancer()
    
    if not enhancer.is_available():
        return {
            'success': False,
            'message': 'AI enhancement not available. Set OPENAI_API_KEY environment variable.',
            'text': text
        }
    
    result = {
        'success': True,
        'message': 'AI enhancement completed',
        'text': text,
        'suggestions': []
    }
    
    if options.get('improve_tone', False):
        result['text'] = await enhancer.enhance_academic_tone(result['text'])
    
    if options.get('fix_grammar', False):
        result['text'] = await enhancer.fix_grammar(result['text'])
    
    if options.get('suggest_citations', False):
        result['suggestions'] = await enhancer.suggest_citations(text)
    
    return result
