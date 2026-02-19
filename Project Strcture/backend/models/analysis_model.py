"""
Data models for Civil Engineering Analysis
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
import json


@dataclass
class Material:
    """Material identification model"""
    name: str
    confidence: float
    quantity: str
    location: str
    properties: Dict[str, str] = field(default_factory=dict)
    color_info: Optional[str] = None
    texture: Optional[str] = None

    def to_dict(self):
        return {
            'name': self.name,
            'confidence': self.confidence,
            'quantity': self.quantity,
            'location': self.location,
            'properties': self.properties,
            'color_info': self.color_info,
            'texture': self.texture
        }


@dataclass
class StructuralComponent:
    """Structural component model"""
    component_type: str
    material: str
    dimensions: Dict[str, float]
    location: str
    construction_method: str
    condition: str
    confidence: float
    notable_features: List[str] = field(default_factory=list)

    def to_dict(self):
        return {
            'component_type': self.component_type,
            'material': self.material,
            'dimensions': self.dimensions,
            'location': self.location,
            'construction_method': self.construction_method,
            'condition': self.condition,
            'confidence': self.confidence,
            'notable_features': self.notable_features
        }


@dataclass
class ProjectProgress:
    """Project progress documentation model"""
    phase: str
    completion_percentage: float
    completed_elements: List[str]
    planned_elements: List[str]
    materials_used: List[Material]
    construction_methods: List[str]
    timeline: Optional[str] = None
    challenges: List[str] = field(default_factory=list)

    def to_dict(self):
        return {
            'phase': self.phase,
            'completion_percentage': self.completion_percentage,
            'completed_elements': self.completed_elements,
            'planned_elements': self.planned_elements,
            'materials_used': [m.to_dict() for m in self.materials_used],
            'construction_methods': self.construction_methods,
            'timeline': self.timeline,
            'challenges': self.challenges
        }


@dataclass
class AnalysisResult:
    """Complete analysis result model"""
    analysis_type: str
    timestamp: str
    image_info: Dict[str, any]
    materials: List[Material] = field(default_factory=list)
    structural_components: List[StructuralComponent] = field(default_factory=list)
    project_progress: Optional[ProjectProgress] = None
    summary: str = ""
    detailed_description: str = ""
    recommendations: List[str] = field(default_factory=list)
    confidence_score: float = 0.0

    def to_dict(self):
        result = {
            'analysis_type': self.analysis_type,
            'timestamp': self.timestamp,
            'image_info': self.image_info,
            'summary': self.summary,
            'detailed_description': self.detailed_description,
            'recommendations': self.recommendations,
            'confidence_score': self.confidence_score
        }
        
        if self.materials:
            result['materials'] = [m.to_dict() for m in self.materials]
        
        if self.structural_components:
            result['structural_components'] = [c.to_dict() for c in self.structural_components]
        
        if self.project_progress:
            result['project_progress'] = self.project_progress.to_dict()
        
        return result

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)


class AnalysisResultBuilder:
    """Builder pattern for constructing analysis results"""
    
    def __init__(self, analysis_type: str):
        self.result = AnalysisResult(
            analysis_type=analysis_type,
            timestamp=datetime.now().isoformat(),
            image_info={}
        )
    
    def set_image_info(self, width: int, height: int, format: str, filename: str):
        self.result.image_info = {
            'width': width,
            'height': height,
            'format': format,
            'filename': filename
        }
        return self
    
    def add_material(self, material: Material):
        self.result.materials.append(material)
        return self
    
    def add_structural_component(self, component: StructuralComponent):
        self.result.structural_components.append(component)
        return self
    
    def set_project_progress(self, progress: ProjectProgress):
        self.result.project_progress = progress
        return self
    
    def set_summary(self, summary: str):
        self.result.summary = summary
        return self
    
    def set_detailed_description(self, description: str):
        self.result.detailed_description = description
        return self
    
    def add_recommendation(self, recommendation: str):
        self.result.recommendations.append(recommendation)
        return self
    
    def set_confidence_score(self, score: float):
        self.result.confidence_score = score
        return self
    
    def build(self) -> AnalysisResult:
        return self.result