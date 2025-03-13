# Netflow Data Analysis Tools

This Python code is useful for analyzing net flow exported data. It merges all `.time` files, resolves IPs, removes duplicates, and exports all data into a CSV file which can then be analyzed in forensics.

## Functionality

### `extract.py`

- **Description**: Extracts net flow data from a specified file or directory.
- **Features**:
  - Load data from a single file or merge data from multiple files in a directory.
  - Optionally trim duplicate records.
  - Optionally resolve IP addresses using `ipinfo.io`.
  - Export the processed data into a CSV file.

### `resolve.py`

- **Description**: Resolves IP addresses to additional information using `ipinfo.io`.
- **Features**:
  - Fetch hostname, city, country, and organization information for each IP address.
  - Integrate the resolved information into the net flow data.
  - Export the enriched data into a CSV file.

### `merge.py`

- **Description**: Merges multiple net flow data files into a single DataFrame.
- **Features**:
  - Load and merge data from multiple `.time` files in a specified directory.
  - Sort and concatenate the data into a single DataFrame.
  - Export the merged data into a CSV file.

## Usage

1. **Extract Data**:

   ```bash
   python extract.py
   ```

2. **Resolve IPs**:

   ```bash
   python resolve.py
   ```

3. **Merge Data**:

   ```bash
   python merge.py
   ```

## Output

The processed data is exported into a CSV file, which can be further analyzed for forensic purposes.

## TODO

- nfExtractor.py which will connect all the scripts
