import pandas as pd
for file in ['text_units.parquet', 'community_reports.parquet']:
    path = f'output/{file}'
    try:
        df = pd.read_parquet(path)
        col = 'full_content' if 'full_content' in df.columns else 'text'
        df['len'] = df[col].str.len()
        print(f"{file} max length: {df['len'].max()}")
    except: pass
