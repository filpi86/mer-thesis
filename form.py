import pandas as pd
from pathlib import Path
import json

# Static settings
input_csv = Path('~/Desktop/Thesis code/User-Songs-Music-Group.xls').expanduser()
output_csv = input_csv.parent / 'form_to_send.csv'
key_csv = input_csv.parent / 'form_key.csv'

random_seed = 42
songs_per_group = 25

# preparation columns from the dataset
group = 'disorder'
control = 'control'
depression = 'depression'

artist = 'artist'
song = 'title'
link = 'music_url'

# Load the dataset
df = pd.read_csv(input_csv)

# Sanity check
required_columns = [group, artist, song, link]
missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    raise ValueError(f'Missing required columns: {missing_columns}')
    
# split groups
control_df = df[df[group] == control].copy()
depression_df = df[df[group] == depression].copy()

# sample rows
control_sample = control_df.sample(n=songs_per_group, random_state=random_seed)
depression_sample = depression_df.sample(n=songs_per_group, random_state=random_seed)

sampled_df = pd.concat([control_sample, depression_sample], ignore_index=True)

# Shuffle combined sample
sampled_df = sampled_df.sample(frac=1, random_state=random_seed).reset_index(drop=True)

# Assign new IDs
sampled_df.insert(0, 'id', [f'S{str(i+1).zfill(3)}' for i in range(len(sampled_df))])

# expert columns
expert_df = sampled_df[['id', 'artist', 'title', 'music_url']].copy()

# columns to fill
expert_df['valence'] = ''
expert_df['arousal'] = ''

# save file to csv -> UNCOMMENT TO SAVE
expert_df.to_csv(output_csv, index=False, sep=';')
sampled_df.to_csv(key_csv, index=False, sep=';')

# Save to json
songs_data = expert_df.to_dict(orient='records')

json_path = input_csv.parent / 'form_data.json'
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(songs_data, f, ensure_ascii=False, indent=2)

print(f'Saved sampled annotation file to {output_csv}')
print(f'Saved key file to {key_csv}')
print(f'Saved JSON file to {json_path}')
print(f'Total songs: {len(expert_df)}')
print(f'Control sampled: {len(control_sample)}')
print(f'Depression sampled: {len(depression_sample)}')