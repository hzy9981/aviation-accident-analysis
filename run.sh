#!/bin/bash

# Configuration
SOURCE_DATA="data/input_reports"
INPUT_DIR="input"
OUTPUT_DIR="output"

echo "=== Aviation Accident Knowledge Graph Pipeline ==="

# 1. Ingest Data
echo "Step 1: Ingesting data from $SOURCE_DATA..."
mkdir -p "$SOURCE_DATA"
# Assume user puts reports in SOURCE_DATA
uv run python src/ingest.py --source "$SOURCE_DATA" --output "$INPUT_DIR"

# 2. Run GraphRAG Index
echo "Step 2: Running GraphRAG indexing (this may take time and API calls)..."
uv run python -m graphrag index --root .

# 3. Evaluation (Optional)
echo "Step 3: Running evaluation..."
# uv run python src/evaluate.py --results output/artifacts/entities.parquet --gt data/ground_truth.json

echo "Pipeline complete. Check $OUTPUT_DIR for results."
