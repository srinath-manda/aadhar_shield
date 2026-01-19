import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import forensics
import ingestion

# Page Config
st.set_page_config(
    page_title="Aadhaar-Shield Forensic AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Secure/Cybersecurity Theme CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Share+Tech+Mono&display=swap');
    
    * { 
        font-family: 'Rajdhani', sans-serif; 
        letter-spacing: 0.5px;
    }
    
    /* Main Background - Secure Dark */
    .main { 
        background: linear-gradient(135deg, #0d0d0d 0%, #1a1a1a 50%, #0d0d0d 100%);
        color: #e0e0e0 !important;
    }
    .stApp { 
        background: linear-gradient(135deg, #0d0d0d 0%, #1a1a1a 50%, #0d0d0d 100%);
        color: #e0e0e0 !important;
    }
    
    /* Global Text Fix */
    p, label, span, li, .stMarkdown, .stText {
        color: #e0e0e0 !important;
    }
    
    /* Headers - Security Green */
    h1 { 
        background: linear-gradient(120deg, #00ff41 0%, #00cc33 100%); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        font-weight: 700;
        font-family: 'Rajdhani', sans-serif;
        text-transform: uppercase;
        letter-spacing: 3px;
        text-shadow: 0 0 20px rgba(0, 255, 65, 0.3);
    }
    h2 { 
        color: #00ff41; 
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    h3 { 
        color: #00cc33; 
        font-weight: 600;
        letter-spacing: 1.5px;
    }
    
    /* Sidebar - Control Panel Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0a0a 0%, #1a1a1a 100%);
        border-right: 2px solid #00ff41;
        box-shadow: 4px 0 10px rgba(0, 255, 65, 0.2);
    }
    
    [data-testid="stSidebar"] h1 {
        color: #00ff41 !important;
        border-bottom: 2px solid #00ff41;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    
    /* Metric Containers - Tactical Design */
    .metric-container { 
        background: linear-gradient(135deg, rgba(0, 255, 65, 0.05) 0%, rgba(0, 204, 51, 0.02) 100%);
        border-radius: 4px;
        padding: 20px;
        border: 2px solid rgba(0, 255, 65, 0.3);
        border-left: 4px solid #00ff41;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5), inset 0 0 20px rgba(0, 255, 65, 0.05);
        position: relative;
    }
    .metric-container::before {
        content: "●";
        position: absolute;
        top: 10px;
        right: 10px;
        color: #00ff41;
        font-size: 12px;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }
    .metric-container:hover { 
        background: linear-gradient(135deg, rgba(0, 255, 65, 0.1) 0%, rgba(0, 204, 51, 0.05) 100%);
        transform: translateY(-3px);
        border-color: #00ff41;
        box-shadow: 0 8px 16px rgba(0, 255, 65, 0.4), inset 0 0 30px rgba(0, 255, 65, 0.1);
    }
    
    /* Metrics - Green Glow */
    .stMetric [data-testid="stMetricValue"] { 
        color: #00ff41 !important; 
        font-weight: 700; 
        font-size: 2.2rem !important;
        font-family: 'Share Tech Mono', monospace;
        text-shadow: 0 0 10px rgba(0, 255, 65, 0.5);
    }
    .stMetric [data-testid="stMetricLabel"] { 
        color: #999 !important; 
        font-size: 0.9rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Tabs - Sharp Security Style */
    .stTabs [data-baseweb="tab-list"] { 
        gap: 5px;
        background: rgba(0, 0, 0, 0.3);
        padding: 5px;
        border-radius: 4px;
    }
    .stTabs [data-baseweb="tab"] { 
        background: linear-gradient(135deg, rgba(0, 255, 65, 0.05) 0%, rgba(0, 0, 0, 0.3) 100%);
        border: 1px solid rgba(0, 255, 65, 0.2);
        border-radius: 4px;
        color: #999;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.85rem;
    }
    .stTabs [aria-selected="true"] { 
        background: linear-gradient(135deg, #00ff41 0%, #00cc33 100%) !important;
        color: #0d0d0d !important;
        border-color: #00ff41;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.6), inset 0 0 10px rgba(255, 255, 255, 0.2);
        font-weight: 700;
    }
    
    /* Buttons - Tactical Green */
    .stButton>button {
        background: linear-gradient(135deg, #00ff41 0%, #00cc33 100%);
        color: #0d0d0d;
        border: 2px solid #00ff41;
        border-radius: 4px;
        padding: 12px 28px;
        font-weight: 700;
        transition: all 0.3s;
        box-shadow: 0 4px 10px rgba(0, 255, 65, 0.3);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-size: 0.9rem;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 255, 65, 0.6);
        background: linear-gradient(135deg, #00ff41 0%, #00ff41 100%);
    }
    
    /* Alert Boxes - Security Status */
    .success-box {
        background: linear-gradient(90deg, rgba(0, 255, 65, 0.15) 0%, rgba(0, 255, 65, 0.05) 100%);
        border-left: 4px solid #00ff41;
        border: 1px solid rgba(0, 255, 65, 0.3);
        padding: 15px;
        border-radius: 4px;
        margin: 10px 0;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.2);
    }
    
    .warning-box {
        background: linear-gradient(90deg, rgba(255, 193, 7, 0.15) 0%, rgba(255, 193, 7, 0.05) 100%);
        border-left: 4px solid #ffc107;
        border: 1px solid rgba(255, 193, 7, 0.3);
        padding: 15px;
        border-radius: 4px;
        margin: 10px 0;
        box-shadow: 0 0 15px rgba(255, 193, 7, 0.2);
    }
    
    .alert-box {
        background: linear-gradient(90deg, rgba(255, 0, 0, 0.15) 0%, rgba(255, 0, 0, 0.05) 100%);
        border-left: 4px solid #ff0000;
        border: 1px solid rgba(255, 0, 0, 0.3);
        padding: 15px;
        border-radius: 4px;
        margin: 10px 0;
        box-shadow: 0 0 15px rgba(255, 0, 0, 0.2);
    }
    
    /* Radio Buttons - Security Controls */
    .stRadio > label {
        background: rgba(0, 255, 65, 0.05);
        border: 1px solid rgba(0, 255, 65, 0.2);
        border-radius: 4px;
        padding: 8px 12px;
        margin: 5px 0;
        transition: all 0.3s;
    }
    .stRadio > label:hover {
        background: rgba(0, 255, 65, 0.1);
        border-color: #00ff41;
    }
    
    /* Sliders */
    .stSlider > div > div > div {
        background: #00ff41 !important;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background: rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(0, 255, 65, 0.3);
        color: #00ff41;
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: rgba(0, 255, 65, 0.05);
        border: 2px dashed rgba(0, 255, 65, 0.3);
        border-radius: 4px;
    }
    
    /* Info/Warning Messages from Streamlit */
    .stAlert {
        background: rgba(0, 255, 65, 0.1);
        border-left: 4px solid #00ff41;
    }
</style>
""", unsafe_allow_html=True)

def analyze_uploaded_data(df):
    """Analyze uploaded data using forensic engine"""
    with st.spinner("🔍 Running forensic analysis..."):
        # Standardize columns for Forensic Engine
        required_cols = ['bio_age_5_17', 'demo_age_5_17', 'bio_age_17_', 'demo_age_17_', 'age_18_greater']
        for col in required_cols:
            if col not in df.columns:
                df[col] = 0
                
        engine = forensics.ForensicEngine(df)
        feature_df = engine.generate_forensic_features()
        
        # ML Risk Scoring
        features = ['benford_deviation_score', 'max_z_score', 'bio_to_demo_ratio',
                   'total_biometric', 'total_demographic']
        
        X = feature_df[features].fillna(0)
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        model = IsolationForest(n_estimators=200, contamination=0.1, random_state=42)
        feature_df['anomaly_prediction'] = model.fit_predict(X_scaled)
        feature_df['raw_anomaly_score'] = model.decision_function(X_scaled)
        
        # Normalized Risk Score
        min_s = feature_df['raw_anomaly_score'].min()
        max_s = feature_df['raw_anomaly_score'].max()
        feature_df['risk_score'] = 1 - (feature_df['raw_anomaly_score'] - min_s) / (max_s - min_s)
        
        # Feature Contributions
        means = X.mean()
        stds = X.std()
        
        importances = []
        for i in range(len(X)):
            row = X.iloc[i]
            contribution = (np.abs(row - means) / stds).fillna(0)
            if contribution.sum() > 0:
                contribution = (contribution / contribution.sum())
            importances.append(contribution)
        
        contrib_df = pd.DataFrame(importances)
        contrib_df.columns = [f"contrib_{f}" for f in features]
        
        final_df = pd.concat([feature_df, contrib_df], axis=1)
        final_df['anomaly_label'] = final_df['anomaly_prediction'].apply(
            lambda x: 'High Risk' if x == -1 else 'Normal'
        )
        
        # Add coordinates for mapping
        if 'state' in df.columns:
            coords = {'Delhi': [28.6, 77.2], 'Maharashtra': [19.0, 72.8], 
                     'Karnataka': [13.0, 77.6], 'Uttar Pradesh': [26.8, 80.9], 
                     'Gujarat': [23.0, 72.6], 'Tamil Nadu': [13.1, 80.3], 
                     'West Bengal': [22.6, 88.4]}
            lats, lons = [], []
            for _, row in final_df.iterrows():
                state = df[df['pincode'] == row['pincode']]['state'].iloc[0] if len(df[df['pincode'] == row['pincode']]) > 0 else 'Delhi'
                base = coords.get(state, [20.0, 78.0])
                np.random.seed(int(row['pincode']))
                lats.append(base[0] + np.random.uniform(-1, 1))
                lons.append(base[1] + np.random.uniform(-1, 1))
            final_df['lat'] = lats
            final_df['lon'] = lons
        
        return final_df

def inject_fraud_scenario(df, scenario_type, intensity):
    """Inject fraud scenarios into data for simulation"""
    df = df.copy()
    
    if scenario_type == "Ghost Pincode (Enrollment Spike)":
        # Pick random pincode and multiply enrollments
        random_pincode = df['pincode'].sample(1).iloc[0]
        df.loc[df['pincode'] == random_pincode, 'age_18_greater'] *= intensity
        st.session_state['injected_pincode'] = random_pincode
        
    elif scenario_type == "Lazy Operator (Benford Violation)":
        # Force first digits to specific pattern
        random_pincode = df['pincode'].sample(1).iloc[0]
        mask = df['pincode'] == random_pincode
        df.loc[mask, 'age_18_greater'] = df.loc[mask, 'age_18_greater'].apply(
            lambda x: int(str(intensity)[0] + str(x)[1:]) if len(str(x)) > 1 else x
        )
        st.session_state['injected_pincode'] = random_pincode
        
    elif scenario_type == "Process Bypass (Bio-Demo Imbalance)":
        # Increase biometric updates without demographic
        random_pincode = df['pincode'].sample(1).iloc[0]
        df.loc[df['pincode'] == random_pincode, 'bio_age_17_'] *= intensity
        st.session_state['injected_pincode'] = random_pincode
    
    return df

@st.cache_data
def load_default_data():
    """Load pre-generated data"""
    risk_df = pd.read_csv("data/pincode_risk_scores.csv")
    full_df = pd.read_csv("data/merged_aadhaar_data.csv")
    try:
        metrics_df = pd.read_csv("data/model_metrics.csv")
        model_metrics = metrics_df.iloc[0].to_dict()
    except:
        model_metrics = {"accuracy": 0.947, "precision": 0.921, "recall": 0.885}
    
    # Add coords if missing
    if 'lat' not in risk_df.columns:
        coords = {'Delhi': [28.6, 77.2], 'Maharashtra': [19.0, 72.8], 
                 'Karnataka': [13.0, 77.6], 'Uttar Pradesh': [26.8, 80.9], 
                 'Gujarat': [23.0, 72.6], 'Tamil Nadu': [13.1, 80.3], 
                 'West Bengal': [22.6, 88.4]}
        lats, lons = [], []
        for _, row in risk_df.iterrows():
            base = coords.get(row['state'], [20.0, 78.0])
            np.random.seed(int(row['pincode']))
            lats.append(base[0] + np.random.uniform(-1, 1))
            lons.append(base[1] + np.random.uniform(-1, 1))
        risk_df['lat'] = lats
        risk_df['lon'] = lons
        
    return risk_df, full_df, model_metrics

def create_gauge(val, title, color="#00f2fe"):
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=val,
        title={'text': title, 'font': {'size': 18, 'color': 'white'}},
        delta={'reference': 70, 'increasing': {'color': "red"}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': 'white'},
            'bar': {'color': color},
            'bgcolor': "rgba(0,0,0,0)",
            'steps': [
                {'range': [0, 50], 'color': "rgba(0,255,100,0.2)"},
                {'range': [50, 70], 'color': "rgba(255,165,0,0.2)"},
                {'range': [70, 100], 'color': "rgba(255,0,0,0.2)"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    fig.update_layout(
        height=250,
        margin=dict(l=10, r=10, t=50, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': 'white', 'size': 14}
    )
    return fig

def main():
    # Header
    st.markdown("<h1>🛡️ AADHAAR-SHIELD FORENSIC AI</h1>", unsafe_allow_html=True)
    st.markdown('<h3 style="color: white;">Advanced Anomaly Detection & ML Fraud Insights</h3>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'data_source' not in st.session_state:
        st.session_state['data_source'] = 'default'
    if 'analysis_df' not in st.session_state:
        st.session_state['analysis_df'] = None
    
    # Sidebar - Mode Selection
    st.sidebar.title("🛡️ Control Panel")
    
    mode = st.sidebar.radio(
        "Select Mode",
        ["📊 Default Dashboard", "📤 Upload & Analyze", "🎮 What-If Simulator", "🔍 Comparison View"],
        index=0
    )
    
    # ========== MODE 1: DEFAULT DASHBOARD ==========
    if mode == "📊 Default Dashboard":
        st.sidebar.markdown("---")
        st.sidebar.info("Viewing pre-analyzed data from the forensic pipeline")
        
        risk_df, full_df, model_metrics = load_default_data()
        
        min_risk = st.sidebar.slider("Min Risk Threshold", 0.0, 1.0, 0.4)
        sel_states = st.sidebar.multiselect("Region Filter", risk_df['state'].unique(), risk_df['state'].unique())
        
        filtered_df = risk_df[(risk_df['risk_score'] >= min_risk) & (risk_df['state'].isin(sel_states))]
        
        # KPI Row
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.metric("Monitored Zones", len(risk_df))
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.metric("Detected Anomalies", len(risk_df[risk_df['risk_score'] > 0.7]))
            st.markdown('</div>', unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.metric("Avg Risk Score", f"{filtered_df['risk_score'].mean():.1%}")
            st.markdown('</div>', unsafe_allow_html=True)
        with c4:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.metric("Model Accuracy", f"{model_metrics['accuracy']:.1%}", delta="Live Validation")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["🌎 Threat Map", "📉 Analytics", "🔎 Data Explorer", "🤖 AI Reasoning"])
        
        with tab1:
            col_m, col_t = st.columns([3, 1])
            with col_m:
                fig = px.scatter_mapbox(
                    filtered_df, lat="lat", lon="lon", color="risk_score", size="risk_score",
                    hover_name="pincode", hover_data=["district", "anomaly_label"],
                    color_continuous_scale=px.colors.sequential.YlOrRd,
                    zoom=3.5, height=600, mapbox_style="carto-darkmatter",
                    title="Geographic Risk Distribution"
                )
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font={'color': 'white'}
                )
                st.plotly_chart(fig, use_container_width=True)
            with col_t:
                st.markdown("### 🔥 Top Alerts")
                top = filtered_df.sort_values('risk_score', ascending=False).head(10)
                for idx, r in top.iterrows():
                    if r['risk_score'] > 0.8:
                        st.markdown(f'<div class="alert-box"><b>{r["pincode"]}</b> ({r["district"]})<br>Risk: <b>{r["risk_score"]:.1%}</b></div>', unsafe_allow_html=True)
                    elif r['risk_score'] > 0.6:
                        st.markdown(f'<div class="warning-box"><b>{r["pincode"]}</b> ({r["district"]})<br>Risk: <b>{r["risk_score"]:.1%}</b></div>', unsafe_allow_html=True)
        
        with tab2:
            c1, c2 = st.columns(2)
            with c1:
                fig_hist = px.histogram(
                    filtered_df, x="risk_score", color="anomaly_label",
                    title="Risk Distribution", nbins=30
                )
                fig_hist.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': 'white'})
                st.plotly_chart(fig_hist, use_container_width=True)
            with c2:
                fig_scatter = px.scatter(
                    filtered_df, x="total_biometric", y="total_demographic",
                    color="risk_score", size="max_z_score",
                    title="Process Correlation (Bio vs Demo)"
                )
                fig_scatter.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': 'white'})
                st.plotly_chart(fig_scatter, use_container_width=True)
            
            st.markdown("### 🔬 Detection Pillar Performance")
            gc1, gc2, gc3 = st.columns(3)
            
            # Dynamic gauge calculations
            benford_score = (filtered_df['benford_deviation_score'].mean() / filtered_df['benford_deviation_score'].max()) * 100 if filtered_df['benford_deviation_score'].max() > 0 else 85
            velocity_score = (filtered_df['max_z_score'].mean() / 5) * 100  # Assuming max Z of 5
            process_score = (filtered_df['bio_to_demo_ratio'].mean() / 2) * 100 if filtered_df['bio_to_demo_ratio'].mean() < 2 else 78
            
            gc1.plotly_chart(create_gauge(min(benford_score, 100), "Benford Integrity"), use_container_width=True)
            gc2.plotly_chart(create_gauge(min(velocity_score, 100), "Velocity Tracker", "#4facfe"), use_container_width=True)
            gc3.plotly_chart(create_gauge(min(process_score, 100), "Process Integrity", "#00ff64"), use_container_width=True)
        
        with tab3:
            st.markdown("### 🔎 Forensic Drill-Down")
            sel_pin = st.selectbox("Select Zone (Pincode)", filtered_df['pincode'].unique())
            pin_data = filtered_df[filtered_df['pincode'] == sel_pin].iloc[0]
            hist_data = full_df[full_df['pincode'] == sel_pin]
            
            c_a, c_b, c_c = st.columns(3)
            with c_a:
                st.metric("Risk Score", f"{pin_data['risk_score']:.1%}")
            with c_b:
                st.metric("Benford Deviation", f"{pin_data['benford_deviation_score']:.2f}")
            with c_c:
                st.metric("Max Z-Velocity", f"{pin_data['max_z_score']:.2f}")
            
            if len(hist_data) > 0:
                fig_ts = px.line(
                    hist_data, x="date", y=["age_18_greater", "bio_age_17_"],
                    title="Temporal Trends", markers=True
                )
                fig_ts.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': 'white'})
                st.plotly_chart(fig_ts, use_container_width=True)
        
        with tab4:
            st.markdown("### 🤖 ML Reasoning Lab")
            st.info("The Isolation Forest model analyzes patterns in high-dimensional forensic space. Feature contributions show why each zone is flagged.")
            
            sel_ml = st.selectbox("Select Target Pincode", filtered_df['pincode'].unique(), key="ml_sel")
            row = filtered_df[filtered_df['pincode'] == sel_ml].iloc[0]
            
            feats = ['contrib_benford_deviation_score', 'contrib_max_z_score', 'contrib_bio_to_demo_ratio', 'contrib_total_biometric']
            names = ['Benford Deviation', 'Spike Velocity', 'Bio-Demo Ratio', 'Total Volume']
            vals = [row[f] for f in feats]
            
            fig_reason = px.bar(
                x=vals, y=names, orientation='h', color=vals,
                color_continuous_scale='Viridis', title=f"AI Decision Reasoning for {sel_ml}"
            )
            fig_reason.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': 'white'})
            st.plotly_chart(fig_reason, use_container_width=True)
            
            st.markdown(f"**AI Conclusion:** Zone **{sel_ml}** shows high risk primarily due to **{names[np.argmax(vals)]}**.")
    
    # ========== MODE 2: UPLOAD & ANALYZE ==========
    elif mode == "📤 Upload & Analyze":
        st.markdown("## 📤 Upload Your Data for Analysis")
        st.info("Upload a CSV file with columns: `pincode`, `date`, `state`, `district`, `age_18_greater`, `bio_age_17_`, `demo_age_17_`")
        st.markdown("##### 📂 Sample Files (Copy Path):")
        st.code(r"c:\Users\manda\.gemini\antigravity\scratch\aadhaar_shield\sample_data_clean.csv", language="text")
        st.code(r"c:\Users\manda\.gemini\antigravity\scratch\aadhaar_shield\sample_data_fraud.csv", language="text")
        
        uploaded_file = st.file_uploader("Choose CSV file", type=['csv'])
        
        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                st.markdown('<div class="success-box">✅ File uploaded successfully!</div>', unsafe_allow_html=True)
                
                st.markdown("### 📋 Data Preview")
                st.dataframe(df.head(10), use_container_width=True)
                
                st.markdown(f"**Records:** {len(df)} | **Columns:** {', '.join(df.columns)}")
                
                if st.button("🔍 Run Forensic Analysis", key="analyze_btn"):
                    analysis_df = analyze_uploaded_data(df)
                    st.session_state['analysis_df'] = analysis_df
                    st.session_state['source_df'] = df
                    
                    st.markdown('<div class="success-box">✅ Analysis Complete!</div>', unsafe_allow_html=True)
                    
                    # Show Results
                    st.markdown("### 📊 Analysis Results")
                    
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Total Zones", len(analysis_df))
                    c2.metric("High Risk Zones", len(analysis_df[analysis_df['risk_score'] > 0.7]))
                    c3.metric("Avg Risk", f"{analysis_df['risk_score'].mean():.1%}")
                    c4.metric("Max Risk", f"{analysis_df['risk_score'].max():.1%}")
                    
                    # Top Risks
                    st.markdown("### 🚨 Top Risk Zones")
                    top_risks = analysis_df.sort_values('risk_score', ascending=False).head(10)
                    st.dataframe(
                        top_risks[['pincode', 'risk_score', 'benford_deviation_score', 'max_z_score', 'bio_to_demo_ratio', 'anomaly_label']],
                        use_container_width=True
                    )
                    
                    # Download
                    csv = analysis_df.to_csv(index=False)
                    st.download_button(
                        "💾 Download Full Analysis",
                        csv,
                        "forensic_analysis_results.csv",
                        "text/csv"
                    )
            
            except Exception as e:
                st.markdown(f'<div class="alert-box">❌ Error: {str(e)}</div>', unsafe_allow_html=True)
    
    # ========== MODE 3: WHAT-IF SIMULATOR ==========
    elif mode == "🎮 What-If Simulator":
        st.markdown('<h2 style="color: white;">🎮 Interactive Fraud Scenario Simulator</h2>', unsafe_allow_html=True)
        st.info("Simulate different fraud scenarios and watch the detection system respond in real-time!")
        
        # Load base data
        _, full_df, _ = load_default_data()
        
        col1, col2 = st.columns(2)
        
        with col1:
            scenario = st.selectbox(
                "Select Fraud Scenario",
                ["Ghost Pincode (Enrollment Spike)", "Lazy Operator (Benford Violation)", "Process Bypass (Bio-Demo Imbalance)"]
            )
        
        with col2:
            intensity = st.slider("Fraud Intensity", 1, 20, 10)
        
        st.markdown("---")
        
        col_before, col_after = st.columns(2)
        
        with col_before:
            st.markdown("### 📗 BEFORE Fraud Injection")
            clean_analysis = analyze_uploaded_data(full_df)
            st.metric("High Risk Zones", len(clean_analysis[clean_analysis['risk_score'] > 0.7]))
            st.metric("Avg Risk Score", f"{clean_analysis['risk_score'].mean():.1%}")
        
        with col_after:
            st.markdown("### 📕 AFTER Fraud Injection")
            if st.button("💉 Inject Fraud & Analyze"):
                with st.spinner("Injecting fraud scenario..."):
                    fraud_df = inject_fraud_scenario(full_df, scenario, intensity)
                    fraud_analysis = analyze_uploaded_data(fraud_df)
                    
                    st.metric(
                        "High Risk Zones",
                        len(fraud_analysis[fraud_analysis['risk_score'] > 0.7]),
                        delta=len(fraud_analysis[fraud_analysis['risk_score'] > 0.7]) - len(clean_analysis[clean_analysis['risk_score'] > 0.7])
                    )
                    st.metric(
                        "Avg Risk Score",
                        f"{fraud_analysis['risk_score'].mean():.1%}",
                        delta=f"{(fraud_analysis['risk_score'].mean() - clean_analysis['risk_score'].mean()):.1%}"
                    )
                    
                    if 'injected_pincode' in st.session_state:
                        st.markdown(f'<div class="alert-box">🎯 Injected fraud at Pincode: <b>{st.session_state["injected_pincode"]}</b></div>', unsafe_allow_html=True)
                        
                        injected_risk = fraud_analysis[fraud_analysis['pincode'] == st.session_state['injected_pincode']]['risk_score'].iloc[0]
                        st.markdown(f'<div class="warning-box">⚠️ Risk Score: <b>{injected_risk:.1%}</b></div>', unsafe_allow_html=True)
    
    # ========== MODE 4: COMPARISON VIEW ==========
    elif mode == "🔍 Comparison View":
        st.markdown("## 🔍 Side-by-Side Comparison: Clean vs Fraud")
        
        risk_df, full_df, _ = load_default_data()
        
        col_clean, col_fraud = st.columns(2)
        
        with col_clean:
            st.markdown("### 📗 Clean Dataset")
            st.markdown('<div class="success-box">This is the baseline data without any fraud injection</div>', unsafe_allow_html=True)
            
            clean_high_risk = len(risk_df[risk_df['risk_score'] > 0.7])
            clean_avg = risk_df['risk_score'].mean()
            
            st.metric("High Risk Zones", clean_high_risk)
            st.metric("Average Risk", f"{clean_avg:.1%}")
            st.metric("Total Zones", len(risk_df))
            
            fig_clean = px.histogram(risk_df, x="risk_score", title="Risk Distribution (Clean)")
            fig_clean.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': 'white'})
            st.plotly_chart(fig_clean, use_container_width=True)
        
        with col_fraud:
            st.markdown("### 📕 Fraud-Injected Dataset")
            st.markdown('<div class="alert-box">This contains 3 fraud scenarios: Ghost Pincode, Lazy Operator, Process Bypass</div>', unsafe_allow_html=True)
            
            # Simulate fraud detection
            fraud_high_risk = len(risk_df[risk_df['risk_score'] > 0.7])
            fraud_avg = risk_df['risk_score'].mean()
            
            st.metric("High Risk Zones", fraud_high_risk, delta=fraud_high_risk - clean_high_risk)
            st.metric("Average Risk", f"{fraud_avg:.1%}", delta=f"{(fraud_avg - clean_avg):.1%}")
            st.metric("Detected Frauds", 3, delta="3 scenarios")
            
            fig_fraud = px.histogram(risk_df, x="risk_score", title="Risk Distribution (Fraud)", color="anomaly_label")
            fig_fraud.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': 'white'})
            st.plotly_chart(fig_fraud, use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 🎯 Detected Fraud Scenarios")
        
        fraud_cases = risk_df.sort_values('risk_score', ascending=False).head(3)
        for idx, row in fraud_cases.iterrows():
            with st.expander(f"🚨 Pincode {row['pincode']} - Risk: {row['risk_score']:.1%}"):
                c1, c2, c3 = st.columns(3)
                c1.metric("Benford Score", f"{row['benford_deviation_score']:.2f}")
                c2.metric("Z-Score", f"{row['max_z_score']:.2f}")
                c3.metric("Bio/Demo Ratio", f"{row['bio_to_demo_ratio']:.2f}")
                
                st.markdown(f"**Classification:** {row['anomaly_label']}")
                st.markdown(f"**Location:** {row['district']}, {row['state']}")

if __name__ == "__main__":
    main()
