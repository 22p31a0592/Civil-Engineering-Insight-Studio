"""
NLP Analyzer Service - Advanced Natural Language Processing
Uses spaCy and Transformers for intelligent text generation
"""
import spacy
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Tuple
import numpy as np
from collections import defaultdict


class NLPAnalyzer:
    """Advanced NLP analyzer for generating technical descriptions"""
    
    def __init__(self, spacy_model: str = 'en_core_web_sm'):
        """Initialize NLP models"""
        try:
            self.nlp = spacy.load(spacy_model)
        except OSError:
            print(f"Downloading spaCy model {spacy_model}...")
            import subprocess
            subprocess.run(['python', '-m', 'spacy', 'download', spacy_model])
            self.nlp = spacy.load(spacy_model)
        
        # Load sentence transformer for semantic similarity
        self.sentence_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        
        # Technical vocabulary
        self.technical_terms = self._load_technical_vocabulary()
        
        # Description templates
        self.templates = self._load_description_templates()
    
    def _load_technical_vocabulary(self) -> Dict[str, List[str]]:
        """Load civil engineering technical vocabulary"""
        return {
            'materials': [
                'reinforced concrete', 'structural steel', 'high-strength concrete',
                'prestressed concrete', 'composite materials', 'masonry', 'timber',
                'aluminum alloys', 'glass fiber reinforced polymer'
            ],
            'components': [
                'load-bearing structure', 'cantilever beam', 'truss system',
                'foundation system', 'structural frame', 'shear wall', 'column assembly',
                'deck system', 'arch structure', 'cable-stayed system'
            ],
            'properties': [
                'tensile strength', 'compressive strength', 'shear capacity',
                'bending moment', 'load distribution', 'structural integrity',
                'seismic resistance', 'durability', 'corrosion resistance'
            ],
            'methods': [
                'cast-in-place construction', 'precast assembly', 'welded connections',
                'bolted joints', 'post-tensioning', 'formwork system', 'reinforcement placement'
            ],
            'conditions': [
                'excellent structural condition', 'minor surface deterioration',
                'moderate weathering', 'requires maintenance', 'newly constructed',
                'undergoing renovation', 'structurally sound'
            ]
        }
    
    def _load_description_templates(self) -> Dict[str, List[str]]:
        """Load templates for generating descriptions"""
        return {
            'material_identification': [
                "The structure exhibits extensive use of {material}, identifiable by its {characteristics}.",
                "Analysis reveals {material} as the primary construction material, featuring {properties}.",
                "{material} comprises approximately {percentage}% of the visible structure, located in {location}."
            ],
            'structural_component': [
                "The {component} demonstrates {construction_method} construction, measuring approximately {dimensions}.",
                "A {component} constructed from {material} serves as a critical load-bearing element.",
                "The structural system includes a {component} featuring {notable_features}."
            ],
            'construction_progress': [
                "Construction progress indicates completion of {phase} phase at approximately {percentage}%.",
                "The project has successfully completed {completed_elements}, with {planned_elements} remaining.",
                "Current construction phase shows {materials} being installed using {methods}."
            ],
            'structural_analysis': [
                "Structural assessment reveals a {structure_type} configuration with {components}.",
                "The load-bearing system consists of {primary_elements} designed for {purpose}.",
                "Engineering analysis indicates {condition} with {characteristics}."
            ]
        }
    
    def generate_material_description(self, material: Dict) -> str:
        """Generate detailed material description using NLP"""
        material_name = material.get('name', 'unknown material')
        confidence = material.get('confidence', 0.0)
        properties = material.get('properties', {})
        
        # Create base description
        parts = []
        
        # Material identification
        confidence_level = "high" if confidence > 0.8 else "moderate" if confidence > 0.6 else "possible"
        parts.append(f"Identified with {confidence_level} confidence as {material_name}")
        
        # Properties
        if properties:
            prop_strs = [f"{k.replace('_', ' ')}: {v}" for k, v in properties.items()]
            parts.append(f"exhibiting {', '.join(prop_strs)}")
        
        # Location and quantity
        if material.get('location'):
            parts.append(f"located in {material['location']}")
        
        if material.get('quantity'):
            parts.append(f"with {material['quantity']} observed")
        
        # Texture information
        if material.get('texture'):
            parts.append(f"displaying {material['texture']} texture")
        
        description = ". ".join([p.capitalize() for p in parts]) + "."
        
        return description
    
    def generate_component_description(self, component: Dict) -> str:
        """Generate detailed structural component description"""
        comp_type = component.get('component_type', 'structural element')
        material = component.get('material', 'unspecified material')
        dimensions = component.get('dimensions', {})
        construction_method = component.get('construction_method', 'standard construction')
        
        parts = []
        
        # Component introduction
        parts.append(f"A {comp_type} constructed from {material}")
        
        # Dimensions
        if dimensions:
            dim_parts = []
            for key, value in dimensions.items():
                dim_parts.append(f"{key}: {value}m")
            parts.append(f"with dimensions of {', '.join(dim_parts)}")
        
        # Construction method
        parts.append(f"utilizing {construction_method}")
        
        # Notable features
        if component.get('notable_features'):
            features = component['notable_features']
            if len(features) > 0:
                parts.append(f"Notable features include: {', '.join(features)}")
        
        # Condition
        if component.get('condition'):
            parts.append(f"The component is in {component['condition']} condition")
        
        description = ". ".join(parts) + "."
        
        return description
    
    def generate_progress_description(self, progress: Dict) -> str:
        """Generate project progress description"""
        phase = progress.get('phase', 'construction')
        completion = progress.get('completion_percentage', 0)
        
        parts = []
        
        # Phase and completion
        parts.append(f"The project is currently in the {phase} phase")
        parts.append(f"with an estimated {completion:.1f}% completion rate")
        
        # Completed elements
        if progress.get('completed_elements'):
            completed = progress['completed_elements']
            parts.append(f"Completed work includes: {', '.join(completed)}")
        
        # Planned elements
        if progress.get('planned_elements'):
            planned = progress['planned_elements']
            parts.append(f"Upcoming work involves: {', '.join(planned)}")
        
        # Materials and methods
        if progress.get('construction_methods'):
            methods = progress['construction_methods']
            parts.append(f"Construction methods employed: {', '.join(methods)}")
        
        # Challenges
        if progress.get('challenges'):
            challenges = progress['challenges']
            parts.append(f"Identified challenges: {', '.join(challenges)}")
        
        description = ". ".join(parts) + "."
        
        return description
    
    def generate_comprehensive_summary(self, analysis_data: Dict) -> str:
        """Generate comprehensive analysis summary"""
        sections = []
        
        # Overview
        analysis_type = analysis_data.get('analysis_type', 'General')
        sections.append(f"=== {analysis_type} Analysis Summary ===\n")
        
        # Materials summary
        if analysis_data.get('materials'):
            materials = analysis_data['materials']
            sections.append(f"Material Analysis:")
            sections.append(f"Identified {len(materials)} distinct material types:")
            for mat in materials[:5]:  # Top 5 materials
                sections.append(f"  • {mat.get('name', 'Unknown')} - {mat.get('location', 'Various locations')}")
            sections.append("")
        
        # Structural components summary
        if analysis_data.get('structural_components'):
            components = analysis_data['structural_components']
            sections.append(f"Structural Components:")
            sections.append(f"Detected {len(components)} structural elements:")
            for comp in components[:5]:  # Top 5 components
                sections.append(f"  • {comp.get('component_type', 'Unknown')} - {comp.get('material', 'Unknown material')}")
            sections.append("")
        
        # Progress information
        if analysis_data.get('project_progress'):
            progress = analysis_data['project_progress']
            sections.append(f"Project Progress:")
            sections.append(f"Phase: {progress.get('phase', 'Unknown')}")
            sections.append(f"Completion: {progress.get('completion_percentage', 0):.1f}%")
            sections.append("")
        
        return "\n".join(sections)
    
    def generate_detailed_description(self, analysis_data: Dict) -> str:
        """Generate detailed technical description"""
        paragraphs = []
        
        # Introduction
        analysis_type = analysis_data.get('analysis_type', 'structural')
        paragraphs.append(
            f"This {analysis_type} analysis provides comprehensive insights into the "
            f"construction characteristics, materials composition, and structural elements "
            f"present in the examined structure."
        )
        
        # Materials section
        if analysis_data.get('materials'):
            materials = analysis_data['materials']
            material_names = [m.get('name', 'unknown') for m in materials]
            paragraphs.append(
                f"Material analysis reveals a composition primarily consisting of "
                f"{', '.join(material_names[:3])}. Each material contributes distinct "
                f"structural and aesthetic properties to the overall construction."
            )
        
        # Structural components section
        if analysis_data.get('structural_components'):
            components = analysis_data['structural_components']
            comp_types = list(set([c.get('component_type', 'element') for c in components]))
            paragraphs.append(
                f"The structural system incorporates {len(components)} identifiable components, "
                f"including {', '.join(comp_types[:3])}. These elements work in concert to "
                f"provide load-bearing capacity and structural stability."
            )
        
        # Construction methods
        if analysis_data.get('construction_methods'):
            methods = analysis_data['construction_methods']
            paragraphs.append(
                f"Construction methodology analysis indicates the use of {', '.join(methods)}. "
                f"These techniques are standard in modern civil engineering practice and "
                f"ensure structural integrity and longevity."
            )
        
        return "\n\n".join(paragraphs)
    
    def generate_recommendations(self, analysis_data: Dict) -> List[str]:
        """Generate engineering recommendations based on analysis"""
        recommendations = []
        
        # Check confidence levels
        avg_confidence = 0
        count = 0
        
        if analysis_data.get('materials'):
            for mat in analysis_data['materials']:
                avg_confidence += mat.get('confidence', 0)
                count += 1
        
        if count > 0:
            avg_confidence /= count
            if avg_confidence < 0.7:
                recommendations.append(
                    "Consider performing additional material testing for more accurate "
                    "identification and characterization."
                )
        
        # Check for structural components
        if analysis_data.get('structural_components'):
            components = analysis_data['structural_components']
            if any(c.get('condition', '').lower() in ['poor', 'deteriorated'] for c in components):
                recommendations.append(
                    "Schedule detailed structural inspection for components showing signs "
                    "of deterioration or distress."
                )
        
        # Progress-related recommendations
        if analysis_data.get('project_progress'):
            progress = analysis_data['project_progress']
            if progress.get('challenges'):
                recommendations.append(
                    "Address identified construction challenges through engineering review "
                    "and potential design modifications."
                )
        
        # General recommendations
        recommendations.append(
            "Maintain comprehensive documentation of all construction phases and material specifications."
        )
        
        recommendations.append(
            "Ensure compliance with relevant building codes and engineering standards."
        )
        
        return recommendations
    
    def extract_technical_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract technical entities from text using NLP"""
        doc = self.nlp(text)
        
        entities = {
            'materials': [],
            'measurements': [],
            'locations': [],
            'methods': []
        }
        
        # Extract entities
        for ent in doc.ents:
            if ent.label_ in ['MATERIAL', 'SUBSTANCE']:
                entities['materials'].append(ent.text)
            elif ent.label_ in ['QUANTITY', 'CARDINAL']:
                entities['measurements'].append(ent.text)
            elif ent.label_ in ['LOC', 'GPE']:
                entities['locations'].append(ent.text)
        
        # Extract noun chunks for methods and components
        for chunk in doc.noun_chunks:
            text_lower = chunk.text.lower()
            if any(term in text_lower for term in ['construction', 'method', 'technique']):
                entities['methods'].append(chunk.text)
        
        return entities
    
    def calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two texts"""
        embeddings = self.sentence_model.encode([text1, text2])
        similarity = np.dot(embeddings[0], embeddings[1]) / (
            np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
        )
        return float(similarity)