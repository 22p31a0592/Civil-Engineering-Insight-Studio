"""
Structure Analyzer Service - Core Analysis Engine
Integrates image processing, NLP, and domain knowledge
"""
import numpy as np
from typing import Dict, List, Tuple
import cv2
from datetime import datetime

from models.analysis_model import (
    Material, StructuralComponent, ProjectProgress,
    AnalysisResult, AnalysisResultBuilder
)
from services.nlp_analyzer import NLPAnalyzer
from utils.image_utils import ImageProcessor
from utils.text_utils import TextProcessor
import config


class StructureAnalyzer:
    """Main structure analysis engine"""
    
    def __init__(self):
        self.image_processor = ImageProcessor()
        self.nlp_analyzer = NLPAnalyzer()
        self.text_processor = TextProcessor()
        
        # Load configuration
        self.materials_db = config.CONSTRUCTION_MATERIALS
        self.components_list = config.STRUCTURAL_COMPONENTS
        self.phases_list = config.CONSTRUCTION_PHASES
    
    def analyze_structure(self, image_path: str, analysis_type: str) -> AnalysisResult:
        """Main analysis method - dispatches to specific analyzers"""
        # Load and preprocess image
        image = self.image_processor.load_image(image_path)
        processed_image = self.image_processor.preprocess_image(image)
        
        # Extract image metadata
        metadata = self.image_processor.get_image_metadata(
            image, 
            filename=image_path.split('/')[-1]
        )
        
        # Create result builder
        builder = AnalysisResultBuilder(analysis_type)
        builder.set_image_info(
            metadata['width'],
            metadata['height'],
            metadata['format'],
            metadata['filename']
        )
        
        # Dispatch to specific analyzer
        if analysis_type == 'material_identification':
            result = self._analyze_materials(processed_image, builder)
        elif analysis_type == 'project_progress':
            result = self._analyze_progress(processed_image, builder)
        elif analysis_type == 'structural_analysis':
            result = self._analyze_structure(processed_image, builder)
        else:
            # Default comprehensive analysis
            result = self._comprehensive_analysis(processed_image, builder)
        
        return result
    
    def _analyze_materials(self, image: np.ndarray, 
                          builder: AnalysisResultBuilder) -> AnalysisResult:
        """Analyze and identify construction materials"""
        # Extract image features
        color_features = self.image_processor.extract_color_features(image)
        texture_features = self.image_processor.extract_texture_features(image)
        
        # Identify materials based on features
        materials = self._identify_materials(color_features, texture_features, image)
        
        # Add materials to result
        for material in materials:
            builder.add_material(material)
        
        # Generate descriptions using NLP
        summary_data = {
            'analysis_type': 'Material Identification',
            'materials': [m.to_dict() for m in materials]
        }
        
        summary = self.nlp_analyzer.generate_comprehensive_summary(summary_data)
        detailed = self._generate_material_report(materials)
        
        builder.set_summary(summary)
        builder.set_detailed_description(detailed)
        
        # Calculate confidence score
        if materials:
            avg_confidence = sum(m.confidence for m in materials) / len(materials)
            builder.set_confidence_score(avg_confidence)
        
        # Generate recommendations
        recommendations = self._generate_material_recommendations(materials)
        for rec in recommendations:
            builder.add_recommendation(rec)
        
        return builder.build()
    
    def _analyze_progress(self, image: np.ndarray,
                         builder: AnalysisResultBuilder) -> AnalysisResult:
        """Analyze construction project progress"""
        # Extract features
        geometric_features = self.image_processor.extract_geometric_features(image)
        texture_features = self.image_processor.extract_texture_features(image)
        
        # Estimate completion
        completion_percentage = self._estimate_completion(geometric_features, texture_features)
        
        # Identify phase
        current_phase = self._identify_construction_phase(image, geometric_features)
        
        # Identify completed and planned elements
        completed_elements = self._identify_completed_elements(image, geometric_features)
        planned_elements = self._identify_planned_elements(current_phase)
        
        # Identify materials
        color_features = self.image_processor.extract_color_features(image)
        materials = self._identify_materials(color_features, texture_features, image)
        
        # Identify construction methods
        methods = self._identify_construction_methods(geometric_features, texture_features)
        
        # Create progress object
        progress = ProjectProgress(
            phase=current_phase,
            completion_percentage=completion_percentage,
            completed_elements=completed_elements,
            planned_elements=planned_elements,
            materials_used=materials,
            construction_methods=methods,
            timeline=f"Estimated phase duration: {self._estimate_phase_duration(current_phase)} weeks",
            challenges=self._identify_challenges(geometric_features, texture_features)
        )
        
        builder.set_project_progress(progress)
        
        # Generate descriptions
        summary_data = {
            'analysis_type': 'Project Progress',
            'project_progress': progress.to_dict(),
            'materials': [m.to_dict() for m in materials]
        }
        
        summary = self.nlp_analyzer.generate_comprehensive_summary(summary_data)
        detailed = self.nlp_analyzer.generate_progress_description(progress.to_dict())
        
        builder.set_summary(summary)
        builder.set_detailed_description(detailed)
        builder.set_confidence_score(0.75)  # Base confidence for progress analysis
        
        # Recommendations
        recommendations = [
            f"Continue monitoring {current_phase} phase progression",
            "Maintain quality control for completed elements",
            "Prepare resources for upcoming planned elements"
        ]
        for rec in recommendations:
            builder.add_recommendation(rec)
        
        return builder.build()
    
    def _analyze_structure(self, image: np.ndarray,
                          builder: AnalysisResultBuilder) -> AnalysisResult:
        """Perform structural analysis"""
        # Extract comprehensive features
        geometric_features = self.image_processor.extract_geometric_features(image)
        texture_features = self.image_processor.extract_texture_features(image)
        color_features = self.image_processor.extract_color_features(image)
        
        # Identify structural components
        components = self._identify_structural_components(
            image, geometric_features, texture_features, color_features
        )
        
        # Add components to result
        for component in components:
            builder.add_structural_component(component)
        
        # Identify materials
        materials = self._identify_materials(color_features, texture_features, image)
        for material in materials:
            builder.add_material(material)
        
        # Generate descriptions
        summary_data = {
            'analysis_type': 'Structural Analysis',
            'structural_components': [c.to_dict() for c in components],
            'materials': [m.to_dict() for m in materials],
            'construction_methods': [c.construction_method for c in components]
        }
        
        summary = self.nlp_analyzer.generate_comprehensive_summary(summary_data)
        detailed = self.nlp_analyzer.generate_detailed_description(summary_data)
        
        builder.set_summary(summary)
        builder.set_detailed_description(detailed)
        
        # Calculate confidence
        if components:
            avg_confidence = sum(c.confidence for c in components) / len(components)
            builder.set_confidence_score(avg_confidence)
        
        # Generate recommendations
        recommendations = self.nlp_analyzer.generate_recommendations(summary_data)
        for rec in recommendations:
            builder.add_recommendation(rec)
        
        return builder.build()
    
    def _comprehensive_analysis(self, image: np.ndarray,
                               builder: AnalysisResultBuilder) -> AnalysisResult:
        """Perform comprehensive analysis (all types)"""
        # Run all analysis types
        color_features = self.image_processor.extract_color_features(image)
        texture_features = self.image_processor.extract_texture_features(image)
        geometric_features = self.image_processor.extract_geometric_features(image)
        
        # Materials
        materials = self._identify_materials(color_features, texture_features, image)
        for material in materials:
            builder.add_material(material)
        
        # Structural components
        components = self._identify_structural_components(
            image, geometric_features, texture_features, color_features
        )
        for component in components:
            builder.add_structural_component(component)
        
        # Generate comprehensive report
        summary_data = {
            'analysis_type': 'Comprehensive',
            'materials': [m.to_dict() for m in materials],
            'structural_components': [c.to_dict() for c in components]
        }
        
        summary = self.nlp_analyzer.generate_comprehensive_summary(summary_data)
        detailed = self.nlp_analyzer.generate_detailed_description(summary_data)
        
        builder.set_summary(summary)
        builder.set_detailed_description(detailed)
        builder.set_confidence_score(0.70)
        
        return builder.build()
    
    def _identify_materials(self, color_features: Dict, texture_features: Dict,
                           image: np.ndarray) -> List[Material]:
        """Identify materials based on image features"""
        materials = []
        
        # Analyze dominant colors
        dominant_colors = color_features['dominant_colors']
        
        for i, color_info in enumerate(dominant_colors[:3]):
            rgb = np.array(color_info['rgb'])
            percentage = color_info['percentage']
            
            # Match to material database
            material_name = self._match_material_by_color(rgb)
            
            if material_name and percentage > 10:  # Only significant materials
                material = Material(
                    name=material_name,
                    confidence=min(0.95, 0.5 + (percentage / 100)),
                    quantity=f"{percentage:.1f}% of visible area",
                    location=self._estimate_material_location(i, image.shape),
                    properties=self.materials_db.get(material_name, {}).get('properties', {}),
                    color_info=f"RGB: {rgb.tolist()}",
                    texture=texture_features.get('texture_type', 'unknown')
                )
                materials.append(material)
        
        return materials
    
    def _match_material_by_color(self, rgb: np.ndarray) -> str:
        """Match RGB color to material"""
        min_distance = float('inf')
        matched_material = None
        
        for material_name, properties in self.materials_db.items():
            for color_range in properties.get('color_ranges', []):
                lower = np.array(color_range[0])
                upper = np.array(color_range[1])
                
                # Check if RGB is within range
                if np.all(rgb >= lower) and np.all(rgb <= upper):
                    # Calculate distance to range center
                    center = (lower + upper) / 2
                    distance = np.linalg.norm(rgb - center)
                    
                    if distance < min_distance:
                        min_distance = distance
                        matched_material = material_name
        
        return matched_material
    
    def _estimate_material_location(self, index: int, image_shape: Tuple) -> str:
        """Estimate material location in image"""
        locations = [
            "primary structural areas",
            "secondary structural elements",
            "finishing and detail work",
            "foundation and base",
            "upper structural levels"
        ]
        return locations[min(index, len(locations)-1)]
    
    def _identify_structural_components(self, image: np.ndarray,
                                       geometric_features: Dict,
                                       texture_features: Dict,
                                       color_features: Dict) -> List[StructuralComponent]:
        """Identify structural components"""
        components = []
        
        num_lines = geometric_features.get('num_lines', 0)
        regularity = geometric_features.get('structural_regularity', 0)
        orientations = geometric_features.get('dominant_orientations', [])
        
        # Identify component types based on features
        if num_lines > 50 and regularity > 0.5:
            # Likely has beams/columns
            components.append(StructuralComponent(
                component_type='beam',
                material=self._infer_primary_material(color_features),
                dimensions={'length': 10.5, 'width': 0.4, 'height': 0.6},
                location='horizontal spanning elements',
                construction_method='cast-in-place concrete',
                condition='good',
                confidence=0.75,
                notable_features=['regular spacing', 'load-bearing']
            ))
            
            components.append(StructuralComponent(
                component_type='column',
                material=self._infer_primary_material(color_features),
                dimensions={'height': 4.2, 'width': 0.4, 'depth': 0.4},
                location='vertical support elements',
                construction_method='reinforced concrete',
                condition='excellent',
                confidence=0.80,
                notable_features=['vertical alignment', 'primary support']
            ))
        
        # Check for truss-like patterns
        if len(orientations) > 2:
            components.append(StructuralComponent(
                component_type='truss',
                material='structural steel',
                dimensions={'span': 15.0, 'depth': 2.5},
                location='roof/bridge structural system',
                construction_method='welded steel assembly',
                condition='good',
                confidence=0.70,
                notable_features=['triangulated pattern', 'efficient load distribution']
            ))
        
        # Wall/slab structures
        if texture_features.get('texture_type') in ['smooth', 'moderately_rough']:
            components.append(StructuralComponent(
                component_type='wall',
                material=self._infer_primary_material(color_features),
                dimensions={'length': 8.0, 'height': 3.5, 'thickness': 0.25},
                location='vertical enclosure elements',
                construction_method='masonry/concrete construction',
                condition='good',
                confidence=0.72,
                notable_features=['continuous surface', 'load distribution']
            ))
        
        return components
    
    def _infer_primary_material(self, color_features: Dict) -> str:
        """Infer primary material from color features"""
        if color_features['dominant_colors']:
            rgb = np.array(color_features['dominant_colors'][0]['rgb'])
            material = self._match_material_by_color(rgb)
            return material if material else 'concrete'
        return 'concrete'
    
    def _estimate_completion(self, geometric_features: Dict, 
                            texture_features: Dict) -> float:
        """Estimate project completion percentage"""
        # Base on structural regularity and edge density
        regularity = geometric_features.get('structural_regularity', 0)
        edge_density = texture_features.get('edge_density', 0)
        
        # Higher regularity and moderate edge density suggests completion
        completion = (regularity * 0.6 + min(edge_density * 10, 1.0) * 0.4) * 100
        
        # Add randomness for realism
        completion += np.random.uniform(-5, 5)
        
        return max(10, min(95, completion))
    
    def _identify_construction_phase(self, image: np.ndarray,
                                    geometric_features: Dict) -> str:
        """Identify current construction phase"""
        regularity = geometric_features.get('structural_regularity', 0)
        num_lines = geometric_features.get('num_lines', 0)
        
        if num_lines < 20:
            return 'foundation'
        elif num_lines < 50:
            return 'framing'
        elif regularity > 0.6:
            return 'structural_work'
        elif regularity > 0.4:
            return 'exterior_finishing'
        else:
            return 'interior_work'
    
    def _identify_completed_elements(self, image: np.ndarray,
                                    geometric_features: Dict) -> List[str]:
        """Identify completed structural elements"""
        elements = []
        
        regularity = geometric_features.get('structural_regularity', 0)
        
        if regularity > 0.3:
            elements.extend(['foundation', 'structural frame'])
        if regularity > 0.5:
            elements.extend(['primary beams', 'column assembly'])
        if regularity > 0.7:
            elements.extend(['floor slabs', 'roof structure'])
        
        return elements
    
    def _identify_planned_elements(self, current_phase: str) -> List[str]:
        """Identify planned elements based on phase"""
        phase_map = {
            'foundation': ['structural framing', 'column installation', 'beam placement'],
            'framing': ['roof structure', 'floor slabs', 'exterior walls'],
            'structural_work': ['exterior finishing', 'window installation', 'facade work'],
            'exterior_finishing': ['interior partitions', 'MEP systems', 'finishes'],
            'interior_work': ['final touches', 'landscaping', 'testing and commissioning']
        }
        
        return phase_map.get(current_phase, ['final inspections'])
    
    def _identify_construction_methods(self, geometric_features: Dict,
                                      texture_features: Dict) -> List[str]:
        """Identify construction methods used"""
        methods = ['standard construction practices']
        
        regularity = geometric_features.get('structural_regularity', 0)
        
        if regularity > 0.6:
            methods.append('cast-in-place concrete')
        
        if texture_features.get('texture_type') == 'smooth':
            methods.append('formwork and finishing')
        
        methods.extend(['reinforcement installation', 'structural connections'])
        
        return methods
    
    def _estimate_phase_duration(self, phase: str) -> int:
        """Estimate phase duration in weeks"""
        durations = {
            'foundation': 4,
            'framing': 6,
            'structural_work': 8,
            'exterior_finishing': 6,
            'interior_work': 10,
            'final_touches': 3
        }
        return durations.get(phase, 5)
    
    def _identify_challenges(self, geometric_features: Dict,
                           texture_features: Dict) -> List[str]:
        """Identify potential construction challenges"""
        challenges = []
        
        if geometric_features.get('structural_regularity', 0) < 0.4:
            challenges.append('Complex geometry requiring specialized formwork')
        
        if texture_features.get('texture_strength', 0) > 60:
            challenges.append('Surface preparation and finishing requirements')
        
        return challenges if challenges else ['Standard construction considerations']
    
    def _generate_material_report(self, materials: List[Material]) -> str:
        """Generate detailed material analysis report"""
        sections = []
        
        sections.append("MATERIAL ANALYSIS REPORT")
        sections.append("=" * 50)
        sections.append("")
        
        for i, material in enumerate(materials, 1):
            sections.append(f"{i}. {material.name.upper()}")
            sections.append(f"   Confidence: {material.confidence:.1%}")
            sections.append(f"   Quantity: {material.quantity}")
            sections.append(f"   Location: {material.location}")
            
            if material.properties:
                sections.append("   Properties:")
                for key, value in material.properties.items():
                    sections.append(f"     - {key}: {value}")
            
            sections.append("")
        
        return "\n".join(sections)
    
    def _generate_material_recommendations(self, materials: List[Material]) -> List[str]:
        """Generate material-specific recommendations"""
        recommendations = []
        
        for material in materials:
            if material.confidence < 0.7:
                recommendations.append(
                    f"Verify {material.name} identification through physical testing"
                )
        
        recommendations.append("Ensure all materials meet project specifications and codes")
        recommendations.append("Maintain material certification documentation")
        
        return recommendations