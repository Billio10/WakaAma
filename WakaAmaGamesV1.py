import os
from tkinter import filedialog, Tk, messagebox

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
    print(f".lif files found ({count}):")
    for f in lif_files:
        print(f)
