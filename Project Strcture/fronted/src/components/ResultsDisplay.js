/**
 * ResultsDisplay Component - Displays analysis results
 */
import React from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Chip,
  Divider,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemText,
  LinearProgress,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from '@mui/material';
import {
  ExpandMore,
  CheckCircle,
  Info,
  Warning,
  Construction,
  Architecture,
} from '@mui/icons-material';

const ResultsDisplay = ({ results }) => {
  if (!results) return null;

  const renderMaterials = () => {
    if (!results.materials || results.materials.length === 0) return null;

    return (
      <Accordion defaultExpanded>
        <AccordionSummary expandIcon={<ExpandMore />}>
          <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Construction color="primary" />
            Materials Identified ({results.materials.length})
          </Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Grid container spacing={2}>
            {results.materials.map((material, index) => (
              <Grid item xs={12} md={6} key={index}>
                <Card variant="outlined">
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Typography variant="h6" color="primary">
                        {material.name.charAt(0).toUpperCase() + material.name.slice(1)}
                      </Typography>
                      <Chip
                        label={`${(material.confidence * 100).toFixed(0)}%`}
                        color={material.confidence > 0.8 ? 'success' : 'warning'}
                        size="small"
                      />
                    </Box>
                    <Divider sx={{ my: 1 }} />
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      <strong>Quantity:</strong> {material.quantity}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      <strong>Location:</strong> {material.location}
                    </Typography>
                    {material.texture && (
                      <Typography variant="body2" color="text.secondary">
                        <strong>Texture:</strong> {material.texture.replace('_', ' ')}
                      </Typography>
                    )}
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </AccordionDetails>
      </Accordion>
    );
  };

  const renderStructuralComponents = () => {
    if (!results.structural_components || results.structural_components.length === 0)
      return null;

    return (
      <Accordion defaultExpanded>
        <AccordionSummary expandIcon={<ExpandMore />}>
          <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Architecture color="primary" />
            Structural Components ({results.structural_components.length})
          </Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Grid container spacing={2}>
            {results.structural_components.map((component, index) => (
              <Grid item xs={12} key={index}>
                <Card variant="outlined">
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Typography variant="h6" color="primary">
                        {component.component_type.charAt(0).toUpperCase() +
                          component.component_type.slice(1)}
                      </Typography>
                      <Chip
                        label={component.condition}
                        color={
                          component.condition.toLowerCase().includes('excellent')
                            ? 'success'
                            : component.condition.toLowerCase().includes('good')
                            ? 'primary'
                            : 'warning'
                        }
                        size="small"
                      />
                    </Box>
                    <Divider sx={{ my: 1 }} />
                    <Grid container spacing={2}>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="body2" color="text.secondary">
                          <strong>Material:</strong> {component.material}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          <strong>Location:</strong> {component.location}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          <strong>Method:</strong> {component.construction_method}
                        </Typography>
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="body2" color="text.secondary" gutterBottom>
                          <strong>Dimensions:</strong>
                        </Typography>
                        {Object.entries(component.dimensions || {}).map(([key, value]) => (
                          <Typography
                            key={key}
                            variant="body2"
                            color="text.secondary"
                            sx={{ ml: 2 }}
                          >
                            • {key}: {value}m
                          </Typography>
                        ))}
                      </Grid>
                    </Grid>
                    {component.notable_features && component.notable_features.length > 0 && (
                      <>
                        <Divider sx={{ my: 1 }} />
                        <Typography variant="body2" color="text.secondary">
                          <strong>Notable Features:</strong>
                        </Typography>
                        <Box sx={{ mt: 1 }}>
                          {component.notable_features.map((feature, idx) => (
                            <Chip
                              key={idx}
                              label={feature}
                              size="small"
                              sx={{ mr: 0.5, mb: 0.5 }}
                            />
                          ))}
                        </Box>
                      </>
                    )}
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </AccordionDetails>
      </Accordion>
    );
  };

  const renderProjectProgress = () => {
    if (!results.project_progress) return null;

    const progress = results.project_progress;

    return (
      <Accordion defaultExpanded>
        <AccordionSummary expandIcon={<ExpandMore />}>
          <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <CheckCircle color="primary" />
            Project Progress
          </Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Box sx={{ mb: 3 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
              <Typography variant="body2">Completion</Typography>
              <Typography variant="body2" fontWeight="bold">
                {progress.completion_percentage.toFixed(1)}%
              </Typography>
            </Box>
            <LinearProgress
              variant="determinate"
              value={progress.completion_percentage}
              sx={{ height: 8, borderRadius: 1 }}
            />
          </Box>

          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Paper variant="outlined" sx={{ p: 2 }}>
                <Typography variant="subtitle2" gutterBottom color="primary">
                  Current Phase
                </Typography>
                <Chip
                  label={progress.phase.replace('_', ' ').toUpperCase()}
                  color="primary"
                  sx={{ mb: 2 }}
                />
                {progress.timeline && (
                  <Typography variant="body2" color="text.secondary">
                    {progress.timeline}
                  </Typography>
                )}
              </Paper>
            </Grid>

            <Grid item xs={12} md={6}>
              <Paper variant="outlined" sx={{ p: 2 }}>
                <Typography variant="subtitle2" gutterBottom color="success.main">
                  Completed Elements
                </Typography>
                <List dense>
                  {progress.completed_elements.map((element, idx) => (
                    <ListItem key={idx} disableGutters>
                      <CheckCircle
                        sx={{ fontSize: 16, mr: 1, color: 'success.main' }}
                      />
                      <ListItemText primary={element} />
                    </ListItem>
                  ))}
                </List>
              </Paper>
            </Grid>

            <Grid item xs={12}>
              <Paper variant="outlined" sx={{ p: 2 }}>
                <Typography variant="subtitle2" gutterBottom color="info.main">
                  Planned Elements
                </Typography>
                <List dense>
                  {progress.planned_elements.map((element, idx) => (
                    <ListItem key={idx} disableGutters>
                      <Info sx={{ fontSize: 16, mr: 1, color: 'info.main' }} />
                      <ListItemText primary={element} />
                    </ListItem>
                  ))}
                </List>
              </Paper>
            </Grid>
          </Grid>
        </AccordionDetails>
      </Accordion>
    );
  };

  const renderRecommendations = () => {
    if (!results.recommendations || results.recommendations.length === 0) return null;

    return (
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMore />}>
          <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Warning color="warning" />
            Recommendations ({results.recommendations.length})
          </Typography>
        </AccordionSummary>
        <AccordionDetails>
          <List>
            {results.recommendations.map((recommendation, index) => (
              <ListItem key={index} disableGutters>
                <ListItemText
                  primary={`${index + 1}. ${recommendation}`}
                  primaryTypographyProps={{
                    variant: 'body2',
                  }}
                />
              </ListItem>
            ))}
          </List>
        </AccordionDetails>
      </Accordion>
    );
  };

  return (
    <Box sx={{ mt: 4 }}>
      {/* Summary Section */}
      <Paper elevation={3} sx={{ p: 3, mb: 3, backgroundColor: 'primary.main', color: 'white' }}>
        <Typography variant="h5" gutterBottom>
          Analysis Complete
        </Typography>
        {results.confidence_score > 0 && (
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Typography variant="body2">Overall Confidence:</Typography>
            <Chip
              label={`${(results.confidence_score * 100).toFixed(0)}%`}
              sx={{
                backgroundColor: 'rgba(255, 255, 255, 0.2)',
                color: 'white',
              }}
            />
          </Box>
        )}
      </Paper>

      {/* Summary Text */}
      {results.summary && (
        <Paper elevation={2} sx={{ p: 3, mb: 2 }}>
          <Typography variant="h6" gutterBottom>
            Summary
          </Typography>
          <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }}>
            {results.summary}
          </Typography>
        </Paper>
      )}

      {/* Detailed Results */}
      <Box sx={{ mb: 2 }}>
        {renderMaterials()}
        {renderStructuralComponents()}
        {renderProjectProgress()}
        {renderRecommendations()}
      </Box>

      {/* Detailed Description */}
      {results.detailed_description && (
        <Paper elevation={2} sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Detailed Description
          </Typography>
          <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }}>
            {results.detailed_description}
          </Typography>
        </Paper>
      )}
    </Box>
  );
};

export default ResultsDisplay;