import subprocess
import os
from pathlib import Path

def run_evaluation():
    # 1. Clean previous results
    print("Cleaning output and cache directories...")
    if Path("output").exists():
        subprocess.run(["rm", "-rf", "output"], check=True)
    if Path("cache").exists():
        subprocess.run(["rm", "-rf", "cache"], check=True)
    
    # 2. Ingest Data
    print("Step 1: Ingesting evaluation data...")
    subprocess.run(["uv", "run", "python", "src/ingest.py", "--source", "data/evaluation_set", "--output", "input", "--clear"], check=True)
    
    # 3. Run GraphRAG Index
    print("Step 2: Running GraphRAG indexing...")
    subprocess.run(["uv", "run", "python", "-m", "graphrag", "index", "--root", "."], check=True)
    
    # 4. Evaluation
    print("Step 3: Running evaluation...")
    # Note: entities.parquet is now in output/artifacts/ (depending on graphrag version, but checking script)
    # Actually, the original script used output/entities.parquet. 
    # Let's check where graphrag actually puts them.
    
    entities_path = "output/entities.parquet"
    relationships_path = "output/relationships.parquet"
    
    # Check if they exist in artifacts subfolder instead
    if not os.path.exists(entities_path):
        entities_path = "output/artifacts/entities.parquet"
        relationships_path = "output/artifacts/relationships.parquet"

    result = subprocess.run([
        "uv", "run", "python", "src/evaluate.py", 
        "--entities", entities_path, 
        "--relationships", relationships_path, 
        "--gt", "data/ground_truth.json"
    ], capture_output=True, text=True, check=True)
    
    print(result.stdout)

if __name__ == "__main__":
    run_evaluation()
