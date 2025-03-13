import pandas as pd

# Load the CSV files
trimmed_data = pd.read_csv('./trimmed_data.csv')
ip_resolve = pd.read_csv('./ipresolve.csv')

# Merge the dataframes based on the 'dst.ip' column
merged_data = pd.merge(trimmed_data, ip_resolve, how='left', left_on='dst.ip', right_on='dst.ip')

# Add the 'dst.protocol' column by resolving 'dst.port'
protocol_mapping = {
    21: 'FTP',
    22: 'SSH',
    25: 'SMTP',
    53: 'DNS',
    80: 'HTTP',
    81: 'Trojans|HTTP',
    85: 'Trojans|HTTP',
    123: 'NTP',
    110: 'POP3',
    143: 'IMAP',
    443: 'HTTPS',
    853: 'DNS',
    3000: 'various|Trojans',
    5222: 'Chat',
    5228: 'GoogleStore|WhatsApp',
    7275: 'Oma-ulp',
    8000: 'VideoStreaming|Trojans',
    8086: 'ipTV|Wiki-services',
    8666: 'Monetra Admin',
    8820: 'Unassigned',
    8883: 'MQTT',
    8886: 'applications',
    8895: 'Unassigned',
    19302: 'GoogleTalk',
    25903: 'NIProbe',
    36653: 'Unassigned',
    46030: 'Unassigned',

}

merged_data['dst.protocol'] = merged_data['dst.port'].map(protocol_mapping).fillna('UNKNOWN')

# Reorder the columns
merged_data = merged_data[['timestamp', 'reps', 'src.ip', 'src.port', 'dst.ip', 'dst.port', 'dst.protocol', 'hostname', 'org', 'city', 'country', 'source_file']]


# Save the merged dataframe to a new CSV file
merged_data.to_csv('merged_data.csv', index=False)