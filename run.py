import os
import shutil
import subprocess
import sys

def copy_and_run_executable(source_executable, destination_folder):
    # Ensure the destination folder exists
    os.makedirs(destination_folder, exist_ok=True)

    # Define the destination path for the copied executable
    destination_path = os.path.join(destination_folder, os.path.basename(source_executable))

    # Copy the executable
    shutil.copy(source_executable, destination_path)
    print(f"Copied {source_executable} to {destination_path}")

    # Run the copied executable
    subprocess.run([destination_path], check=True)

if __name__ == "__main__":
    # Specify the source executable and the destination folder
    source_executable = "swhost.exe"  # Change this to the name of your executable
    destination_folder = os.path.join(os.path.expanduser("~"), "Desktop")  # Change this if needed

    try:
        copy_and_run_executable(source_executable, destination_folder)
    except Exception as e:
        print(f"An error occurred: {e}")