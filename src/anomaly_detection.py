import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import ingestion
import forensics
import os

def train_with_explainability():
    """
    Trains Isolation Forest and calculates feature importance for explainability.
    """
    print("Gathering features for ML Layer...")
    df = ingestion.load_and_merge_data()
    
    # Use the Advanced Forensic Engine to get features
    engine = forensics.ForensicEngine(df)
    feature_df = engine.generate_forensic_features()
    
    # Feature columns for ML
    features = [
        'benford_deviation_score', 'max_z_score', 'bio_to_demo_ratio',
        'total_biometric', 'total_demographic'
    ]
    
    # Filter and Scale
    X = feature_df[features].fillna(0)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    print("Training Anomaly Detection Model (Isolation Forest)...")
    model = IsolationForest(n_estimators=200, contamination=0.1, random_state=42)
    feature_df['anomaly_prediction'] = model.fit_predict(X_scaled)
    
    # Raw anomaly score (lower is more anomalous)
    feature_df['raw_anomaly_score'] = model.decision_function(X_scaled)
    
    # Normalized Risk Score (0 to 1)
    min_s = feature_df['raw_anomaly_score'].min()
    max_s = feature_df['raw_anomaly_score'].max()
    feature_df['risk_score'] = 1 - (feature_df['raw_anomaly_score'] - min_s) / (max_s - min_s)
    
    # --- ML Explainability (Pseudo-Feature Importance) ---
    # For Isolation Forest, we can estimate importance by seeing how much 
    # each feature contributes to the anomaly score per record.
    # Simple heuristic: Feature absolute deviation from mean.
    
    means = X.mean()
    stds = X.std()
    
    importances = []
    for i in range(len(X)):
        row = X.iloc[i]
        # Calculate contribution: (abs(row - mean) / std) 
        # This highlights which feature is "out of range"
        contribution = (np.abs(row - means) / stds).fillna(0)
        # Normalize contributions to sum to 100%
        if contribution.sum() > 0:
            contribution = (contribution / contribution.sum())
        importances.append(contribution)
        
    contrib_df = pd.DataFrame(importances)
    contrib_df.columns = [f"contrib_{f}" for f in features]
    
    # Final Result
    final_df = pd.concat([feature_df, contrib_df], axis=1)
    
    # Final Labeling
    final_df['anomaly_label'] = final_df['anomaly_prediction'].apply(lambda x: 'High Risk' if x == -1 else 'Normal')
    
    # Find State/District (join back from original)
    metadata = df[['pincode', 'state', 'district']].drop_duplicates(subset=['pincode'])
    final_df = final_df.merge(metadata, on='pincode', how='left')
    
    # --- DYNAMIC ACCURACY CALCULATION ---
    metrics = {"accuracy": 0, "precision": 0, "recall": 0}
    try:
        ground_truth = pd.read_csv("data/ground_truth_labels.csv")
        ground_truth['pincode'] = ground_truth['pincode'].astype(str)
        final_df['pincode'] = final_df['pincode'].astype(str)
        
        val_df = final_df.merge(ground_truth, on='pincode')
        
        y_true = val_df['is_fraud'].astype(int)
        y_pred = (val_df['risk_score'] > 0.7).astype(int)
        
        from sklearn.metrics import accuracy_score, precision_score, recall_score
        metrics['accuracy'] = accuracy_score(y_true, y_pred)
        metrics['precision'] = precision_score(y_true, y_pred, zero_division=0)
        metrics['recall'] = recall_score(y_true, y_pred, zero_division=0)
        
        print("\n" + "="*40)
        print("MODEL VALIDATION METRICS (DYNAMIC)")
        print(f"Accuracy:  {metrics['accuracy']:.2%}")
        print(f"Precision: {metrics['precision']:.2%}")
        print(f"Recall:    {metrics['recall']:.2%}")
        print("="*40)
        
        # Save metrics for dashboard
        pd.DataFrame([metrics]).to_csv("data/model_metrics.csv", index=False)
        
    except Exception as e:
        print(f"Warning: Could not calculate accuracy: {e}")

    output_path = "data/pincode_risk_scores.csv"
    final_df.to_csv(output_path, index=False)
    print(f"[OK] ML scoring complete. Results (including explainability) saved to {output_path}")
    
    return final_df

if __name__ == "__main__":
    train_with_explainability()
