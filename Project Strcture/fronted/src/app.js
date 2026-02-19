/**
 * App Component - Main Application
 */
import React, { useState } from 'react';
import {
  Container,
  Box,
  Typography,
  Button,
  Alert,
  CircularProgress,
  ThemeProvider,
  createTheme,
  CssBaseline,
  AppBar,
  Toolbar,
  Paper,
} from '@mui/material';
import { Engineering, PlayArrow } from '@mui/icons-material';

import ImageUpload from './components/ImageUpload';
import AnalysisTypeSelector from './components/AnalysisTypeSelector';
import ResultsDisplay from './components/ResultsDisplay';
import apiService from './services/apiService';

// Create theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
  },
});

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [analysisType, setAnalysisType] = useState('comprehensive');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleAnalyze = async () => {
    if (!selectedImage) {
      setError('Please select an image first');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      let response;

      // Call appropriate API based on analysis type
      switch (analysisType) {
        case 'material_identification':
          response = await apiService.identifyMaterials(selectedImage);
          break;
        case 'project_progress':
          response = await apiService.documentProgress(selectedImage);
          break;
        case 'structural_analysis':
          response = await apiService.structuralAnalysis(selectedImage);
          break;
        default:
          response = await apiService.analyzeStructure(selectedImage, analysisType);
      }

      if (response.success) {
        setResults(response.analysis || response);
      } else {
        setError(response.message || 'Analysis failed');
      }
    } catch (err) {
      setError(err.message || 'An error occurred during analysis');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ flexGrow: 1 }}>
        {/* App Bar */}
        <AppBar position="static" elevation={2}>
          <Toolbar>
            <Engineering sx={{ mr: 2, fontSize: 32 }} />
            <Typography variant="h5" component="div" sx={{ flexGrow: 1 }}>
              Civil Engineering Insight Studio
            </Typography>
          </Toolbar>
        </AppBar>

        {/* Main Content */}
        <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
          {/* Introduction */}
          <Paper elevation={3} sx={{ p: 3, mb: 4, backgroundColor: 'background.paper' }}>
            <Typography variant="h6" gutterBottom>
              Welcome to Civil Engineering Insight Studio
            </Typography>
            <Typography variant="body2" color="text.secondary">
              An AI-powered tool for automated analysis of civil engineering structures. Upload
              an image of a construction site, building, or infrastructure, select your analysis
              type, and get detailed insights powered by computer vision and natural language
              processing.
            </Typography>
          </Paper>

          {/* Upload Section */}
          <Box sx={{ mb: 4 }}>
            <Typography variant="h6" gutterBottom>
              Step 1: Upload Image
            </Typography>
            <ImageUpload
              onImageSelect={setSelectedImage}
              selectedImage={selectedImage}
            />
          </Box>

          {/* Analysis Type Selection */}
          <Box sx={{ mb: 4 }}>
            <Typography variant="h6" gutterBottom>
              Step 2: Select Analysis Type
            </Typography>
            <AnalysisTypeSelector
              selectedType={analysisType}
              onTypeSelect={setAnalysisType}
            />
          </Box>

          {/* Analyze Button */}
          <Box sx={{ mb: 4, display: 'flex', justifyContent: 'center' }}>
            <Button
              variant="contained"
              size="large"
              startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <PlayArrow />}
              onClick={handleAnalyze}
              disabled={!selectedImage || loading}
              sx={{ minWidth: 200, py: 1.5 }}
            >
              {loading ? 'Analyzing...' : 'Start Analysis'}
            </Button>
          </Box>

          {/* Error Display */}
          {error && (
            <Alert severity="error" onClose={() => setError(null)} sx={{ mb: 3 }}>
              {error}
            </Alert>
          )}

          {/* Results Display */}
          {results && <ResultsDisplay results={results} />}

          {/* Loading Indicator */}
          {loading && (
            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mt: 4 }}>
              <CircularProgress size={60} sx={{ mb: 2 }} />
              <Typography variant="body1" color="text.secondary">
                Processing image and generating insights...
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                This may take a few moments
              </Typography>
            </Box>
          )}
        </Container>

        {/* Footer */}
        <Box
          component="footer"
          sx={{
            py: 3,
            px: 2,
            mt: 'auto',
            backgroundColor: 'background.paper',
            borderTop: '1px solid',
            borderColor: 'divider',
          }}
        >
          <Container maxWidth="lg">
            <Typography variant="body2" color="text.secondary" align="center">
              © 2024 Civil Engineering Insight Studio. Powered by AI and Computer Vision.
            </Typography>
          </Container>
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default App;