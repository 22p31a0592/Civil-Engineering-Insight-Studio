"""
Image Processing Utilities for Structure Analysis
"""
import cv2
import numpy as np
from PIL import Image
import io
from typing import Tuple, List, Dict, Optional


class ImageProcessor:
    """Handles image preprocessing and feature extraction"""
    
    def __init__(self):
        self.supported_formats = ['jpg', 'jpeg', 'png', 'bmp', 'tiff']
    
    def load_image(self, image_path: str) -> np.ndarray:
        """Load image from file path"""
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Unable to load image from {image_path}")
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    def load_image_from_bytes(self, image_bytes: bytes) -> np.ndarray:
        """Load image from bytes"""
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Unable to decode image from bytes")
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Apply preprocessing to enhance features"""
        # Resize if too large
        max_dimension = 1920
        height, width = image.shape[:2]
        
        if max(height, width) > max_dimension:
            scale = max_dimension / max(height, width)
            new_width = int(width * scale)
            new_height = int(height * scale)
            image = cv2.resize(image, (new_width, new_height))
        
        # Apply denoising
        denoised = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
        
        # Enhance contrast
        lab = cv2.cvtColor(denoised, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        enhanced = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2RGB)
        
        return enhanced
    
    def extract_color_features(self, image: np.ndarray) -> Dict[str, any]:
        """Extract color-based features"""
        # Calculate dominant colors
        pixels = image.reshape(-1, 3)
        pixels = np.float32(pixels)
        
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
        k = 5
        _, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        
        centers = np.uint8(centers)
        
        # Calculate color percentages
        unique_labels, counts = np.unique(labels, return_counts=True)
        percentages = (counts / len(labels)) * 100
        
        dominant_colors = []
        for i, (center, percentage) in enumerate(zip(centers, percentages)):
            dominant_colors.append({
                'rgb': center.tolist(),
                'percentage': float(percentage)
            })
        
        # Sort by percentage
        dominant_colors.sort(key=lambda x: x['percentage'], reverse=True)
        
        return {
            'dominant_colors': dominant_colors[:3],
            'average_color': np.mean(image, axis=(0, 1)).tolist(),
            'color_variance': np.var(image, axis=(0, 1)).tolist()
        }
    
    def extract_texture_features(self, image: np.ndarray) -> Dict[str, any]:
        """Extract texture features"""
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Calculate gradient magnitude
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        gradient_magnitude = np.sqrt(sobelx**2 + sobely**2)
        
        # Calculate texture metrics
        texture_strength = np.mean(gradient_magnitude)
        texture_variance = np.var(gradient_magnitude)
        
        # Edge detection
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / edges.size
        
        return {
            'texture_strength': float(texture_strength),
            'texture_variance': float(texture_variance),
            'edge_density': float(edge_density),
            'texture_type': self._classify_texture(texture_strength, edge_density)
        }
    
    def _classify_texture(self, strength: float, edge_density: float) -> str:
        """Classify texture type based on metrics"""
        if strength > 50 and edge_density > 0.1:
            return "rough"
        elif strength > 30 and edge_density > 0.05:
            return "moderately_rough"
        elif strength < 20 and edge_density < 0.03:
            return "smooth"
        else:
            return "mixed"
    
    def detect_edges(self, image: np.ndarray) -> np.ndarray:
        """Detect edges in image"""
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        return edges
    
    def detect_lines(self, image: np.ndarray) -> List[List[int]]:
        """Detect lines using Hough Transform"""
        edges = self.detect_edges(image)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, 
                                minLineLength=100, maxLineGap=10)
        
        if lines is None:
            return []
        
        return lines.tolist()
    
    def segment_regions(self, image: np.ndarray) -> Tuple[np.ndarray, int]:
        """Segment image into regions"""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Apply thresholding
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Create segmentation mask
        mask = np.zeros_like(gray)
        for i, contour in enumerate(contours):
            cv2.drawContours(mask, [contour], -1, (i+1)*10, -1)
        
        return mask, len(contours)
    
    def extract_geometric_features(self, image: np.ndarray) -> Dict[str, any]:
        """Extract geometric features"""
        edges = self.detect_edges(image)
        lines = self.detect_lines(image)
        
        # Calculate line orientations
        orientations = []
        if lines:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
                orientations.append(angle)
        
        return {
            'num_lines': len(lines) if lines else 0,
            'dominant_orientations': self._get_dominant_orientations(orientations),
            'edge_density': np.sum(edges > 0) / edges.size,
            'structural_regularity': self._calculate_regularity(orientations)
        }
    
    def _get_dominant_orientations(self, orientations: List[float], 
                                   bins: int = 8) -> List[Dict[str, float]]:
        """Get dominant line orientations"""
        if not orientations:
            return []
        
        hist, bin_edges = np.histogram(orientations, bins=bins, range=(-90, 90))
        dominant = []
        
        for i in range(bins):
            if hist[i] > 0:
                dominant.append({
                    'angle': float((bin_edges[i] + bin_edges[i+1]) / 2),
                    'count': int(hist[i])
                })
        
        dominant.sort(key=lambda x: x['count'], reverse=True)
        return dominant[:3]
    
    def _calculate_regularity(self, orientations: List[float]) -> float:
        """Calculate structural regularity score"""
        if not orientations:
            return 0.0
        
        # Check for horizontal and vertical alignment
        horizontal = sum(1 for angle in orientations if abs(angle) < 10 or abs(angle - 180) < 10)
        vertical = sum(1 for angle in orientations if abs(angle - 90) < 10 or abs(angle + 90) < 10)
        
        regularity = (horizontal + vertical) / len(orientations)
        return float(regularity)
    
    def get_image_metadata(self, image: np.ndarray, filename: str = "") -> Dict[str, any]:
        """Extract image metadata"""
        height, width = image.shape[:2]
        
        return {
            'filename': filename,
            'width': int(width),
            'height': int(height),
            'aspect_ratio': float(width / height),
            'total_pixels': int(width * height),
            'format': filename.split('.')[-1] if '.' in filename else 'unknown'
        }