"""
Text Processing Utilities for NLP-based Analysis
"""
import re
from typing import List, Dict, Set
import string


class TextProcessor:
    """Handles text preprocessing and NLP utilities"""
    
    def __init__(self):
        self.stopwords = self._load_stopwords()
    
    def _load_stopwords(self) -> Set[str]:
        """Load common English stopwords"""
        return {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'will', 'with', 'this', 'these', 'those', 'which'
        }
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def tokenize(self, text: str) -> List[str]:
        """Tokenize text into words"""
        # Remove punctuation and split
        text = text.translate(str.maketrans('', '', string.punctuation))
        tokens = text.split()
        return tokens
    
    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """Remove stopwords from token list"""
        return [token for token in tokens if token.lower() not in self.stopwords]
    
    def extract_keywords(self, text: str, top_n: int = 10) -> List[str]:
        """Extract keywords from text"""
        tokens = self.tokenize(self.clean_text(text))
        tokens = self.remove_stopwords(tokens)
        
        # Count frequency
        freq = {}
        for token in tokens:
            freq[token] = freq.get(token, 0) + 1
        
        # Sort by frequency
        sorted_tokens = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        
        return [token for token, count in sorted_tokens[:top_n]]
    
    def format_description(self, sections: Dict[str, str], title: str = "") -> str:
        """Format structured description from sections"""
        lines = []
        
        if title:
            lines.append(title)
            lines.append("=" * len(title))
            lines.append("")
        
        for section_title, content in sections.items():
            lines.append(f"{section_title}:")
            lines.append(content)
            lines.append("")
        
        return "\n".join(lines)
    
    def create_bullet_list(self, items: List[str]) -> str:
        """Create formatted bullet list"""
        return "\n".join([f"• {item}" for item in items])
    
    def create_numbered_list(self, items: List[str]) -> str:
        """Create formatted numbered list"""
        return "\n".join([f"{i+1}. {item}" for i, item in enumerate(items)])
    
    def summarize_findings(self, findings: List[Dict[str, any]], 
                          key_field: str = 'name') -> str:
        """Create summary from findings"""
        if not findings:
            return "No significant findings detected."
        
        summary_parts = []
        summary_parts.append(f"Analysis identified {len(findings)} key elements:")
        
        for i, finding in enumerate(findings, 1):
            name = finding.get(key_field, f"Element {i}")
            confidence = finding.get('confidence', 0)
            summary_parts.append(f"  {i}. {name} (Confidence: {confidence:.1%})")
        
        return "\n".join(summary_parts)
    
    def generate_sentence(self, template: str, **kwargs) -> str:
        """Generate sentence from template with keyword substitution"""
        try:
            return template.format(**kwargs)
        except KeyError as e:
            return f"Error generating sentence: missing key {e}"
    
    def pluralize(self, word: str, count: int) -> str:
        """Simple pluralization"""
        if count == 1:
            return word
        
        # Simple rules
        if word.endswith('y'):
            return word[:-1] + 'ies'
        elif word.endswith(('s', 'x', 'z', 'ch', 'sh')):
            return word + 'es'
        else:
            return word + 's'
    
    def format_measurement(self, value: float, unit: str, precision: int = 2) -> str:
        """Format measurement with units"""
        return f"{value:.{precision}f} {unit}"
    
    def create_technical_description(self, component_type: str, properties: Dict) -> str:
        """Generate technical description for component"""
        parts = [f"This is a {component_type}"]
        
        if 'material' in properties:
            parts.append(f"constructed of {properties['material']}")
        
        if 'dimensions' in properties and isinstance(properties['dimensions'], dict):
            dim_strs = [f"{k}: {v}" for k, v in properties['dimensions'].items()]
            parts.append(f"with dimensions {', '.join(dim_strs)}")
        
        if 'condition' in properties:
            parts.append(f"in {properties['condition']} condition")
        
        description = " ".join(parts) + "."
        return description
    
    def capitalize_words(self, text: str, skip_words: Set[str] = None) -> str:
        """Capitalize words in text, skipping specified words"""
        if skip_words is None:
            skip_words = {'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at'}
        
        words = text.split()
        capitalized = []
        
        for i, word in enumerate(words):
            if i == 0 or word.lower() not in skip_words:
                capitalized.append(word.capitalize())
            else:
                capitalized.append(word.lower())
        
        return " ".join(capitalized)