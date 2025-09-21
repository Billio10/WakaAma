import os
from collections import defaultdict
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

# Function to assign points from a .lif file 
def assign_points_from_lif(lif_lines):
    """Extract club points from a .lif file if it is a Final race file."""
    club_scores = defaultdict(int)

    # Helper function to calculate points based on place
    def get_points(place):
        try:
            n = int(place)
            return 9 - n if 1 <= n <= 8 else 1
        except:
            return 0

    # Only process Finals (check first line)
    if not lif_lines or "Final" not in lif_lines[0]:
        return club_scores

    # Process results line by line
    for line in lif_lines[1:]:  # skip header
        parts = line.split(",")
        if len(parts) < 6:
            continue

        place = parts[0].strip()
        assoc = parts[5].strip()

        # Skip invalid rows
        if not assoc or place.upper() in ("DQ", "DNS") or place == "":
            continue

        points = get_points(place)
        club_scores[assoc] += points

    return club_scores


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

    total_scores = defaultdict(int)

    # Read and process contents of each .lif file
    for f in lif_files:
        filepath = os.path.join(folder, f)
        lif_lines = read_lif_file(filepath)
        print(f"--- {f} ---")

        # Assign points only if it’s a Final file
        file_scores = assign_points_from_lif(lif_lines)
        for club, points in file_scores.items():
            total_scores[club] += points

        # Print the file lines (for checking)
        for line in lif_lines:
            print(line)
        print("\n")  # Add a blank line between files

    # Print overall scores at the end
    print("=== Total Scores Across All Files ===")
    for club, points in total_scores.items():
        print(f"{club}: {points}")
