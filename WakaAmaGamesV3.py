import os
import tkinter as tk
from tkinter import scrolledtext, ttk
from collections import defaultdict

# Base folder where your WakaNats folders are stored
BASE_PATH = r"C:\Users\qle78\OneDrive - Papatoetoe High School\Documents\DTP3\Waka Ama\3.7B resource files\3.7B resource files"

#Helper functions
def read_lif_file(filepath):
    """Read a .lif file and return lines."""
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        return []
    return [line.strip() for line in lines if line.strip()]

def assign_points_from_lif(lif_lines):
    """
    Extract club points from a .lif file.
    Simplified: assign points based on placement for lines containing 'Final'.
    """
    place_points = {1: 8, 2: 7, 3: 6, 4: 5, 5: 4, 6: 3, 7: 2, 8: 1}
    club_scores = defaultdict(int)

    current_race = []
    for line in lif_lines:
        if "Final" in line:
            if current_race:
                # Process previous race
                for race_line in current_race:
                    parts = race_line.split(",")
                    if len(parts) > 5:
                        try:
                            place = int(parts[0])
                            club = parts[5].strip()
                            if club:
                                club_scores[club] += place_points.get(place, 1)
                        except ValueError:
                            continue
            current_race = []
        else:
            current_race.append(line)
    #Process last race
    for race_line in current_race:
        parts = race_line.split(",")
        if len(parts) > 5:
            try:
                place = int(parts[0])
                club = parts[5].strip()
                if club:
                    club_scores[club] += place_points.get(place, 1)
            except ValueError:
                continue
    return club_scores

class WakaAmaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Waka Ama Games")
        self.geometry("700x500")
        self.configure(bg="#e6f7ff")
        self.selected_year = None
        self.show_interface()

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    def analyze_year(self, year):
        self.selected_year = year
        folder = os.path.join(BASE_PATH, f"WakaNats{year}")

        self.result_text.delete(1.0, tk.END)
        for row in self.tree.get_children():
            self.tree.delete(row)

        if os.path.exists(folder):
            files = [f for f in os.listdir(folder) if f.lower().endswith(".lif")]
            self.result_text.insert(tk.END, f"Found {len(files)} .lif files in {folder}\n")
            total_scores = defaultdict(int)
            for f in files:
                lif_lines = read_lif_file(os.path.join(folder, f))
                file_scores = assign_points_from_lif(lif_lines)
                for club, points in file_scores.items():
                    total_scores[club] += points
            #Sort clubs by points
            sorted_scores = sorted(total_scores.items(), key=lambda x: x[1], reverse=True)
            #Insert into Treeview
            for rank, (club, points) in enumerate(sorted_scores, 1):
                self.tree.insert("", "end", values=(rank, club, points))
        else:
            self.result_text.insert(tk.END, f"Folder '{folder}' was not found\n")

    def show_interface(self):
        self.clear_screen()
        tk.Label(self, text="Waka Ama Games", font=("Arial", 18, "bold"), bg="#e6f7ff").pack(pady=15)

        year_frame = tk.Frame(self, bg="#cceeff", padx=10, pady=10)
        year_frame.pack(pady=10, fill="x", padx=20)

        tk.Label(year_frame, text="Select a year to analyze:", font=("Arial", 14), bg="#cceeff").pack(pady=5)
        tk.Button(year_frame, text="2017", font=("Arial", 12), width=20, bg="#99ddff",
                  command=lambda: self.analyze_year("2017")).pack(pady=5)
        tk.Button(year_frame, text="2018", font=("Arial", 12), width=20, bg="#99ddff",
                  command=lambda: self.analyze_year("2018")).pack(pady=5)

        result_frame = tk.Frame(self, bg="#f0f8ff", padx=10, pady=10)
        result_frame.pack(pady=10, fill="both", expand=True, padx=20)

        tk.Label(result_frame, text="Results:", font=("Arial", 14), bg="#f0f8ff").pack(anchor="w")
        self.result_text = scrolledtext.ScrolledText(result_frame, width=50, height=6, font=("Arial", 10))
        self.result_text.pack(fill="x", expand=False)

        tk.Label(result_frame, text="Standings Table:", font=("Arial", 14), bg="#f0f8ff").pack(anchor="w", pady=(10,0))
        columns = ("Rank", "Association", "Points")
        self.tree = ttk.Treeview(result_frame, columns=columns, show="headings", height=12)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)
        self.tree.pack(fill="both", expand=True)

# Run
if __name__ == "__main__":
    app = WakaAmaApp()
    app.mainloop()
