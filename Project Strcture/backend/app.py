"""
Civil Engineering Insight Studio - Flask Application
Main application entry point
"""
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os
from werkzeug.exceptions import HTTPException

from config import config
from controllers.analysis_controller import analysis_bp


def create_app(config_name='development'):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Enable CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000", "http://localhost:5000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Set max file size
    app.config['MAX_CONTENT_LENGTH'] = config[config_name].MAX_FILE_SIZE
    
    # Register blueprints
    app.register_blueprint(analysis_bp, url_prefix='/api')
    
    # Root route
    @app.route('/')
    def index():
        return jsonify({
            'service': 'Civil Engineering Insight Studio API',
            'version': '1.0.0',
            'status': 'running',
            'endpoints': {
                'health': '/api/health',
                'analyze': '/api/analyze',
                'material_identification': '/api/identify-materials',
                'project_progress': '/api/document-progress',
                'structural_analysis': '/api/structural-analysis',
                'analysis_types': '/api/analysis-types'
            },
            'documentation': 'See README.md for API documentation'
        })
    
    # Serve uploaded files (for development only)
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not found',
            'message': 'The requested resource was not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred'
        }), 500
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return jsonify({
            'error': e.name,
            'message': e.description
        }), e.code
    
    return app


if __name__ == '__main__':
    # Create application
    app = create_app('development')
    
    # Print startup information
    print("=" * 60)
    print("Civil Engineering Insight Studio - Backend Server")
    print("=" * 60)
    print(f"Server starting on http://127.0.0.1:5000")
    print(f"API Base URL: http://127.0.0.1:5000/api")
    print("=" * 60)
    print("\nAvailable Endpoints:")
    print("  GET  /api/health               - Health check")
    print("  POST /api/analyze              - General analysis")
    print("  POST /api/identify-materials   - Material identification")
    print("  POST /api/document-progress    - Progress documentation")
    print("  POST /api/structural-analysis  - Structural analysis")
    print("  GET  /api/analysis-types       - Get available analysis types")
    print("=" * 60)
    
    # Run server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )