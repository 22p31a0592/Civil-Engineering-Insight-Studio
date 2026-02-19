# API Documentation

## Base URL
```
http://localhost:5000/api
```

## Endpoints

### 1. Health Check
Check if the API is running.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "service": "Civil Engineering Insight Studio",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00"
}
```

---

### 2. Get Analysis Types
Get list of available analysis types.

**Endpoint:** `GET /analysis-types`

**Response:**
```json
{
  "analysis_types": [
    {
      "id": "material_identification",
      "name": "Material Identification",
      "description": "Identify construction materials like concrete, steel, bricks"
    },
    {
      "id": "project_progress",
      "name": "Project Progress Documentation",
      "description": "Document construction progress and phases"
    },
    {
      "id": "structural_analysis",
      "name": "Structural Analysis",
      "description": "Analyze structural components like beams, columns, trusses"
    },
    {
      "id": "comprehensive",
      "name": "Comprehensive Analysis",
      "description": "Complete analysis including all above types"
    }
  ]
}
```

---

### 3. General Structure Analysis
Perform general structure analysis.

**Endpoint:** `POST /analyze`

**Request:**
- Content-Type: `multipart/form-data`
- Body:
  - `image` (file): Image file to analyze
  - `analysis_type` (string, optional): Type of analysis (default: "comprehensive")

**Example using cURL:**
```bash
curl -X POST http://localhost:5000/api/analyze \
  -F "image=@/path/to/image.jpg" \
  -F "analysis_type=comprehensive"
```

**Response:**
```json
{
  "success": true,
  "analysis": {
    "analysis_type": "comprehensive",
    "timestamp": "2024-01-15T10:30:00",
    "image_info": {
      "width": 1920,
      "height": 1080,
      "format": "jpg",
      "filename": "construction_site.jpg"
    },
    "materials": [...],
    "structural_components": [...],
    "summary": "Analysis summary...",
    "detailed_description": "Detailed technical description...",
    "recommendations": ["Recommendation 1", "Recommendation 2"],
    "confidence_score": 0.85
  },
  "message": "Analysis completed successfully"
}
```

---

### 4. Material Identification
Identify construction materials in an image.

**Endpoint:** `POST /identify-materials`

**Request:**
- Content-Type: `multipart/form-data`
- Body:
  - `image` (file): Image file to analyze

**Response:**
```json
{
  "success": true,
  "materials": [
    {
      "name": "concrete",
      "confidence": 0.87,
      "quantity": "45.2% of visible area",
      "location": "primary structural areas",
      "properties": {
        "compressive_strength": "high",
        "durability": "excellent"
      },
      "color_info": "RGB: [150, 150, 145]",
      "texture": "smooth"
    }
  ],
  "summary": "Material analysis summary...",
  "detailed_description": "Detailed material report...",
  "recommendations": ["Material-specific recommendations..."],
  "confidence_score": 0.82
}
```

---

### 5. Project Progress Documentation
Document construction project progress.

**Endpoint:** `POST /document-progress`

**Request:**
- Content-Type: `multipart/form-data`
- Body:
  - `image` (file): Image file of construction site

**Response:**
```json
{
  "success": true,
  "project_progress": {
    "phase": "structural_work",
    "completion_percentage": 65.5,
    "completed_elements": [
      "foundation",
      "structural frame",
      "primary beams"
    ],
    "planned_elements": [
      "roof structure",
      "exterior finishing",
      "window installation"
    ],
    "materials_used": [...],
    "construction_methods": [
      "cast-in-place concrete",
      "reinforcement installation"
    ],
    "timeline": "Estimated phase duration: 8 weeks",
    "challenges": ["Complex geometry requiring specialized formwork"]
  },
  "summary": "Progress summary...",
  "detailed_description": "Detailed progress report...",
  "recommendations": ["Progress-related recommendations..."],
  "materials": [...]
}
```

---

### 6. Structural Analysis
Analyze structural components.

**Endpoint:** `POST /structural-analysis`

**Request:**
- Content-Type: `multipart/form-data`
- Body:
  - `image` (file): Image file of structure

**Response:**
```json
{
  "success": true,
  "structural_components": [
    {
      "component_type": "beam",
      "material": "concrete",
      "dimensions": {
        "length": 10.5,
        "width": 0.4,
        "height": 0.6
      },
      "location": "horizontal spanning elements",
      "construction_method": "cast-in-place concrete",
      "condition": "good",
      "confidence": 0.75,
      "notable_features": [
        "regular spacing",
        "load-bearing"
      ]
    }
  ],
  "materials": [...],
  "summary": "Structural analysis summary...",
  "detailed_description": "Detailed structural report...",
  "recommendations": ["Structural recommendations..."],
  "confidence_score": 0.78
}
```

---

## Data Models

### Material Object
```typescript
{
  name: string,              // Material name (concrete, steel, brick, etc.)
  confidence: number,        // Confidence score (0-1)
  quantity: string,          // Quantity description
  location: string,          // Location in structure
  properties: {              // Material properties
    [key: string]: string
  },
  color_info?: string,       // RGB color information
  texture?: string           // Texture type
}
```

### Structural Component Object
```typescript
{
  component_type: string,    // Type (beam, column, truss, etc.)
  material: string,          // Material composition
  dimensions: {              // Physical dimensions
    [key: string]: number
  },
  location: string,          // Location description
  construction_method: string, // Construction method used
  condition: string,         // Current condition
  confidence: number,        // Confidence score (0-1)
  notable_features: string[] // List of notable features
}
```

### Project Progress Object
```typescript
{
  phase: string,             // Current construction phase
  completion_percentage: number, // Completion % (0-100)
  completed_elements: string[],  // List of completed elements
  planned_elements: string[],    // List of planned elements
  materials_used: Material[],    // Materials being used
  construction_methods: string[], // Methods employed
  timeline?: string,         // Timeline information
  challenges: string[]       // Identified challenges
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "No image file provided",
  "message": "Please upload an image file"
}
```

### 413 Payload Too Large
```json
{
  "error": "File too large",
  "message": "Maximum file size is 16MB"
}
```

### 500 Internal Server Error
```json
{
  "error": "Analysis failed",
  "message": "Error details..."
}
```

---

## Rate Limits
Currently no rate limits are enforced. In production, consider implementing:
- 100 requests per hour per IP
- 1000 requests per day per API key

## Authentication
Current version does not require authentication. For production deployment, implement:
- API key authentication
- JWT tokens
- OAuth 2.0

## File Constraints
- **Supported formats:** PNG, JPG, JPEG, BMP, TIFF
- **Maximum file size:** 16 MB
- **Recommended resolution:** 1920x1080 or higher
- **Minimum resolution:** 640x480

## Best Practices
1. Compress images before upload for faster processing
2. Use high-quality images for better analysis accuracy
3. Ensure good lighting in construction site photos
4. Include clear views of structural elements
5. Avoid heavily obstructed views