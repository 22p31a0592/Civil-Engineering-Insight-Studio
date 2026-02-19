"""
Analysis Controller - REST API Endpoints
"""
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from datetime import datetime

from services.structure_analyzer import StructureAnalyzer
#from services.image_processor import ImageProcessor # type: ignore
import config

analysis_bp = Blueprint('analysis', __name__)
analyzer = StructureAnalyzer()


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


@analysis_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Civil Engineering Insight Studio',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    }), 200


@analysis_bp.route('/analyze', methods=['POST'])
def analyze_structure():
    """
    Main analysis endpoint
    Accepts: image file, analysis_type
    Returns: analysis results
    """
    try:
        # Check if image file is present
        if 'image' not in request.files:
            return jsonify({
                'error': 'No image file provided',
                'message': 'Please upload an image file'
            }), 400
        
        file = request.files['image']
        analysis_type = request.form.get('analysis_type', 'comprehensive')
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({
                'error': 'No file selected',
                'message': 'Please select a file to upload'
            }), 400
        
        # Check file type
        if not allowed_file(file.filename):
            return jsonify({
                'error': 'Invalid file type',
                'message': f'Allowed types: {", ".join(config.ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Perform analysis
        result = analyzer.analyze_structure(filepath, analysis_type)
        
        return jsonify({
            'success': True,
            'analysis': result.to_dict(),
            'message': 'Analysis completed successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Analysis failed',
            'message': str(e)
        }), 500


@analysis_bp.route('/identify-materials', methods=['POST'])
def identify_materials():
    """
    Material identification endpoint
    Specialized for identifying construction materials
    """
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Perform material identification
        result = analyzer.analyze_structure(filepath, 'material_identification')
        
        return jsonify({
            'success': True,
            'materials': [m.to_dict() for m in result.materials],
            'summary': result.summary,
            'detailed_description': result.detailed_description,
            'recommendations': result.recommendations,
            'confidence_score': result.confidence_score
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Material identification failed',
            'message': str(e)
        }), 500


@analysis_bp.route('/document-progress', methods=['POST'])
def document_progress():
    """
    Project progress documentation endpoint
    """
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Perform progress analysis
        result = analyzer.analyze_structure(filepath, 'project_progress')
        
        return jsonify({
            'success': True,
            'project_progress': result.project_progress.to_dict() if result.project_progress else None,
            'summary': result.summary,
            'detailed_description': result.detailed_description,
            'recommendations': result.recommendations,
            'materials': [m.to_dict() for m in result.materials]
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Progress documentation failed',
            'message': str(e)
        }), 500


@analysis_bp.route('/structural-analysis', methods=['POST'])
def structural_analysis():
    """
    Structural analysis endpoint
    Analyzes structural components and integrity
    """
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Perform structural analysis
        result = analyzer.analyze_structure(filepath, 'structural_analysis')
        
        return jsonify({
            'success': True,
            'structural_components': [c.to_dict() for c in result.structural_components],
            'materials': [m.to_dict() for m in result.materials],
            'summary': result.summary,
            'detailed_description': result.detailed_description,
            'recommendations': result.recommendations,
            'confidence_score': result.confidence_score
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Structural analysis failed',
            'message': str(e)
        }), 500


@analysis_bp.route('/analysis-types', methods=['GET'])
def get_analysis_types():
    """Get available analysis types"""
    return jsonify({
        'analysis_types': [
            {
                'id': 'material_identification',
                'name': 'Material Identification',
                'description': 'Identify construction materials like concrete, steel, bricks'
            },
            {
                'id': 'project_progress',
                'name': 'Project Progress Documentation',
                'description': 'Document construction progress and phases'
            },
            {
                'id': 'structural_analysis',
                'name': 'Structural Analysis',
                'description': 'Analyze structural components like beams, columns, trusses'
            },
            {
                'id': 'comprehensive',
                'name': 'Comprehensive Analysis',
                'description': 'Complete analysis including all above types'
            }
        ]
    }), 200


@analysis_bp.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return jsonify({
        'error': 'File too large',
        'message': f'Maximum file size is {config.MAX_FILE_SIZE / (1024*1024):.0f}MB'
    }), 413


@analysis_bp.errorhandler(500)
def internal_server_error(error):
    """Handle internal server errors"""
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500