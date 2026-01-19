import pandas as pd
import numpy as np
import random
import os
from datetime import datetime, timedelta

def generate_dates(start_date, end_date):
    start = datetime.strptime(start_date, "%d-%m-%Y")
    end = datetime.strptime(end_date, "%d-%m-%Y")
    date_list = []
    while start <= end:
        date_list.append(start.strftime("%d-%m-%Y"))
        start += timedelta(days=30)
    return date_list

def generate_massive_dataset(num_pincodes=200, output_dir="data"):
    """
    Generates a large-scale 'Real-Looking' base and injects MANY faults.
    This simulates 10,000+ records to show the scale and ML robustness.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    print(f"Generating massive dataset with {num_pincodes} Pincodes...")
    
    states = ['Delhi', 'Maharashtra', 'Karnataka', 'Uttar Pradesh', 'Gujarat', 'Tamil Nadu', 'West Bengal']
    districts = {
        'Delhi': ['New Delhi', 'North Delhi', 'South Delhi'], 
        'Maharashtra': ['Mumbai', 'Pune', 'Nagpur'],
        'Karnataka': ['Bangalore', 'Mysore', 'Hubli'],
        'Uttar Pradesh': ['Lucknow', 'Kanpur', 'Varanasi'],
        'Gujarat': ['Ahmedabad', 'Surat'],
        'Tamil Nadu': ['Chennai', 'Coimbatore'],
        'West Bengal': ['Kolkata', 'Howrah']
    }
    
    pincodes = [f"{random.randint(110000, 999999)}" for _ in range(num_pincodes)]
    dates = generate_dates("01-01-2024", "31-12-2025") # 2 years of data
    
    enrolment_recs, demo_recs, bio_recs = [], [], []
    
    # 1. Select 10% of Pincodes to be "Dirty"
    dirty_pincodes = random.sample(pincodes, int(num_pincodes * 0.10))
    print(f"Injecting faults into {len(dirty_pincodes)} Pincodes (Dirty Set)...")

    for pincode in pincodes:
        state = random.choice(states)
        district = random.choice(districts[state])
        is_dirty = pincode in dirty_pincodes
        
        # Choose a fault type for dirty pincodes
        fault_type = random.choice(['spike', 'benford', 'ratio', 'hybrid']) if is_dirty else 'none'
        
        for date in dates:
            # Base values (Clean)
            e_18 = random.randint(50, 500)
            d_17 = random.randint(10, 100)
            b_17 = random.randint(20, 150)
            
            # --- FAULT INJECTIONS ---
            if fault_type == 'spike' and "2025" in date:
                # Scenario: Bulk Spiker (15x)
                if random.random() > 0.7: e_18 = int(e_18 * random.uniform(10, 20))
                
            elif fault_type == 'benford':
                # Scenario: Data Fabricator (Always starts with 5 or 8)
                e_18 = int(f"{random.choice([5, 8])}{random.randint(10, 99)}")
                d_17 = int(f"{random.choice([5, 8])}{random.randint(1, 9)}")
                
            elif fault_type == 'ratio':
                # Scenario: Process Bypass (50:1 Bio to Demo)
                b_17 = random.randint(1000, 2000)
                d_17 = random.randint(1, 5)
                
            elif fault_type == 'hybrid':
                # All of the above
                e_18 = int(e_18 * 5)
                b_17 = b_17 * 10
                d_17 = 2
            
            # Enrolment
            enrolment_recs.append({
                "date": date, "state": state, "district": district, "pincode": pincode,
                "age_0_5": str(random.randint(5, 50)), 
                "age_5_17": str(random.randint(10, 100)),
                "age_18_greater": str(e_18)
            })
            
            # Demo
            demo_recs.append({
                "date": date, "state": state, "district": district, "pincode": pincode,
                "demo_age_5_17": str(random.randint(2, 20)),
                "demo_age_17_": str(d_17)
            })
            
            # Bio
            bio_recs.append({
                "date": date, "state": state, "district": district, "pincode": pincode,
                "bio_age_5_17": str(random.randint(5, 40)),
                "bio_age_17_": str(b_17)
            })

    # Save
    pd.DataFrame(enrolment_recs).to_csv(os.path.join(output_dir, "enrolment_data.csv"), index=False)
    pd.DataFrame(demo_recs).to_csv(os.path.join(output_dir, "demographic_data.csv"), index=False)
    pd.DataFrame(bio_recs).to_csv(os.path.join(output_dir, "biometric_data.csv"), index=False)
    
    # Save Labels for accuracy calculation (GROUND TRUTH)
    labels_df = pd.DataFrame({'pincode': pincodes})
    labels_df['is_fraud'] = labels_df['pincode'].isin(dirty_pincodes)
    labels_df.to_csv(os.path.join(output_dir, "ground_truth_labels.csv"), index=False)
    
    total_recs = len(enrolment_recs)
    print(f"[OK] Massive dataset generated: {total_recs} records across {num_pincodes} Pincodes.")
    print(f"[OK] Ground truth labels saved for accuracy verification.")

if __name__ == "__main__":
    generate_massive_dataset(num_pincodes=300) # ~7,200 records (enough for demo)
