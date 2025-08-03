import pandas as pd
import numpy as np
import json
def get_df_and_data(path,filename):
    metadata_filename = path + filename[:16] + "metadata.json"
    full_path = path + filename
    # Load the CSV
    df = pd.read_csv(full_path)
    with open(metadata_filename, 'r') as file:
        data = json.load(file)

    return df,data

def get_spectral_data(df,row=14, molecule=""):
    df['spectrum'] = df['spectrum'].fillna(r'"[0]"')  # Prevent error in processing later
    if molecule=="":
        target = df.iloc[row-1]
    else:
        if not df[df["Name"] == molecule].empty:
            target = df[df["Name"] == molecule].iloc[0]
        else:
            print(f"Warning: No molecule named '{molecule}' found in the DataFrame.")
            return None, None

    intensities_raw = target["spectrum"][2:-2]

    intensities_strings = intensities_raw.split(';')
    intensities = [float(num_str) for num_str in intensities_strings]
    return np.array(intensities).reshape(-1,1), target["Name"]


def compare_all_spectra(path,filename):
    df, data = get_df_and_data(path,filename)
    all_intensities = []
    for row in range(1,len(df)):
        target = df.iloc[row-1]
        if pd.isna(target["spectrum"]):
            continue
        intensities_raw = target["spectrum"][2:-2]
        intensities_strings = intensities_raw.split(';')
        all_intensities.append([float(num_str) for num_str in intensities_strings])

    return all_intensities

def compare_comparable_spectra(path, filename):
    df, data = get_df_and_data(path, filename)
    spectra_dict = {}
    for _, row in df.iterrows():
        if pd.isna(row["spectrum"]):
            continue
        name = row["Name"]
        intensities_raw = row["spectrum"][2:-2]
        intensities_strings = intensities_raw.split(';')
        intensities = [float(num_str) for num_str in intensities_strings]
        spectra_dict[name] = intensities
    return spectra_dict, data


def compare_all_comparable_spectra(df):
    spectra_dict = {}
    for _, row in df.iterrows():
        if pd.isna(row["spectrum"]):
            continue
        name = row["Name"]
        intensities_raw = row["spectrum"][2:-2]
        intensities_strings = intensities_raw.split(';')
        intensities = [float(num_str) for num_str in intensities_strings]
        spectra_dict[name] = intensities
    return spectra_dict
