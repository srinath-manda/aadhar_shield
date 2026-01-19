# 🎯 Quick Start Guide

## Installation (1 minute)
```bash
pip install -r requirements.txt
```

## Run Everything (2 minutes)
```bash
# Generate data + Run analysis
python src/data_generator.py
python src/ingestion.py
python src/forensics.py
python src/anomaly_detection.py

# Launch dashboard
streamlit run src/app.py
```

Dashboard opens at: `http://localhost:8501`

## What You'll See
- 🗺️ **Interactive Heatmap** of fraud risk zones
- 📊 **Real-time metrics** and analytics
- 🔍 **Deep-dive** into suspicious Pincodes
- 📄 **Export reports** instantly

## Key Files
- `README.md` - Full project documentation
- `PRESENTATION_GUIDE.md` - Hackathon pitch script
- `src/app.py` - Premium dashboard
- `data/pincode_risk_scores.csv` - ML output

## Detected Fraud (Demo Data)
✓ Ghost Pincode 993133 - Risk: 100%
✓ Lazy Operator 941000 - Risk: 73%  
✓ Mobile Farmer 991660 - Risk: 65%

**For judges: See PRESENTATION_GUIDE.md for demo script!**
