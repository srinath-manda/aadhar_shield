import requests
import os
from dotenv import load_dotenv
import pandas as pd
from typing import Dict, List

load_dotenv()

class AadhaarAPIClient:
    """Client for fetching real UIDAI Aadhaar data."""
    
    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        self.base_url = "https://www.uidai.gov.in/aadhaar_dashboard/india_data_api.php"
        
    def fetch_data(self, dataset_type: str) -> pd.DataFrame:
        """
        Fetch data from UIDAI API.
        
        Args:
            dataset_type: One of 'enrolment', 'demographic', 'biometric'
        
        Returns:
            DataFrame with the fetched data
        """
        print(f"Fetching {dataset_type} data from UIDAI API...")
        
        # API endpoint mapping
        type_map = {
            'enrolment': 'monthly_enrolment',
            'demographic': 'demographic_update',
            'biometric': 'biometric_update'
        }
        
        params = {
            'api_key': self.api_key,
            'type': type_map.get(dataset_type, dataset_type)
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if 'data' in data:
                df = pd.DataFrame(data['data'])
                print(f"✓ Fetched {len(df)} records for {dataset_type}")
                return df
            else:
                print(f"[!] No data field in response for {dataset_type}")
                return pd.DataFrame()
                
        except requests.exceptions.RequestException as e:
            print(f"[X] Error fetching {dataset_type} data: {e}")
            print(f"  Falling back to synthetic data...")
            return pd.DataFrame()
    
    def fetch_all_datasets(self, save_to_csv=True) -> Dict[str, pd.DataFrame]:
        """Fetch all three datasets and optionally save to CSV."""
        datasets = {}
        
        for dtype in ['enrolment', 'demographic', 'biometric']:
            df = self.fetch_data(dtype)
            
            if df.empty:
                print(f"  Using synthetic data for {dtype}")
                continue
                
            datasets[dtype] = df
            
            if save_to_csv:
                filepath = f"data/{dtype}_data_real.csv"
                df.to_csv(filepath, index=False)
                print(f"  Saved to {filepath}")
        
        return datasets

if __name__ == "__main__":
    client = AadhaarAPIClient()
    datasets = client.fetch_all_datasets()
    
    if datasets:
        print(f"\n✓ Successfully fetched {len(datasets)} datasets")
    else:
        print("\n⚠ No datasets fetched. Using synthetic data.")
