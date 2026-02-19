/**
 * ImageUpload Component - Handles drag-and-drop file upload
 */
import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import {
  Box,
  Typography,
  Paper,
  IconButton,
  Card,
  CardMedia,
} from '@mui/material';
import {
  CloudUpload,
  Delete,
  Image as ImageIcon,
} from '@mui/icons-material';

const ImageUpload = ({ onImageSelect, selectedImage }) => {
  const [preview, setPreview] = useState(null);

  const onDrop = useCallback(
    (acceptedFiles) => {
      if (acceptedFiles && acceptedFiles.length > 0) {
        const file = acceptedFiles[0];
        onImageSelect(file);

        // Create preview
        const reader = new FileReader();
        reader.onload = () => {
          setPreview(reader.result);
        };
        reader.readAsDataURL(file);
      }
    },
    [onImageSelect]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.bmp', '.tiff'],
    },
    maxFiles: 1,
    maxSize: 16 * 1024 * 1024, // 16MB
  });

  const handleRemove = () => {
    setPreview(null);
    onImageSelect(null);
  };

  return (
    <Box sx={{ width: '100%', mb: 3 }}>
      {!preview ? (
        <Paper
          {...getRootProps()}
          elevation={3}
          sx={{
            p: 4,
            textAlign: 'center',
            cursor: 'pointer',
            backgroundColor: isDragActive ? 'action.hover' : 'background.paper',
            border: '2px dashed',
            borderColor: isDragActive ? 'primary.main' : 'divider',
            transition: 'all 0.3s ease',
            '&:hover': {
              borderColor: 'primary.main',
              backgroundColor: 'action.hover',
            },
          }}
        >
          <input {...getInputProps()} />
          <CloudUpload sx={{ fontSize: 64, color: 'primary.main', mb: 2 }} />
          <Typography variant="h6" gutterBottom>
            {isDragActive
              ? 'Drop the image here'
              : 'Drag & drop an image here, or click to select'}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Supported formats: PNG, JPG, JPEG, BMP, TIFF (Max 16MB)
          </Typography>
        </Paper>
      ) : (
        <Card elevation={3}>
          <Box sx={{ position: 'relative' }}>
            <CardMedia
              component="img"
              image={preview}
              alt="Preview"
              sx={{
                maxHeight: 400,
                objectFit: 'contain',
                width: '100%',
              }}
            />
            <IconButton
              onClick={handleRemove}
              sx={{
                position: 'absolute',
                top: 8,
                right: 8,
                backgroundColor: 'background.paper',
                '&:hover': {
                  backgroundColor: 'error.light',
                  color: 'error.contrastText',
                },
              }}
            >
              <Delete />
            </IconButton>
          </Box>
          <Box sx={{ p: 2, backgroundColor: 'background.default' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <ImageIcon color="primary" />
              <Typography variant="body2">
                {selectedImage?.name} ({(selectedImage?.size / 1024).toFixed(2)} KB)
              </Typography>
            </Box>
          </Box>
        </Card>
      )}
    </Box>
  );
};

export default ImageUpload;