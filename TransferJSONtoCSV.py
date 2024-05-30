import pandas as pd
import json
import os

def json_to_csv(json_file_path, csv_file_path):
    # Check if the JSON file exists
    if not os.path.exists(json_file_path):
        print(f"File not found: {json_file_path}")
        return

    try:
        # Read the JSON file
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        # Convert the JSON data to a DataFrame
        df = pd.DataFrame(data)

        # Export the DataFrame to a CSV file with UTF-8 encoding
        df.to_csv(csv_file_path, encoding='utf-8-sig', index=False)
        print(f"CSV file created successfully at: {csv_file_path}")

    except json.JSONDecodeError as e:
        print(f"Error reading JSON file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Replace 'your_json_file.json' and 'output_csv_file.csv' with the appropriate file paths
json_file_path = r'XXX'
csv_file_path = r'XXX'

json_to_csv(json_file_path, csv_file_path)
