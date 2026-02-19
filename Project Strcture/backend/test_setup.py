"""
Simple test script to verify backend installation and functionality
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

def test_imports():
    """Test if all required packages are installed"""
    print("Testing package imports...")
    
    try:
        import flask
        print("✓ Flask")
    except ImportError:
        print("✗ Flask - Run: pip install flask")
        return False
    
    try:
        import cv2
        print("✓ OpenCV")
    except ImportError:
        print("✗ OpenCV - Run: pip install opencv-python")
        return False
    
    try:
        import spacy
        print("✓ spaCy")
    except ImportError:
        print("✗ spaCy - Run: pip install spacy")
        return False
    
    try:
        import transformers
        print("✓ Transformers")
    except ImportError:
        print("✗ Transformers - Run: pip install transformers")
        return False
    
    try:
        import numpy
        print("✓ NumPy")
    except ImportError:
        print("✗ NumPy - Run: pip install numpy")
        return False
    
    return True

def test_spacy_model():
    """Test if spaCy model is downloaded"""
    print("\nTesting spaCy model...")
    
    try:
        import spacy
        nlp = spacy.load('en_core_web_sm')
        doc = nlp("Test sentence")
        print("✓ spaCy model 'en_core_web_sm' loaded successfully")
        return True
    except OSError:
        print("✗ spaCy model not found - Run: python -m spacy download en_core_web_sm")
        return False

def test_modules():
    """Test if custom modules can be imported"""
    print("\nTesting custom modules...")
    
    try:
        from models.analysis_model import Material, AnalysisResult
        print("✓ Models module")
    except ImportError as e:
        print(f"✗ Models module - {e}")
        return False
    
    try:
        from services.nlp_analyzer import NLPAnalyzer
        print("✓ NLP Analyzer")
    except ImportError as e:
        print(f"✗ NLP Analyzer - {e}")
        return False
    
    try:
        from services.structure_analyzer import StructureAnalyzer
        print("✓ Structure Analyzer")
    except ImportError as e:
        print(f"✗ Structure Analyzer - {e}")
        return False
    
    try:
        from utils.image_utils import ImageProcessor
        print("✓ Image Processor")
    except ImportError as e:
        print(f"✗ Image Processor - {e}")
        return False
    
    return True

def test_directories():
    """Test if required directories exist"""
    print("\nTesting directory structure...")
    
    required_dirs = ['uploads', 'reports', 'models', 'services', 'controllers', 'utils']
    all_exist = True
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✓ {dir_name}/")
        else:
            print(f"✗ {dir_name}/ - Directory missing")
            all_exist = False
    
    return all_exist

def run_tests():
    """Run all tests"""
    print("=" * 60)
    print("Civil Engineering Insight Studio - Backend Test Suite")
    print("=" * 60)
    
    results = []
    
    # Test imports
    results.append(("Package Imports", test_imports()))
    
    # Test spaCy model
    results.append(("spaCy Model", test_spacy_model()))
    
    # Test directories
    results.append(("Directory Structure", test_directories()))
    
    # Test custom modules
    results.append(("Custom Modules", test_modules()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "PASSED" if passed else "FAILED"
        symbol = "✓" if passed else "✗"
        print(f"{symbol} {test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("=" * 60)
    if all_passed:
        print("✓ All tests passed! Backend is ready to run.")
        print("\nRun: python app.py")
    else:
        print("✗ Some tests failed. Please fix the issues above.")
    print("=" * 60)
    
    return all_passed

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)