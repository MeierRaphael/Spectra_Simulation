import pandas as pd
import matplotlib.pyplot as plt
import ast
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
import numpy as np

# Ask the user for the filename
filename = input("Enter the path to the CSV file: ")

# Load the CSV
df = pd.read_csv(filename)

# Convert 'Index' from string to actual list and get their lengths
df['matrix_size'] = df['Index'].apply(lambda x: len(ast.literal_eval(x)))

# Sort by computation_time
df_sorted = df.sort_values(by='computation_time')

# Prepare data

X = df_sorted['matrix_size'].values.reshape(-1, 1)
y = df_sorted['computation_time'].values

# Polynomial regression model
degree = 2
model = make_pipeline(PolynomialFeatures(degree=degree), LinearRegression())
model.fit(X, y)

# Generate predictions
x_range = np.linspace(X.min(), (X.max() * 1.2), 200).reshape(-1, 1)
y_pred = model.predict(x_range)

# Plot scatter and regression curve
plt.figure(figsize=(10, 6))
plt.scatter(X, y, c='blue', alpha=0.7, label='Data')
plt.plot(x_range, y_pred, color='red', linewidth=2, label=f'Polynomial Regression (degree={degree})')
plt.xlabel('Number of Spins')
plt.ylabel('Computation Time (s)')
plt.title('Computation Time for H1 NMR')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


# number of non-zero values in the matrix agains time
# number of spins instead of matrix size
