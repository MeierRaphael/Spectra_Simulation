import os
import shutil
import subprocess
import sys


def find_matlab():
    matlab_exe = shutil.which("matlab")
    if matlab_exe:
        return matlab_exe

    possible_paths = [
        r"C:\Program Files\MATLAB\R2024b\bin\matlab.exe",
        r"C:\Program Files\MATLAB\R2024a\bin\matlab.exe",
        r"C:\Program Files\MATLAB\R2023b\bin\matlab.exe",
        r"C:\Program Files\MATLAB\R2023a\bin\matlab.exe",
    ]
    for path in possible_paths:
        if os.path.exists(path):
            print(f'Matlab Path found: {path}')
            return path
    return None


def get_matlab_version(matlab_path):
    try:
        result = subprocess.run(
            [matlab_path, "-batch", "disp(version('-release'))"],
            capture_output=True,
            text=True,
        )
        print(f'Matlab version found: {result.stdout.strip()}')
        return result.stdout.strip()
    except Exception as e:
        result = input("Couldn't find Matlab Version.\n Please enter Matlab Version (e.g. <2025a>): ")
        return result.removeprefix('<').removesuffix('>')

def get_engine_version(matlab_release):
    mapping = {
        "2025a": "25.1.2",
        "2024b": "24.2.2",
        "2024a": "24.1.4",
        "2023b": "23.2.3"
    }
    while True:
        version = mapping.get(matlab_release.lower())
        if version:
            print(f'Found version: {version}')
            return version

        matlab_release = input("Please enter your Matlab release (or <engine:>): ")
        if matlab_release.startswith("engine:"):
            engine_version = input("Please enter the Matlab.Engine version (e.g. <25.2.1>):")
            install_package("matlabengine==" + engine_version)
        else:
            possible_releases = "\n".join(mapping.keys())
            print(f"Couldn't find Matlab release '{matlab_release}'. \nHere are the possible releases: \n{possible_releases}\n Please enter your Version:  ")

def install_package(package_name):
    print(f'installing package: matlabengine=={package_name}')
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])


def setup_matlab_engine():
    matlab_path = find_matlab()

    matlab_version = get_matlab_version(matlab_path)
    engine_version = get_engine_version(matlab_version)
    install_package("matlabengine==" + engine_version)

