import pandas as pd
import re


def clean_spin_matrix(matrix_str):
    if pd.isna(matrix_str):
        return ''

    # Remove outer double brackets if present
    matrix_str = re.sub(r"^\s*\[\[", '[', matrix_str)
    matrix_str = re.sub(r"\]\]\s*$", ']', matrix_str)

    # Remove line breaks inside matrix
    matrix_str = re.sub(r"\s*\n\s*", ' ', matrix_str)

    # Add semicolons between rows if missing
    matrix_str = re.sub(r"\]\s*\[", '];[', matrix_str)

    return matrix_str.strip()

def MHz_cleaner(mHz):
    match = re.search(r'[\d.]+', mHz)
    if match:
        return float(match.group(0))
    else:
        return None

def clean_index(index_str):
    if pd.isna(index_str):
        return 0
    index_str = index_str.strip("[]").strip()
    items = [item for item in index_str.split("'") if item.strip().isdigit()]
    return len(items)



def clean_csv(input_csv, output_csv):
    df = pd.read_csv(input_csv)

    if 'spin_matrix' in df.columns:
        df['spin_matrix'] = df['spin_matrix'].apply(clean_spin_matrix)

    if 'Index' in df.columns:
        df['n_spins'] = df['Index'].apply(clean_index)

    # Ensure 'FieldStrength' is string
    if 'Field Strength' in df.columns:
        df['Field Strength'] = df['Field Strength'].apply(MHz_cleaner)


    df.to_csv(output_csv, index=False, quoting=1)  # Quote all strings

    print(f"✅ Preprocessed CSV saved to: {output_csv}")

