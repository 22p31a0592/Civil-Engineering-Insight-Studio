# System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        CIVIL ENGINEERING INSIGHT STUDIO                  │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND LAYER                               │
│                            (React Application)                            │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐         │
│  │  App Component  │  │  Image Upload   │  │ Analysis Type   │         │
│  │   (Main UI)     │  │   Component     │  │    Selector     │         │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘         │
│           │                    │                     │                   │
│           └────────────────────┴─────────────────────┘                   │
│                                │                                          │
│                    ┌───────────▼───────────┐                             │
│                    │   Results Display     │                             │
│                    │     Component         │                             │
│                    └───────────────────────┘                             │
│                                │                                          │
│           ┌────────────────────┴────────────────────┐                    │
│           │          API Service Layer              │                    │
│           │        (Axios HTTP Client)              │                    │
│           └────────────────────┬────────────────────┘                    │
└────────────────────────────────┼─────────────────────────────────────────┘
                                 │
                          HTTP REST API
                                 │
┌────────────────────────────────▼─────────────────────────────────────────┐
│                              BACKEND LAYER                                │
│                         (Flask REST API Server)                           │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────────┐     │
│  │                    CONTROLLERS LAYER                            │     │
│  │                                                                  │     │
│  │  ┌────────────────────────────────────────────────────────┐    │     │
│  │  │      Analysis Controller (API Endpoints)               │    │     │
│  │  │                                                         │    │     │
│  │  │  • POST /analyze                                       │    │     │
│  │  │  • POST /identify-materials                            │    │     │
│  │  │  • POST /document-progress                             │    │     │
│  │  │  • POST /structural-analysis                           │    │     │
│  │  │  • GET  /analysis-types                                │    │     │
│  │  │  • GET  /health                                        │    │     │
│  │  └────────────────────┬───────────────────────────────────┘    │     │
│  └───────────────────────┼────────────────────────────────────────┘     │
│                          │                                               │
│  ┌───────────────────────▼────────────────────────────────────────┐     │
│  │                    SERVICES LAYER                              │     │
│  │                                                                 │     │
│  │  ┌──────────────────────────────────────────────────────┐     │     │
│  │  │         Structure Analyzer (Main Engine)             │     │     │
│  │  │                                                       │     │     │
│  │  │  • analyze_structure()                               │     │     │
│  │  │  • _analyze_materials()                              │     │     │
│  │  │  • _analyze_progress()                               │     │     │
│  │  │  • _analyze_structure()                              │     │     │
│  │  │  • _identify_materials()                             │     │     │
│  │  │  • _identify_structural_components()                 │     │     │
│  │  └──────────────┬────────────────┬──────────────────────┘     │     │
│  │                 │                │                             │     │
│  │  ┌──────────────▼─────────┐  ┌──▼────────────────────────┐   │     │
│  │  │    NLP Analyzer        │  │    Image Processor        │   │     │
│  │  │                        │  │                           │   │     │
│  │  │  • spaCy NLP          │  │  • OpenCV Processing      │   │     │
│  │  │  • Sentence Trans.    │  │  • Feature Extraction     │   │     │
│  │  │  • Text Generation    │  │  • Color Analysis         │   │     │
│  │  │  • Technical Vocab    │  │  • Texture Detection      │   │     │
│  │  │  • Description        │  │  • Edge Detection         │   │     │
│  │  │    Templates          │  │  • Line Detection         │   │     │
│  │  └───────────────────────┘  └───────────────────────────┘   │     │
│  └─────────────────────────────────────────────────────────────┘     │
│                                                                        │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │                      MODELS LAYER                               │ │
│  │                                                                  │ │
│  │  • Material                                                     │ │
│  │  • StructuralComponent                                          │ │
│  │  • ProjectProgress                                              │ │
│  │  • AnalysisResult                                               │ │
│  │  • AnalysisResultBuilder                                        │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │                      UTILS LAYER                                │ │
│  │                                                                  │ │
│  │  • ImageProcessor (CV utilities)                                │ │
│  │  • TextProcessor (NLP utilities)                                │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│                           DATA FLOW                                     │
├────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. User uploads image → Frontend                                      │
│  2. Frontend sends POST request → Backend API                          │
│  3. Controller receives request → Structure Analyzer                   │
│  4. Structure Analyzer:                                                │
│     a. Image Processor extracts features (color, texture, geometry)    │
│     b. Identifies materials/components using CV algorithms             │
│     c. NLP Analyzer generates technical descriptions                   │
│     d. Builds AnalysisResult object with all findings                  │
│  5. Controller returns JSON response → Frontend                        │
│  6. Results Display renders findings → User                            │
│                                                                         │
└────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│                      TECHNOLOGY STACK                                   │
├────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Frontend:                                                              │
│    • React 18                                                           │
│    • Material-UI (MUI)                                                  │
│    • Axios                                                              │
│    • React Dropzone                                                     │
│                                                                         │
│  Backend:                                                               │
│    • Flask (Web Framework)                                              │
│    • OpenCV (Computer Vision)                                           │
│    • spaCy (NLP)                                                        │
│    • Transformers (Sentence Embeddings)                                 │
│    • NumPy (Numerical Computing)                                        │
│                                                                         │
│  NLP Models:                                                            │
│    • en_core_web_sm (spaCy)                                            │
│    • all-MiniLM-L6-v2 (Sentence Transformer)                           │
│                                                                         │
└────────────────────────────────────────────────────────────────────────┘
```

## Key Features

### 1. Image Processing Pipeline
- Preprocessing (resize, denoise, enhance)
- Feature extraction (color, texture, geometry)
- Object detection (edges, lines, regions)
- Material matching using color/texture signatures

### 2. NLP Analysis Engine
- Technical vocabulary database
- Description template system
- Semantic similarity analysis
- Automated report generation

### 3. Analysis Types
- **Material Identification**: Detect and classify construction materials
- **Project Progress**: Document construction phases and completion
- **Structural Analysis**: Identify and analyze structural components
- **Comprehensive**: Complete analysis combining all types

### 4. Results Generation
- Confidence scoring
- Detailed technical descriptions
- Engineering recommendations
- Structured JSON output

## Design Patterns Used

- **Builder Pattern**: AnalysisResultBuilder for constructing results
- **Service Layer Pattern**: Separation of business logic
- **Repository Pattern**: Data models for entities
- **Factory Pattern**: API endpoint routing
- **Strategy Pattern**: Multiple analysis strategies