# Installation and Setup Guide

## Prerequisites

### Backend Requirements
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Frontend Requirements
- Node.js 14.x or higher
- npm or yarn

## Backend Setup

### 1. Navigate to Backend Directory
```bash
cd backend
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Download NLP Model
```bash
python -m spacy download en_core_web_sm
```

### 5. Verify Installation
```bash
python -c "import cv2, spacy, transformers; print('All packages installed successfully!')"
```

### 6. Run Backend Server
```bash
python app.py
```

The backend server will start on `http://localhost:5000`

## Frontend Setup

### 1. Navigate to Frontend Directory
```bash
cd frontend
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Start Development Server
```bash
npm start
```

The frontend will start on `http://localhost:3000`

## Troubleshooting

### Backend Issues

**Issue: spaCy model not found**
```bash
python -m spacy download en_core_web_sm
```

**Issue: OpenCV not installing**
```bash
pip install opencv-python-headless
```

**Issue: torch installation failing**
```bash
# For CPU-only version (smaller)
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### Frontend Issues

**Issue: npm install fails**
```bash
npm cache clean --force
npm install
```

**Issue: Port 3000 already in use**
```bash
# Use different port
PORT=3001 npm start
```

## Environment Variables

### Backend (.env file)
Create a `.env` file in the backend directory:
```
FLASK_ENV=development
FLASK_APP=app.py
SECRET_KEY=your-secret-key-here
```

### Frontend (.env file)
Create a `.env` file in the frontend directory:
```
REACT_APP_API_URL=http://localhost:5000/api
```

## Production Deployment

### Backend Production
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend Production
```bash
npm run build
# Serve the build folder with your preferred web server
```

## Testing the Application

1. Start both backend and frontend servers
2. Open browser to `http://localhost:3000`
3. Upload a sample construction image
4. Select an analysis type
5. Click "Start Analysis"
6. View the generated results

## Sample Test Images

For testing, use images of:
- Construction sites
- Buildings (exterior/interior)
- Bridges
- Infrastructure projects
- Concrete structures
- Steel frameworks

## Support

For issues or questions:
- Check the README.md for API documentation
- Review the troubleshooting section above
- Ensure all dependencies are correctly installed