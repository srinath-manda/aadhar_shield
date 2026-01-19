import pandas as pd
import numpy as np
import scipy.stats as stats
import math

class ForensicEngine:
    def __init__(self, data):
        self.data = data.copy()
        self.features = pd.DataFrame()

    def calculate_benford_score(self, column_name):
        """
        Pillar A: Statistical Integrity (Benford's Law with Chi-Square)
        Formula: χ² = Σ (Observed - Expected)² / Expected
        Returns a score where higher = more suspicious
        """
        print(f"Calculating Benford Deviation Scores for {column_name}...")
        
        # Benford's Law expected distribution
        benford_expected = {
            1: 0.301, 2: 0.176, 3: 0.125, 4: 0.097, 5: 0.079,
            6: 0.067, 7: 0.058, 8: 0.051, 9: 0.046
        }
        
        results = []
        pincodes = self.data['pincode'].unique()
        
        for pincode in pincodes:
            pin_data = self.data[self.data['pincode'] == pincode][column_name]
            
            # Extract leading digits
            leading_digits = [int(str(int(x))[0]) for x in pin_data if x > 0]
            
            if len(leading_digits) < 5:  # Need minimum sample
                results.append({
                    'pincode': pincode,
                    'benford_deviation_score': 0,
                    'benford_flag': False
                })
                continue
            
            # Count observed frequencies
            observed_counts = {d: leading_digits.count(d) for d in range(1, 10)}
            total = len(leading_digits)
            
            # Calculate Chi-Square
            chi_square = 0
            for digit in range(1, 10):
                expected_count = benford_expected[digit] * total
                observed_count = observed_counts[digit]
                if expected_count > 0:
                    chi_square += ((observed_count - expected_count) ** 2) / expected_count
            
            # Chi-square critical value at p=0.05 with 8 df ≈ 15.51
            # Normalize to 0-1 scale for Risk Score
            benford_score = min(chi_square / 20, 1.0)  # Scale it
            is_suspicious = chi_square > 15.51
            
            results.append({
                'pincode': pincode,
                'benford_deviation_score': benford_score,
                'benford_chi_square': chi_square,
                'benford_flag': is_suspicious
            })
        
        benford_df = pd.DataFrame(results)
        print(f"  Flagged {benford_df['benford_flag'].sum()} Pincodes with Benford violations")
        return benford_df

    def calculate_velocity_score(self, column_name):
        """
        Pillar B: Temporal Velocity (Z-Score Analysis)
        Formula: Z = (x_current - μ_historical) / σ_historical
        Returns Z-scores for each Pincode-Month
        """
        print(f"Calculating Z-Score Velocity for {column_name}...")
        
        # Calculate Z-scores per Pincode
        self.data['z_score_velocity'] = self.data.groupby('pincode')[column_name].transform(
            lambda x: stats.zscore(x, nan_policy='omit')
        )
        
        # Replace NaN with 0
        self.data['z_score_velocity'] = self.data['z_score_velocity'].fillna(0)
        
        # Aggregate max Z-score per Pincode (worst case)
        velocity_df = self.data.groupby('pincode').agg({
            'z_score_velocity': ['max', 'mean']
        }).reset_index()
        
        velocity_df.columns = ['pincode', 'max_z_score', 'avg_z_score']
        velocity_df['velocity_flag'] = velocity_df['max_z_score'] > 3.0
        
        print(f"  Flagged {velocity_df['velocity_flag'].sum()} Pincodes with velocity spikes")
        return velocity_df

    def calculate_bio_to_demo_ratio(self):
        """
        Pillar C: Process Bypass Detection (Bio-to-Demo Ratio)
        Formula: Ratio = Count_Biometric / Count_Demographic
        High ratio suggests biometric-only farming to keep fake accounts active
        """
        print("Calculating Bio-to-Demo Ratios...")
        
        # Sum biometric and demographic updates per Pincode
        self.data['total_biometric'] = self.data['bio_age_5_17'] + self.data['bio_age_17_']
        self.data['total_demographic'] = self.data['demo_age_5_17'] + self.data['demo_age_17_']
        
        ratio_df = self.data.groupby('pincode').agg({
            'total_biometric': 'sum',
            'total_demographic': 'sum'
        }).reset_index()
        
        # Calculate ratio (avoid division by zero)
        ratio_df['bio_to_demo_ratio'] = np.where(
            ratio_df['total_demographic'] > 0,
            ratio_df['total_biometric'] / ratio_df['total_demographic'],
            0
        )
        
        # Flag if ratio > 50:1 (as per requirement)
        ratio_df['bypass_flag'] = ratio_df['bio_to_demo_ratio'] > 50
        
        print(f"  Flagged {ratio_df['bypass_flag'].sum()} Pincodes with process bypass patterns")
        return ratio_df[['pincode', 'bio_to_demo_ratio', 'total_biometric', 'total_demographic', 'bypass_flag']]

    def generate_forensic_features(self, enrolment_column='age_18_greater'):
        """
        Master function: Generates all forensic features for ML
        Output: Consolidated DataFrame with all scores
        """
        print("\n=== GENERATING FORENSIC FEATURES ===\n")
        
        # 1. Benford Deviation Score
        benford_features = self.calculate_benford_score(enrolment_column)
        
        # 2. Z-Score Velocity
        velocity_features = self.calculate_velocity_score(enrolment_column)
        
        # 3. Bio-to-Demo Ratio
        ratio_features = self.calculate_bio_to_demo_ratio()
        
        # Merge all features
        features = benford_features.merge(velocity_features, on='pincode')
        features = features.merge(ratio_features, on='pincode')
        
        # Add composite risk indicator
        features['composite_flag_count'] = (
            features['benford_flag'].astype(int) +
            features['velocity_flag'].astype(int) +
            features['bypass_flag'].astype(int)
        )
        
        self.features = features
        
        print(f"\n[OK] Feature engineering complete: {len(features)} Pincodes analyzed")
        print(f"  - Benford violations: {features['benford_flag'].sum()}")
        print(f"  - Velocity spikes: {features['velocity_flag'].sum()}")
        print(f"  - Process bypass: {features['bypass_flag'].sum()}")
        print(f"  - Multiple flags: {(features['composite_flag_count'] >= 2).sum()}")
        
        return features

    # Legacy methods for backward compatibility
    def benford_test(self, column_name):
        """Legacy wrapper - use calculate_benford_score instead"""
        results = self.calculate_benford_score(column_name)
        return results[results['benford_flag']]['pincode'].tolist()

    def velocity_checker(self, column_name):
        """Legacy wrapper - maintains old interface"""
        self.calculate_velocity_score(column_name)
        anomalies = self.data[self.data['z_score_velocity'] > 3.0]
        return anomalies[['date', 'district', 'pincode', column_name, 'z_score_velocity']]

    def demographic_skew(self):
        """Legacy wrapper - now includes bio-to-demo ratio"""
        ratio_features = self.calculate_bio_to_demo_ratio()
        flagged = ratio_features[ratio_features['bypass_flag']]
        return flagged[['pincode', 'bio_to_demo_ratio', 'total_biometric', 'total_demographic']]

if __name__ == "__main__":
    # Test stub
    import ingestion
    df = ingestion.load_and_merge_data()
    engine = ForensicEngine(df)
    
    # New unified approach
    print("\n" + "="*60)
    print("UNIFIED FORENSIC FEATURE ENGINEERING")
    print("="*60)
    
    features = engine.generate_forensic_features()
    
    # Show top suspicious Pincodes
    print("\n[TOP 5 MOST SUSPICIOUS PINCODES]:")
    top_suspicious = features.sort_values('composite_flag_count', ascending=False).head(5)
    print(top_suspicious[['pincode', 'benford_deviation_score', 'max_z_score', 
                          'bio_to_demo_ratio', 'composite_flag_count']])
    
    # Save features
    features.to_csv('data/forensic_features.csv', index=False)
    print("\n[OK] Forensic features saved to data/forensic_features.csv")
