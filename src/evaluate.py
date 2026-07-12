import json
import argparse
import pandas as pd

def calculate_metrics(predicted_set, ground_truth_set):
    if not ground_truth_set:
        return 0.0, 0.0, 0.0
    
    tp = len(predicted_set.intersection(ground_truth_set))
    fp = len(predicted_set - ground_truth_set)
    fn = len(ground_truth_set - predicted_set)
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return precision, recall, f1

def main():
    parser = argparse.ArgumentParser(description="Evaluate GraphRAG extraction results.")
    parser.add_argument("--entities", type=str, required=True, help="Path to entities parquet file.")
    parser.add_argument("--relationships", type=str, required=True, help="Path to relationships parquet file.")
    parser.add_argument("--gt", type=str, required=True, help="Path to ground truth JSON file.")
    args = parser.parse_args()

    # Load Ground Truth
    with open(args.gt, 'r', encoding='utf-8') as f:
        gt_data = json.load(f)
    
    gt_entities = set(e['title'].strip().upper() for e in gt_data.get('entities', []))
    gt_rels = set((r['source'].strip().upper(), r['target'].strip().upper()) for r in gt_data.get('relationships', []))

    # Load Predictions
    try:
        pred_entities_df = pd.read_parquet(args.entities)
        pred_rels_df = pd.read_parquet(args.relationships)
    except Exception as e:
        print(f"Error loading prediction files: {e}")
        return

    pred_entities = set(pred_entities_df['title'].str.strip().str.upper())
    pred_rels = set(zip(pred_rels_df['source'].str.strip().str.upper(), 
                        pred_rels_df['target'].str.strip().str.upper()))

    # Evaluate Entities
    ent_p, ent_r, ent_f1 = calculate_metrics(pred_entities, gt_entities)
    
    # Evaluate Relationships
    rel_p, rel_r, rel_f1 = calculate_metrics(pred_rels, gt_rels)

    print("\n" + "="*30)
    print("      EVALUATION RESULTS")
    print("="*30)
    print(f"{'Metric':<15} | {'Entities':<10} | {'Relationships':<10}")
    print("-" * 45)
    print(f"{'Precision':<15} | {ent_p:<10.4f} | {rel_p:<10.4f}")
    print(f"{'Recall':<15} | {ent_r:<10.4f} | {rel_r:<10.4f}")
    print(f"{'F1 Score':<15} | {ent_f1:<10.4f} | {rel_f1:<10.4f}")
    print("="*30)

    # Detailed Mismatches (Optional)
    missing_entities = gt_entities - pred_entities
    if missing_entities:
        print(f"\nMissing Entities ({len(missing_entities)}):")
        print(", ".join(list(missing_entities)[:10]))

if __name__ == "__main__":
    main()
