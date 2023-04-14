import pandas as pd
import os


def fetch_pathes(folder_path):
    file_name_list = os.listdir(folder_path)
    file_path_list = []
    for file_name in file_name_list:
    # construct the full path to the file by joining the folder path and the file name
        file_path = os.path.join(folder_path, file_name)
    
    # check if the file is a regular file (i.e., not a directory)
        if file_name.endswith('.csv') and not file_name.endswith('.gz'):
            file_path_list.append(file_path)
    return file_path_list


def save_sample(source_path, save_path, row_number):
    df = pd.read_csv(source_path, delimiter=',', encoding='utf-8', nrows=row_number)
    df.to_csv(save_path, index=False)


def main():
    core_path = '/Volumes/Jasonthewha/mimic-iv-0.4/core'
    hosp_path = '/Volumes/Jasonthewha/mimic-iv-0.4/hosp'

    core_sample_path = '/Users/youjunchen/Desktop/AI_tools/Winter_Research_MIMIC_IV/core_samples/'
    hosp_sample_path = '/Users/youjunchen/Desktop/AI_tools/Winter_Research_MIMIC_IV/hosp_samples/'

    hosp_files_list = fetch_pathes(hosp_path)
    for source_file_path in hosp_files_list:
        save_path = hosp_sample_path + source_file_path.split('hosp/')[1][:-4] + "_sample.csv"
        save_sample(source_file_path, save_path, 400)