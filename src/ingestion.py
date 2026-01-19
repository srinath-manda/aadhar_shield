import pandas as pd
import os

def load_and_merge_data(data_dir="data"):
    """
    Loads Enrolment, Demographic, and Biometric CSVs.
    Merges them into a single DataFrame on 'date', 'state', 'district', 'pincode'.
    Converts numeric columns from string to appropriate types.
    """
    print("Loading datasets...")
    
    try:
        df_enrolment = pd.read_csv(os.path.join(data_dir, "enrolment_data.csv"))
        df_demo = pd.read_csv(os.path.join(data_dir, "demographic_data.csv"))
        df_bio = pd.read_csv(os.path.join(data_dir, "biometric_data.csv"))
    except FileNotFoundError as e:
        print(f"Error loading files: {e}")
        return None

    print("Merging datasets...")
    # Merge Enrolment and Demo
    merged_df = pd.merge(df_enrolment, df_demo, on=['date', 'state', 'district', 'pincode'], how='outer')
    
    # Merge with Bio
    final_df = pd.merge(merged_df, df_bio, on=['date', 'state', 'district', 'pincode'], how='outer')
    
    # Fill NaNs with 0 (assuming missing means no activity) and convert to string for cleaning
    final_df = final_df.fillna("0")
    
    # Columns to convert to numeric
    numeric_cols = [
        'age_0_5', 'age_5_17', 'age_18_greater',
        'demo_age_5_17', 'demo_age_17_',
        'bio_age_5_17', 'bio_age_17_'
    ]
    
    print("Cleaning and converting types...")
    for col in numeric_cols:
        # Remove potential non-numeric chars if any (though synthetic is clean)
        # In real API data, these were strings.
        final_df[col] = pd.to_numeric(final_df[col], errors='coerce').fillna(0).astype(int)

    print(f"Data ingestion complete. Shape: {final_df.shape}")
    return final_df

if __name__ == "__main__":
    df = load_and_merge_data()
    if df is not None:
        print(df.head())
        # Save merged for inspection
        df.to_csv(os.path.join("data", "merged_aadhaar_data.csv"), index=False)
