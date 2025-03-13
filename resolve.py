import pandas as pd
import requests

# Load the CSV file
df = pd.read_csv('./trimmed_data.csv')

# Select all unique source IP addresses
unique_ips = df['dst.ip'].unique()

# Function to resolve IP address using ipinfo.io
def resolve_ip(ip):
    response = requests.get(f'https://ipinfo.io/{ip}/json?token=XXX')
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

# Resolve all unique IP addresses
resolved_ips = [resolve_ip(ip) for ip in unique_ips]

# Create a DataFrame from the resolved IP information
resolved_df = pd.DataFrame(resolved_ips)

# Save the DataFrame to a CSV file
resolved_df.to_csv('ipresolve.csv', index=False)

print("IP resolution information has been saved to ipresolve.csv")