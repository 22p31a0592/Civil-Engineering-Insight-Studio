/**
 * API Service - Handles all backend communication
 */
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'multipart/form-data',
  },
  timeout: 60000, // 60 second timeout for image processing
});

/**
 * API Service Class
 */
class ApiService {
  /**
   * Health check
   */
  async healthCheck() {
    try {
      const response = await apiClient.get('/health');
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Get available analysis types
   */
  async getAnalysisTypes() {
    try {
      const response = await apiClient.get('/analysis-types');
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Perform general analysis
   * @param {File} imageFile - Image file to analyze
   * @param {string} analysisType - Type of analysis to perform
   */
  async analyzeStructure(imageFile, analysisType = 'comprehensive') {
    try {
      const formData = new FormData();
      formData.append('image', imageFile);
      formData.append('analysis_type', analysisType);

      const response = await apiClient.post('/analyze', formData);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Identify materials in construction
   * @param {File} imageFile - Image file to analyze
   */
  async identifyMaterials(imageFile) {
    try {
      const formData = new FormData();
      formData.append('image', imageFile);

      const response = await apiClient.post('/identify-materials', formData);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Document project progress
   * @param {File} imageFile - Image file to analyze
   */
  async documentProgress(imageFile) {
    try {
      const formData = new FormData();
      formData.append('image', imageFile);

      const response = await apiClient.post('/document-progress', formData);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Perform structural analysis
   * @param {File} imageFile - Image file to analyze
   */
  async structuralAnalysis(imageFile) {
    try {
      const formData = new FormData();
      formData.append('image', imageFile);

      const response = await apiClient.post('/structural-analysis', formData);
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }

  /**
   * Handle API errors
   * @param {Error} error - Axios error object
   */
  handleError(error) {
    if (error.response) {
      // Server responded with error
      return {
        message: error.response.data.message || error.response.data.error || 'Server error',
        status: error.response.status,
        data: error.response.data
      };
    } else if (error.request) {
      // No response received
      return {
        message: 'No response from server. Please check your connection.',
        status: 0
      };
    } else {
      // Request setup error
      return {
        message: error.message || 'An unexpected error occurred',
        status: -1
      };
    }
  }
}

export default new ApiService();