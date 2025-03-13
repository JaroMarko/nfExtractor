import argparse
import os
import sys
import pandas as pd
import requests

default_column_names = ['timestamp', 'dst.ip', 'dst.port', 'src.ip', 'src.port', 'reps', 'source_file'] 
ipinfo_token = 'XXX'

def load_file(file_path):
    df = pd.read_csv(file_path, names=default_column_names) 
    df['source_file'] = file_path
    df['reps'] = 1
    return df


def load_directory_and_merge(folder_path):
    files = [f for f in os.listdir(file_path) if f.endswith('.time')]
    files.sort()
    dataframes = []

    for file in files:
        file_path = os.path.join(file_path, file)
        if os.path.isfile(file_path):
            df = load_file(file_path)
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

def resolve_ip(ip):
    response = requests.get(f'https://ipinfo.io/{ip}/json?token={ipinfo_token}')
    if response.status_code == 200:
        data = response.json()
        return {
            'dst.ip': ip,
            'hostname': data.get('hostname', ''),
            'city': data.get('city', ''),
            'country': data.get('country', ''),
            'org': data.get('org', '')
        }
    else:
        return {
            'dst.ip': ip,
            'hostname': '',
            'city': '',
            'country': '',
            'org': ''
        }

def main():
    parser = argparse.ArgumentParser(description='Netflow data extractor, merger, and resolver.')
    parser.add_argument('-f', '--file', type=str, help='File for analysis')
    parser.add_argument('-d', '--directory', type=str, help='Folder for analysis')
    parser.add_argument('-t', '--trim', help='Trim duplicates of the records')
    parser.add_argument('-nip', '--no-ipresolve', action='store_true', help='Skip IP resolve using ipinfo.io')

    args = parser.parse_args()

    if args.file:
        if os.path.isfile(args.file):
            csv_file = load_file(args.file)
            if args.trim:
                csv_file = trim_diplicates(csv_file)
            if not args.no_ipresolve:
                csv_file['resolved_ip'] = csv_file['dst.ip'].apply(resolve_ip)
        else:
            print(f"File {args.file} does not exist.")
            sys.exit(1)
    elif args.directory:
        if os.path.isdir(args.directory):
            csv_files = load_directory_and_merge(args.directory)
            if args.trim:
                csv_files = trim_diplicates(csv_files)
            if not args.no_ipresolve:
                csv_files['resolved_ip'] = csv_files['dst.ip'].apply(resolve_ip)
        else:
            print(f"Directory {args.directory} does not exist.")
            sys.exit(1)
    else:
        print("Please provide a file or directory for analysis.")
        sys.exit(1)

if __name__ == "__main__":
    main()