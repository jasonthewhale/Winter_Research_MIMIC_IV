import os
import pandas as pd

# Define the directory path where the CSV files are located
directory_path = './icu_samples/'

# Create an empty list to store the column names of each CSV file
column_names_list = []

# Loop through all CSV files in the directory
for filename in os.listdir(directory_path):
    if filename.endswith('.csv'):
        # Read the CSV file into a Pandas dataframe
        df = pd.read_csv(directory_path + filename)
        # Extract the column names and add them to the list
        column_names_list.append(list(df.columns))

# Find the common column names among all CSV files
common_column_names = set(column_names_list[0]).intersection(*column_names_list[1:])

# Print the common column names
print('Common column names:', common_column_names)

"""
Common keys in core:
'subject_id'

Common keys in hosp:
None

Common keys in icu:
None
"""