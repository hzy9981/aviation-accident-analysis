import pandas as pd

def summarize_extraction():
    try:
        entities = pd.read_parquet('output/entities.parquet')
        relationships = pd.read_parquet('output/relationships.parquet')
        
        print("=== Extraction Summary ===")
        print(f"Total Entities Extracted: {len(entities)}")
        print(f"Total Relationships Extracted: {len(relationships)}")
        
        print("\n=== Entity Types Distribution ===")
        print(entities['type'].value_counts())
        
        print("\n=== Top 10 Entities by Degree ===")
        print(entities[['title', 'type', 'degree']].sort_values(by='degree', ascending=False).head(10))
        
        print("\n=== Sample Relationships ===")
        # Merge to get titles for source/target if they are IDs
        # In GraphRAG output/relationships.parquet, source and target are usually titles/strings
        print(relationships[['source', 'target', 'description']].head(5))
        
    except Exception as e:
        print(f"Error during summary: {e}")

if __name__ == "__main__":
    summarize_extraction()
