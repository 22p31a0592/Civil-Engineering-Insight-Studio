"""
Configuration settings for Civil Engineering Insight Studio Backend
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Upload settings
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
REPORTS_FOLDER = os.path.join(BASE_DIR, 'reports')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tiff'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORTS_FOLDER, exist_ok=True)

# API settings
API_VERSION = 'v1'
API_PREFIX = f'/api/{API_VERSION}'

# NLP Model settings
SPACY_MODEL = 'en_core_web_sm'
TRANSFORMER_MODEL = 'sentence-transformers/all-MiniLM-L6-v2'

# Analysis settings
CONFIDENCE_THRESHOLD = 0.6
MIN_OBJECT_SIZE = 50  # pixels

# Material database
CONSTRUCTION_MATERIALS = {
    'concrete': {
        'color_ranges': [(100, 100, 100), (180, 180, 180)],
        'textures': ['smooth', 'rough', 'aggregate'],
        'properties': ['compressive_strength', 'durability']
    },
    'steel': {
        'color_ranges': [(150, 150, 150), (200, 200, 200)],
        'textures': ['metallic', 'smooth', 'reflective'],
        'properties': ['tensile_strength', 'ductility']
    },
    'brick': {
        'color_ranges': [(120, 50, 30), (180, 100, 80)],
        'textures': ['rough', 'patterned', 'rectangular'],
        'properties': ['compressive_strength', 'thermal_insulation']
    },
    'wood': {
        'color_ranges': [(100, 70, 40), (200, 150, 100)],
        'textures': ['grainy', 'fibrous', 'natural'],
        'properties': ['flexibility', 'aesthetic']
    },
    'glass': {
        'color_ranges': [(200, 200, 200), (255, 255, 255)],
        'textures': ['transparent', 'smooth', 'reflective'],
        'properties': ['transparency', 'aesthetic']
    }
}

# Structural components
STRUCTURAL_COMPONENTS = [
    'beam', 'column', 'truss', 'foundation', 'slab', 'wall',
    'roof', 'arch', 'girder', 'joist', 'pier', 'abutment'
]

# Construction phases
CONSTRUCTION_PHASES = [
    'excavation', 'foundation', 'framing', 'structural_work',
    'roofing', 'exterior_finishing', 'interior_work', 'final_touches'
]

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    UPLOAD_FOLDER = UPLOAD_FOLDER
    REPORTS_FOLDER = REPORTS_FOLDER
    ALLOWED_EXTENSIONS = ALLOWED_EXTENSIONS
    MAX_FILE_SIZE = MAX_FILE_SIZE

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}