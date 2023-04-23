import pandas as pd
import os

pd.set_option('display.max_colwidth', None)

core_path = '/Volumes/Jasonthewha/mimic-iv-0.4/core'
hosp_path = '/Volumes/Jasonthewha/mimic-iv-0.4/hosp'
icu_path = '/Volumes/Jasonthewha/mimic-iv-0.4/icu'

def fetch_csv_pathes(folder_path):
    file_name_list = os.listdir(folder_path)
    file_path_list = []
    for file_name in file_name_list:
    # construct the full path to the file by joining the folder path and the file name
        file_path = os.path.join(folder_path, file_name)
    
    # check if the file is a regular file (i.e., not a directory)
        if file_name.endswith('.csv') and not file_name.endswith('.gz') and "._" not in file_name:
            file_path_list.append(file_path)
    return file_path_list


def save_patient_sample(foler_path):
    pass


def fetch_patient_with_subjectid(subject_id):
    core_csvs_list = fetch_csv_pathes(core_path)
    hosp_csvs_list = fetch_csv_pathes(hosp_path)
    icu_csvs_list = fetch_csv_pathes(icu_path)

    full_list = core_csvs_list + hosp_csvs_list + icu_csvs_list

    for csv_file in full_list:
        chunksize = 10 ** 5  # Adjust chunk size as needed
        gen_chunks = pd.read_csv(csv_file, delimiter=',', encoding='utf-8', engine='c', chunksize=chunksize, low_memory=False)

        for chunk in gen_chunks:
            try:
                if subject_id in chunk['subject_id'].values:
                    print(f"{csv_file} info of {subject_id} is: ")
                    print(chunk[chunk['subject_id'] == subject_id])
                    print("\n\n----------------------------\n\n")
            except KeyError:
                print(csv_file + " doesn't have subject_id column")
                continue


def fetch_unique_subject_id():
    # fetch unique subject id from local core_samples folder
    core_sample_path = '/Users/youjunchen/Desktop/AI_tools/Winter_Research_MIMIC_IV/core_samples/'
    core_csvs_list = fetch_csv_pathes(core_sample_path)
    subject_id_list = []
    for csv in core_csvs_list:
        df = pd.read(csv, delimiter=',', encoding='utf-8')
        subject_id = df['subject_id'].values
        if subject_id not in subject_id_list:
            subject_id_list.append(df['subject_id'].values)
    return subject_id_list

def main():
    subject_ids = fetch_unique_subject_id()
    for subject_id in subject_ids:
        fetch_patient_with_subjectid(subject_id)