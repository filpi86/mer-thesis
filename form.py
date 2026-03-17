import pandas as pd

df = pd.read_csv('~/Desktop/Thesis code/lyrics_emotions.csv')

dataset_50 = (
    df[df['disorder'].isin(['depression', 'anxiety'])]
    .groupby('disorder', group_keys=False)
    .sample(n=25, random_state=42)
    .reset_index(drop=True)
)

print(dataset_50['disorder'].value_counts())