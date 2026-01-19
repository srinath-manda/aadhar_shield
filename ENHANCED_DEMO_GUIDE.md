# 🚀 Quick Start Guide - Enhanced Demo

## What Changed?

Your app now has **4 POWERFUL MODES** instead of just 1 static dashboard!

### New Features:
1. **📊 Default Dashboard** - Improved UI with better styling
2. **📤 Upload & Analyze** - Upload ANY CSV and get instant analysis
3. **🎮 What-If Simulator** - Inject fraud scenarios interactively
4. **🔍 Comparison View** - See clean vs fraud side-by-side

---

## How to Run

```bash
cd c:\Users\manda\.gemini\antigravity\scratch\aadhaar_shield
streamlit run src\app_enhanced.py
```

The app will open at: **http://localhost:8501**

---

## Demo Flow for Video

### 1. Start with Default Dashboard (1 min)
- Show the threat map
- Show analytics gauges
- Show AI reasoning for a pincode

### 2. Upload & Analyze - THE MONEY SHOT (2 min)
**First upload (Clean Data):**
- Click sidebar → "📤 Upload & Analyze"
- Upload `sample_data_clean.csv`
- Click "Run Forensic Analysis"
- Show low risk (30-40% avg)

**Second upload (Fraud Data):**
- Upload `sample_data_fraud.csv`  
- Click "Run Forensic Analysis"
- Show high risk detected (pincode 999999 at 90%+)
- **This proves it's not hardcoded!**

### 3. What-If Simulator (1.5 min)
- Click sidebar → "🎮 What-If Simulator"
- Select "Ghost Pincode" scenario
- Set intensity to 15
- Click "Inject Fraud & Analyze"
- Show before/after comparison

### 4. Comparison View (1 min)
- Click sidebar → "🔍 Comparison View"
- Show clean vs fraud side-by-side
- Expand detected fraud cases

---

## Sample Files Location

- `sample_data_clean.csv` - Normal, legitimate data
- `sample_data_fraud.csv` - Contains fraud at pincode 999999

Both files are in the project root directory.

---

## Key Talking Points

✅ **"This is DYNAMIC, not static"** - Upload & Analyze proves it
✅ **"Real-time analysis"** - Loading spinners show processing
✅ **"Works on ANY dataset"** - Not limited to our test data
✅ **"Interactive testing"** - What-If Simulator
✅ **"AI explainability"** - Feature contributions shown

---

## Recording Tips

1. **Full screen browser** (F11)
2. **Close other tabs**
3. **Turn off notifications**
4. **Test upload files BEFORE recording**
5. **Speak confidently** - this is production-ready!

---

## If You Need to Go Back to Old Version

```bash
streamlit run src\app.py
```

But DON'T! The enhanced version is WAY better for demos! 🎯
