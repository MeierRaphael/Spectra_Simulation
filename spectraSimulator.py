import matlab.engine
import pandas as pd
import helper.setup_matlab_engine
import json
import subprocess


from helper.format_values import MatlabDoubleEncoder
from helper.clean_csv import clean_csv

setup = False   #set True if you want automatic installation of correct matlab.engine
if setup:
    helper.setup_matlab_engine.setup_matlab_engine()

# -------------------------- ORCA addition -------------------------------
# orca_exe = "/path/to/orca"
# input_file = "my_calculation.inp" # Path to ORCA input file
# subprocess.run([orca_exe, input_file]) # Run ORCA

# -------------------------- verify Parameters --------------------------
parameters = {
    'filename': r'data\gissmo_spin_matrix.csv', #replace with ORCA output file
    'approx': 'none',
    'approx_level': matlab.double([int(1)]),
    'windowSize_ppm': matlab.double([int(13)]),
    'offset_ppm': matlab.double([int(-1)]),
    'npoints': matlab.double([int(4000)]),
    'formalism': 'sphten-liouv',
    'apodisation': 'exp',
    'apodisation_level': matlab.double([int(2)]),
    'x': 'all',
}

print("Parameters (single number for approx_level):")
print(json.dumps(parameters, indent=4, cls=MatlabDoubleEncoder))

start_calculations = False
while not start_calculations:
    parameter = input("Type the parameter you want to change (e.g. [npoints]) or type [done] to start the calculations: ")
    if parameter == "done":
        start_calculations = True
    elif parameter in parameters:
        value = input(f'Enter new value for {parameter}: ')
        if parameter in ["approx_level", "windowSize_ppm", "offset_ppm", "npoints"]:
            value = matlab.double([int(value)])
        else:
            value = str(value)

        parameters[parameter] = value
    else: print(f"{parameter} is no valid input")
clean_csv(parameters.get('filename'), 'data/temp_dataset.csv')

param_list = []
for key, value in parameters.items():
    param_list.append(key)
    param_list.append(value)

# -------------------------- Start MATLAB engine --------------------------
eng = matlab.engine.start_matlab()
eng.cd(r'spectra_simulator', nargout=0)
eng.spectra_simulator(*param_list, nargout=0)
eng.quit()

# Matlab 2023b or 2024b is used. python 3.11 is compatible for both and the correct engine will be installed via pip install.
#pip install matlabengine==24.2.2

# Versions:
# if version 2023b or higher: use venv with python 3.11 and make adaptive pip install of matlab engine
# version 2023a-2022a: 3.10
# version 2022a-2021b: 3.9
