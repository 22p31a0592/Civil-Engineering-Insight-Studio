/**
 * AnalysisTypeSelector Component - Allows user to select analysis type
 */
import React from 'react';
import {
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Box,
  Typography,
  Paper,
} from '@mui/material';
import {
  Science,
  Construction,
  Timeline,
  ViewInAr,
} from '@mui/icons-material';

const analysisTypes = [
  {
    id: 'material_identification',
    name: 'Material Identification',
    description: 'Identify construction materials like concrete, steel, and bricks',
    icon: <Science />,
  },
  {
    id: 'project_progress',
    name: 'Project Progress Documentation',
    description: 'Document construction progress and completion phases',
    icon: <Timeline />,
  },
  {
    id: 'structural_analysis',
    name: 'Structural Analysis',
    description: 'Analyze structural components like beams, columns, and trusses',
    icon: <ViewInAr />,
  },
  {
    id: 'comprehensive',
    name: 'Comprehensive Analysis',
    description: 'Complete analysis including all features above',
    icon: <Construction />,
  },
];

const AnalysisTypeSelector = ({ selectedType, onTypeSelect }) => {
  const handleChange = (event) => {
    onTypeSelect(event.target.value);
  };

  const selectedAnalysis = analysisTypes.find((type) => type.id === selectedType);

  return (
    <Box sx={{ mb: 3 }}>
      <FormControl fullWidth variant="outlined">
        <InputLabel id="analysis-type-label">Analysis Type</InputLabel>
        <Select
          labelId="analysis-type-label"
          id="analysis-type-select"
          value={selectedType}
          onChange={handleChange}
          label="Analysis Type"
        >
          {analysisTypes.map((type) => (
            <MenuItem key={type.id} value={type.id}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                {type.icon}
                <Typography>{type.name}</Typography>
              </Box>
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      {selectedAnalysis && (
        <Paper
          elevation={0}
          sx={{
            mt: 2,
            p: 2,
            backgroundColor: 'action.hover',
            border: '1px solid',
            borderColor: 'divider',
          }}
        >
          <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 2 }}>
            <Box sx={{ color: 'primary.main', mt: 0.5 }}>
              {selectedAnalysis.icon}
            </Box>
            <Box>
              <Typography variant="subtitle2" fontWeight="bold" gutterBottom>
                {selectedAnalysis.name}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {selectedAnalysis.description}
              </Typography>
            </Box>
          </Box>
        </Paper>
      )}
    </Box>
  );
};

export default AnalysisTypeSelector;