import pandas as pd
import matplotlib.pyplot as plt
import ast
from sklearn.preprocessing import PolynomialFeatures, MinMaxScaler
from sklearn.linear_model import LinearRegression

import seaborn as sns
import numpy as np
import json
import re
from sklearn.pipeline import make_pipeline

def scatterplot(df, filename, yscale='linear', filename_plot='computation_time_plot.png', title_suffix='', save=False, degree=2):
    df_sorted = df.sort_values(by='computation_time')
    X_spins = df_sorted['n_spins'].values.reshape(-1, 1)
    y_time = df_sorted['computation_time'].values

    # Polynomial regression model
    model = make_pipeline(PolynomialFeatures(degree=degree), LinearRegression())
    model.fit(X_spins, y_time)
    x_range = np.linspace(X_spins.min(), (X_spins.max() * 1.2), 200).reshape(-1, 1)
    y_pred = model.predict(x_range)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(X_spins, y_time, c='blue', alpha=0.7, label='Data')
    ax.plot(x_range, y_pred, color='red', linewidth=2, label=f'Polynomial Regression (degree={degree})')
    ax.set(xlabel='Number of Spins',
           ylabel='Computation Time (s)',
           title=f'Computation Time for H1 NMR {title_suffix}',
           yscale=yscale)
    ax.legend()
    if yscale=='log': ax.grid(True,which='both')
    else: ax.grid(True)
    fig.tight_layout()
    if save:
        fig.savefig(filename[:16]+ "_"+filename_plot)
    if filename_plot.endswith('.png'):
        plt.show()
    else:
        plt.close()




def violinplot(df, filename='', yscale='linear', filename_plot='computation_time_violin.png', title_suffix='',
                       save=False):
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.violinplot(data=df, x='n_spins', y='computation_time', ax=ax, inner='point', density_norm='width', cut=0) #inner=box is also helpful

    ax.set(xlabel='Number of Spins',
           ylabel='Computation Time (s)',
           title=f'Computation Time Distribution for H1 NMR {title_suffix}',
           yscale=yscale)

    ax.grid(True, which='both' if yscale == 'log' else 'major')
    fig.tight_layout()

    if save:
        fig.savefig(filename[:16] + "_" + filename_plot)
    if filename_plot.endswith('.png'):
        plt.show()
    else:
        plt.close()


import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd


def boxplot(
        df,
        filename='',
        yscale='linear',
        filename_plot='computation_time_boxplot.png',
        title_suffix='',
        column='n_spins',
        save=False,
        regression_df=None,  # Optional DataFrame for regression line
        regression_label='Predicted Time',
        regression_color='#e94634'
):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.set_theme(style='whitegrid', font_scale=1.5)

    # Draw boxplot
    sns.boxplot(data=df, x=column, y='computation_time', ax=ax)

    # Axis labels and title
    if column == 'n_spins':
        ax.set(
            xlabel='Number of Spins',
            ylabel='Computation Time (s)',
            title=f'Computation Time for 1H NMR {title_suffix}',
            yscale=yscale
        )
    else:
        ax.set(
            xlabel='Number of J-couplings',
            ylabel='Computation Time (s)',
            title=f'Computation Time for 1H NMR {title_suffix}',
            yscale=yscale
        )
 #   if yscale == 'log':
 #       ax.set_ylim(top=1e5)

    # Overlay regression line if provided
    if regression_df is not None and column in regression_df.columns:
        # Fix tick labels to match all unique values from both datasets
        all_x_vals = sorted(set(df[column].unique()) | set(regression_df[column].unique()))
        ax.set_xticks(range(len(all_x_vals)))
        ax.set_xticklabels([str(x) if (i+1) % 5 == 0 else '' for i, x in enumerate(all_x_vals)])
        for i in range(0, len(all_x_vals), 5):
            ax.axvline(x=i-1, color='gray', linewidth=1.5, alpha=0.6)


        # Align boxplot and regression curve
        x_pos_map = {val: idx for idx, val in enumerate(all_x_vals)}
        ax.plot(
            [x_pos_map[x] for x in regression_df[column]],
            regression_df['predicted_computation_time'],
            color=regression_color,
            label=regression_label,
            linewidth=2
        )
        ax.legend()

    ax.grid(True, which='both' if yscale == 'log' else 'major')
    fig.tight_layout()

    if save:
        fig.savefig(filename[:16] + "_" + filename_plot, dpi=300)

    if filename_plot.endswith('.png'):
        plt.show()
    else:
        plt.close()


def count_non_zero_off_diagonal(matrix_str):
    #clean rows
    rows = re.findall(r'\[\s*([^\[\]]+?)\s*\]', matrix_str)
    matrix = np.array([[float(num) for num in row.split()] for row in rows])
    # off-diagonal values
    off_diagonal_mask = ~np.eye(matrix.shape[0], dtype=bool)
    return np.count_nonzero(matrix[off_diagonal_mask])


def get_df_and_data(filename, path="../spectra_simulator"):
    metadata_filename = path + filename[:16] + "metadata.json"
    df = pd.read_csv(path + filename)
    df['spectrum'] = df['spectrum'].fillna(r'"[0]"') # Prevent error in processing later
    with open(metadata_filename, 'r') as file:
        data = json.load(file)
    return df, data
