import os
from tkinter import filedialog, Tk, messagebox

# Function to read a .lif file
def read_lif_file(filepath):
    """Read a .lif file and return lines (keeps all lines)."""
    try:
        with open(filepath, 'r', encoding="latin-1") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return []
    return [line.strip() for line in lines if line.strip()]

# Hide the main Tkinter window
root = Tk()
root.withdraw()

# Ask the user to select a folder
folder = filedialog.askdirectory(title="Select Folder Containing .lif Files")

if not folder:
    messagebox.showinfo("No Folder Selected", "No folder was selected. Exiting.")
else:
    # List all files in the folder that end with .lif (case-insensitive)
    lif_files = [f for f in os.listdir(folder) if f.lower().endswith(".lif")]
    count = len(lif_files)

    # Show the result
    messagebox.showinfo("LIF File Count", f"Number of .lif files in the folder:\n{count}")
    print(f"Folder: {folder}")
    print(f".lif files found ({count}):\n")

    # Read and print contents of each .lif file
    for f in lif_files:
        filepath = os.path.join(folder, f)
        lif_lines = read_lif_file(filepath)
        print(f"--- {f} ---")
        for line in lif_lines:
            print(line)
        print("\n")  # Add a blank line between files
