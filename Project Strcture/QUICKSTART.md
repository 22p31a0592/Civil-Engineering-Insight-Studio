# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Step 2: Start Backend Server
```bash
python app.py
```
Backend will run on: http://localhost:5000

### Step 3: Install Frontend Dependencies (New Terminal)
```bash
cd frontend
npm install
```

### Step 4: Start Frontend Application
```bash
npm start
```
Frontend will open automatically on: http://localhost:3000

### Step 5: Use the Application

1. **Upload an Image:**
   - Drag and drop or click to select
   - Supported: PNG, JPG, JPEG, BMP, TIFF (Max 16MB)

2. **Select Analysis Type:**
   - Material Identification
   - Project Progress Documentation
   - Structural Analysis
   - Comprehensive Analysis

3. **Click "Start Analysis"**
   - Wait for processing (15-30 seconds)
   - View detailed results

## 📋 Example Scenarios

### Scenario 1: Material Identification
1. Upload image of building construction site
2. Select "Material Identification"
3. Get list of materials: concrete, steel, bricks with confidence scores

### Scenario 2: Project Progress
1. Upload image of ongoing construction
2. Select "Project Progress Documentation"
3. Get completion %, current phase, completed/planned elements

### Scenario 3: Structural Analysis
1. Upload image of bridge or building structure
2. Select "Structural Analysis"
3. Get details on beams, columns, trusses with dimensions

## 🔧 Troubleshooting

**Backend won't start:**
```bash
# Check Python version (needs 3.8+)
python --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Frontend won't start:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Analysis fails:**
- Check image file size (must be < 16MB)
- Verify image format (PNG, JPG, etc.)
- Ensure image shows clear construction elements

## 📊 Understanding Results

### Confidence Scores
- **>80%**: High confidence, reliable result
- **60-80%**: Moderate confidence, generally accurate
- **<60%**: Lower confidence, verify manually

### Material Properties
Each identified material includes:
- Name and confidence score
- Quantity (% of visible area)
- Location in structure
- Physical properties

### Structural Components
Each component includes:
- Type (beam, column, etc.)
- Material composition
- Dimensions in meters
- Construction method
- Condition assessment

## 🎯 Tips for Best Results

1. **Image Quality:**
   - Use high resolution (1920x1080 or better)
   - Ensure good lighting
   - Avoid heavily shadowed areas

2. **Image Content:**
   - Include clear view of structure
   - Minimize obstructions
   - Capture relevant structural elements

3. **Analysis Selection:**
   - Use specific analysis types when possible
   - Comprehensive analysis takes longer
   - Material ID is fastest

## 📚 Next Steps

- Read full [README.md](README.md) for architecture details
- Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for API reference
- Review [INSTALLATION.md](INSTALLATION.md) for detailed setup

## 🆘 Need Help?

Common questions:
- **Q:** How long does analysis take?
  **A:** Typically 15-30 seconds depending on image size

- **Q:** Can I analyze multiple images?
  **A:** Upload one at a time, repeat for multiple images

- **Q:** What image formats are supported?
  **A:** PNG, JPG, JPEG, BMP, TIFF

- **Q:** Is my data saved?
  **A:** Uploaded images are stored temporarily on server

- **Q:** Can I use this commercially?
  **A:** Check license terms for usage rights