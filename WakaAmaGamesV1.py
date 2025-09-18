import os

# === Base folder where your WakaNats folders are stored ===
base_path = r"C:\Users\qle78\OneDrive - Papatoetoe High School\Documents\DTP3\Waka Ama\3.7B resource files\3.7B resource files"

# user input for which year they want to analyze
year = input("Enter the year you want to analyze (2017 or 2018): ").strip()
folder = os.path.join(base_path, f"WakaNats{year}")

# To check if folder exists
if os.path.exists(folder):
    files = os.listdir(folder)

    # This code only takes files that are lif
    lif_files = [file for file in files if file.lower().endswith('.lif')]
   
    # Outputs the number of lif files
    print(f"Found {len(lif_files)} .lif files in {folder}")
else:
    print(f"Folder '{folder}' was not found")
