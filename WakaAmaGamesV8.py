import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from collections import defaultdict

# Function to read a .lif file
def read_lif_file(filepath):
    try:
        with open(filepath, 'r', encoding="latin-1") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return []
    return [line.strip() for line in lines if line.strip()]

# Function to assign points from a .lif file
def assign_points_from_lif(lif_lines):
    club_scores = defaultdict(int)

    def get_points(place):
        try:
            n = int(place)
            return 9 - n if 1 <= n <= 8 else 1
        except:
            return 0

    if not lif_lines or "Final" not in lif_lines[0]:
        return club_scores

    for line in lif_lines[1:]:  # skip header
        parts = line.split(",")
        if len(parts) < 6:
            continue

        place = parts[0].strip()
        assoc = parts[5].strip()

        if not assoc or place.upper() in ("DQ", "DNS") or place == "":
            continue

        points = get_points(place)
        assocs = [a.strip() for a in assoc.split("&")]
        for a in assocs:
            club_scores[a] += points

    return club_scores

class WakaAmaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Waka Ama Games")
        self.geometry("500x200")
        self.configure(bg="#e6f7ff")
        self.parent_folder = ""
        self.year = None
        self.create_interface()

    def create_interface(self):
        tk.Label(
            self, text="Select the parent folder and enter a year (≥ 2017):",
            font=("Arial", 12), bg="#e6f7ff"
        ).pack(pady=10)

        folder_frame = tk.Frame(self, bg="#cceeff", padx=10, pady=10)
        folder_frame.pack(pady=5, fill="x", padx=20)

        tk.Button(
            folder_frame, text="Choose Folder", font=("Arial", 12),
            bg="#99ddff", width=15, command=self.select_parent_folder
        ).pack(side="left", padx=(0,10))

        tk.Label(folder_frame, text="Enter Year:", font=("Arial", 12), bg="#cceeff").pack(side="left")
        self.year_entry = tk.Entry(folder_frame, font=("Arial", 12), width=8)
        self.year_entry.pack(side="left", padx=(5,0))
        self.year_entry.bind("<Return>", self.show_scoreboard)

    def select_parent_folder(self):
        folder = filedialog.askdirectory(title="Select Parent Folder")
        if folder:
            self.parent_folder = folder
            messagebox.showinfo("Folder Selected", f"Chosen folder:\n{folder}")

    def validate_year(self):
        year_text = self.year_entry.get().strip()
        if not year_text.isdigit() or int(year_text) < 2017:
            messagebox.showwarning("Invalid Year", "Please enter a valid year (≥ 2017).")
            return False
        if not self.parent_folder:
            messagebox.showwarning("No Folder Selected", "Please select a folder first.")
            return False
        self.year = int(year_text)
        return True

    def show_scoreboard(self, event=None):
        if not self.validate_year():
            return

        folder = os.path.join(self.parent_folder, f"WakaNats{self.year}")
        if not os.path.exists(folder):
            messagebox.showerror("Folder Not Found", f"Folder '{folder}' was not found.")
            return

        files = [f for f in os.listdir(folder) if f.lower().endswith(".lif")]
        if not files:
            messagebox.showerror("No Files Found", f"No .lif files found in '{folder}'.")
            return

        total_scores = defaultdict(int)
        final_count = 0

        for f in files:
            filepath = os.path.join(folder, f)
            lif_lines = read_lif_file(filepath)
            if lif_lines and "Final" in lif_lines[0]:
                final_count += 1
                file_scores = assign_points_from_lif(lif_lines)
                for club, points in file_scores.items():
                    total_scores[club] += points

        # Create scoreboard popup
        popup = tk.Toplevel(self)
        popup.title(f"🏆 Scoreboard – {self.year} 🏆")
        popup.geometry("650x550")
        popup.configure(bg="#f9f9f9")

        tk.Label(
            popup,
            text=f"Number of items in folder: {len(files)}\nNumber of final files: {final_count}",
            font=("Arial", 12), bg="#f9f9f9", justify="center"
        ).pack(pady=5)

        columns = ("Rank", "Association", "Points")
        tree = ttk.Treeview(popup, columns=columns, show="headings", height=15)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=180 if col != "Rank" else 70)
        tree.pack(fill="both", expand=True, padx=15, pady=15)

        sorted_scores = sorted(total_scores.items(), key=lambda x: x[1], reverse=True)
        for rank, (club, points) in enumerate(sorted_scores, 1):
            tree.insert("", "end", values=(rank, club, points))

        tk.Button(
            popup, text="Return", font=("Arial", 12), bg="#ffcccc",
            command=popup.destroy
        ).pack(pady=10)


# Run the app
if __name__ == "__main__":
    app = WakaAmaApp()
    app.mainloop()
