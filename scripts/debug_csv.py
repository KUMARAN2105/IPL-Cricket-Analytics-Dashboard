import pandas as pd
from pathlib import Path

base = Path(__file__).resolve().parent.parent
raw = base / 'data' / 'raw' / 'matches.csv'
processed = base / 'data' / 'processed' / 'matches_clean.csv'
print('raw exists', raw.exists())
print('processed exists', processed.exists())
if raw.exists():
    df = pd.read_csv(raw)
    print('raw rows', len(df))
    print('raw head:')
    print(df.head(10).to_string(index=False))
if processed.exists():
    df2 = pd.read_csv(processed)
    print('processed rows', len(df2))
    print('processed head:')
    print(df2.head(10).to_string(index=False))
