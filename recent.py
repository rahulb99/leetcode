import os
import pandas as pd

# Define the filename to search for in subfolders
target_filename = "1. Thirty Days.csv"
output_filename = "recent.csv"

# List to store dataframes
dataframes = []

# Top tech companies
companies = ["Meta", "Apple", "Amazon", "Google", "Microsoft", "Uber", "Tesla", "Lyft", "Databricks", "Block", "Datadog", "DoorDash"]

# Walk through all subdirectories
for root, dirs, files in os.walk("."):
    # Check if the current directory name is in the list of companies
    # Check if the target filename exists in the current directory
    if any(company in root for company in companies) and target_filename in files:
        file_path = os.path.join(root, target_filename)
        # Read the CSV file and append it to the list
        try:
            df = pd.read_csv(file_path)
            df['company'] = os.path.basename(root)  # Add a new column with the company name
            dataframes.append(df)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

# Combine all dataframes
if dataframes:
    combined_df = pd.concat(dataframes, ignore_index=True)
    if 'Acceptance Rate' in combined_df.columns:
        combined_df = combined_df.drop(columns=['Acceptance Rate'])
    combined_df['Companies'] = combined_df.groupby('Title')['company'].transform(lambda x: ', '.join(x))
    if 'company' in combined_df.columns:
        combined_df = combined_df.drop(columns=['company'])
    combined_df = combined_df.drop_duplicates(subset="Title", keep='first')
    combined_df.to_csv(output_filename, index=False)

else:
    print("No files found to process.")