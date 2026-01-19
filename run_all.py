import os
import sys

def run_step(step_name, command):
    print(f"\n{'='*20}")
    print(f"[STEP]: {step_name}")
    print(f"{'='*20}")
    exit_code = os.system(command)
    if exit_code != 0:
        print(f"\n[ERROR]: {step_name} failed with exit code {exit_code}")
        sys.exit(exit_code)
    print(f"[OK] {step_name} completed successfully.")

def main():
    print("Aadhaar-Shield Master Execution Script")
    print("Initializing forensic audit pipeline...\n")
    
    # Ensure data directory exists
    if not os.path.exists('data'):
        os.makedirs('data')

    # Step 1: Data Generation (Red Team Injection)
    run_step("Data Generation", "python src/data_generator.py")

    # Step 2: Ingestion & Merging
    run_step("Data Ingestion", "python src/ingestion.py")

    # Step 3: Forensic Engine (Chi-Square & Z-Scores)
    run_step("Forensic Math", "python src/forensics.py")

    # Step 4: ML Training & Scoring
    run_step("AI Training", "python src/anomaly_detection.py")

    print(f"\n{'='*40}")
    print("ALL SYSTEMS READY")
    print("Your Aadhaar-Shield project is fully generated, merged, and analyzed.")
    print("\nNext Step: Run the Dashboard")
    print("-> streamlit run src/app.py")
    print(f"{'='*40}")

if __name__ == "__main__":
    main()
