import lancedb
import pandas as pd

def check_lancedb():
    db = lancedb.connect("output/lancedb")
    print("Tables:", db.table_names())
    
    for table_name in db.table_names():
        table = db.open_table(table_name)
        print(f"\nTable: {table_name}")
        print(f"Total rows: {len(table.to_pandas())}")
        # Search for a term - this requires embeddings usually, 
        # but we can just look at the data first.
        df = table.to_pandas()
        if 'text' in df.columns:
            matches = df[df['text'].str.contains('3U8633', na=False)]
            print(f"Text matches for '3U8633': {len(matches)}")
        elif 'description' in df.columns:
            matches = df[df['description'].str.contains('3U8633', na=False)]
            print(f"Description matches for '3U8633': {len(matches)}")

if __name__ == "__main__":
    check_lancedb()
