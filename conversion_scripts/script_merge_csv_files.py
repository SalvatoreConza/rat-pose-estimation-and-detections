import sys
import pandas as pd
import os
import glob
import tqdm

"""
    Usage: python merge_csv.py file1.csv file2.csv ...
"""

def check_column_consistency(file_list):
    column_sets = {}
    
    for file in file_list:
        try:
            df = pd.read_csv(file, nrows=1)  # Read only first row to check columns
            column_sets[file] = set(df.columns)
        except Exception as e:
            print(f"Error reading {file}: {e}")
            return None
    
    all_columns = set.union(*column_sets.values())
    inconsistent_files = {}
    for file, columns in column_sets.items():
        unique_columns = columns - set.intersection(*column_sets.values())
        if unique_columns:
            inconsistent_files[file] = unique_columns
    
    if inconsistent_files:
        print("Column inconsistency detected:")
        for file, unique_cols in inconsistent_files.items():
            print(f"{file} has unique columns: {unique_cols}")
        sys.exit(1)
    
    return list(all_columns)

def find_output_filename(filename="output.csv"):
    basename, ext = os.path.splitext(filename)
    if not os.path.exists(filename):
        return filename
    
    i = 1
    while os.path.exists(f"{basename}_{i}.{ext}"):
        i += 1
    return f"{basename}_{i}.{ext}"

def merge_csv_files(file_list, output_file,duplicates_allowed):
    dfs = [pd.read_csv(file) for file in tqdm.tqdm(file_list, desc="Reading CSV files")]
    merged_df = pd.concat(dfs, ignore_index=True)
    if not duplicates_allowed:
        merged_df = merged_df.drop_duplicates(subset=['filename'], keep='last')
    merged_df.to_csv(output_file, index=False)
    print(f"Merged CSV saved as {output_file}")

def main():
    if len(sys.argv) < 3:
        print("Usage: python merge_csv.py output.csv file1.csv file2.csv ...")
        sys.exit(1)
    
    duplicates_allowed = False

    output_file = sys.argv[1]
    input_dir = sys.argv[2:]
    
    if os.path.isdir(input_dir[0]):
        csv_files = glob.glob(os.path.join(input_dir[0], os.path.join("**","*converted.csv")), recursive=True)
    else:
        csv_files = input_dir
    print(f"Found {len(csv_files)} CSV files in {input_dir}")
     
    common_columns = check_column_consistency(csv_files)
    if common_columns:
        # output_file = find_output_filename(filename=output_file)
        merge_csv_files(csv_files, output_file, duplicates_allowed)

if __name__ == "__main__":
    main()