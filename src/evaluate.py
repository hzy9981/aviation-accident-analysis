import json
import argparse
import pandas as pd

def is_match(pred, gt):
    pred = pred.strip().upper()
    gt = gt.strip().upper()
    if pred == gt:
        return True
    # Fuzzy: if one is a significant substring of the other
    if len(gt) > 2 and (gt in pred or pred in gt):
        return True
    return False

def calculate_metrics_fuzzy(predicted_set, ground_truth_set):
    if not ground_truth_set:
        return 0.0, 0.0, 0.0
    
    matched_gt = set()
    tp = 0
    
    for p in predicted_set:
        for gt in ground_truth_set:
            if gt not in matched_gt and is_match(p, gt):
                tp += 1
                matched_gt.add(gt)
                break
    
    fp = len(predicted_set) - tp
    fn = len(ground_truth_set) - tp
    
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
    
    gt_entities = [e['title'].strip().upper() for e in gt_data.get('entities', [])]
    gt_rels = [(r['source'].strip().upper(), r['target'].strip().upper()) for r in gt_data.get('relationships', [])]

    # Load Predictions
    try:
        pred_entities_df = pd.read_parquet(args.entities)
        pred_rels_df = pd.read_parquet(args.relationships)
    except Exception as e:
        print(f"Error loading prediction files: {e}")
        return

    pred_entities = list(pred_entities_df['title'].str.strip().str.upper())
    pred_rels = list(zip(pred_rels_df['source'].str.strip().str.upper(), 
                         pred_rels_df['target'].str.strip().str.upper()))

    # Evaluate Entities
    ent_p, ent_r, ent_f1 = calculate_metrics_fuzzy(pred_entities, gt_entities)
    
    # Evaluate Relationships (Fuzzy on both source and target)
    tp_rel = 0
    matched_gt_rel = set()
    for p_src, p_tgt in pred_rels:
        for i, (gt_src, gt_tgt) in enumerate(gt_rels):
            if i not in matched_gt_rel:
                # Check both directions for relationships to be a bit more lenient, 
                # or strictly one direction. Let's stay directed but fuzzy on names.
                if is_match(p_src, gt_src) and is_match(p_tgt, gt_tgt):
                    tp_rel += 1
                    matched_gt_rel.add(i)
                    break
    
    rel_p = tp_rel / len(pred_rels) if pred_rels else 0.0
    rel_r = tp_rel / len(gt_rels) if gt_rels else 0.0
    rel_f1 = 2 * (rel_p * rel_r) / (rel_p + rel_r) if (rel_p + rel_r) > 0 else 0.0

    print("\n" + "="*30)
    print("      EVALUATION RESULTS (FUZZY)")
    print("="*30)
    print(f"{'Metric':<15} | {'Entities':<10} | {'Relationships':<10}")
    print("-" * 45)
    print(f"{'Precision':<15} | {ent_p:<10.4f} | {rel_p:<10.4f}")
    print(f"{'Recall':<15} | {ent_r:<10.4f} | {rel_r:<10.4f}")
    print(f"{'F1 Score':<15} | {ent_f1:<10.4f} | {rel_f1:<10.4f}")
    print("="*30)

if __name__ == "__main__":
    main()
