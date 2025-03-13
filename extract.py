import os
import pandas as pd

def load_and_merge_csv_files(data_folder):
    files = [f for f in os.listdir(data_folder) if f.endswith('.time')]
    files.sort()
    dataframes = []

    default_column_names = ['timestamp', 'dst.ip', 'dst.port', 'src.ip', 'src.port', 'reps', 'source_file'] 

    for file in files:
        file_path = os.path.join(data_folder, file)
        df = pd.read_csv(file_path, names=default_column_names) 
        df['source_file'] = file
        df['reps'] = 1
        dataframes.append(df)
    merged_df = pd.concat(dataframes, ignore_index=True)
    
    return merged_df


def trim_diplicates(df):
    i = 0
    
    while i < len(df) - 1:
        if df.iloc[i].drop('reps').equals(df.iloc[i + 1].drop('reps')):
            df.at[i, 'reps'] += 1
            df = df.drop(i+1).reset_index(drop=True)
        else:
            i += 1
    
    return df

data_folder = './data'

merged_df = load_and_merge_csv_files(data_folder)
# merged_df.to_csv('./merged_data.csv', index=False)

trimmed_df = trim_diplicates(merged_df)
trimmed_df.to_csv('./trimmed_data.csv', index=False)

print(trimmed_df.head(10))