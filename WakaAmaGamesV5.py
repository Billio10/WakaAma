import os
import csv
import tkinter as tk
from tkinter import scrolledtext, ttk, filedialog, messagebox
from collections import defaultdict

# Helper functions
def read_lif_file(filepath):
    """Read a .lif file and return lines."""
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        return []
    return [line.strip() for line in lines if line.strip()]

def assign_points_from_lif(lif_lines):
    """Extract club points from a .lif file based on 'Final' races, splitting points for combined clubs."""
    place_points = {1: 8, 2: 7, 3: 6, 4: 5, 5: 4, 6: 3, 7: 2, 8: 1}
    club_scores = defaultdict(int)

    current_race = []
    for line in lif_lines:
        if "Final" in line:
            if current_race:
                for race_line in current_race:
                    parts = race_line.split(",")
                    if len(parts) > 5:
                        try:
                            place = int(parts[0])
                            club = parts[5].strip()
                            if club:
                                # Split combined clubs and divide points evenly
                                clubs = [c.strip() for c in club.split("/")]
                                points = place_points.get(place, 1)
                                split_points = points / len(clubs)
                                for c in clubs:
                                    club_scores[c] += split_points
                        except ValueError:
                            continue
            current_race = []
        else:
            current_race.append(line)
    # Process last race
    for race_line in current_race:
        parts = race_line.split(",")
        if len(parts) > 5:
            try:
                place = int(parts[0])
                club = parts[5].strip()
                if club:
                    clubs = [c.strip() for c in club.split("/")]
                    points = place_points.get(place, 1)
                    split_points = points / len(clubs)
                    for c in clubs:
                        club_scores[c] += split_points
            except ValueError:
                continue
    return club_scores

class WakaAmaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Waka Ama Games")
        self.geometry("700x550")
        self.configure(bg="#e6f7ff")
        self.total_scores = defaultdict(int)
        self.show_interface()

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    def analyze_folder(self, folder):
        """Analyze all .lif files in the selected folder."""
        self.result_text.delete(1.0, tk.END)
        for row in self.tree.get_children():
            self.tree.delete(row)

        if os.path.exists(folder):
            files = [f for f in os.listdir(folder) if f.lower().endswith(".lif")]
            self.result_text.insert(tk.END, f"Found {len(files)} .lif files in {folder}\n")
            self.total_scores = defaultdict(int)
            for f in files:
                lif_lines = read_lif_file(os.path.join(folder, f))
                file_scores = assign_points_from_lif(lif_lines)
                for club, points in file_scores.items():
                    self.total_scores[club] += points
            # Sort clubs by points
            sorted_scores = sorted(self.total_scores.items(), key=lambda x: x[1], reverse=True)
            # Insert into Treeview
            for rank, (club, points) in enumerate(sorted_scores, 1):
                self.tree.insert("", "end", values=(rank, club, points))
        else:
            self.result_text.insert(tk.END, f"Folder '{folder}' was not found\n")

    def select_folder(self):
        folder = filedialog.askdirectory(title="Select Folder with .lif Files")
        if folder:
            self.analyze_folder(folder)

    def export_csv(self):
        """Export the current Treeview standings to a CSV file."""
        if not self.total_scores:
            messagebox.showwarning("Export Error", "No data to export. Analyze a folder first.")
            return

        file_path = filedialog.asksaveasfilename(
            title="Save CSV",
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")]
        )
        if not file_path:
            return

        try:
            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Rank", "Association", "Points"])
                sorted_scores = sorted(self.total_scores.items(), key=lambda x: x[1], reverse=True)
                for rank, (club, points) in enumerate(sorted_scores, 1):
                    writer.writerow([rank, club, points])
            messagebox.showinfo("Export Successful", f"Standings exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Export Failed", str(e))

    def show_interface(self):
        self.clear_screen()
        tk.Label(self, text="Waka Ama Games", font=("Arial", 18, "bold"), bg="#e6f7ff").pack(pady=15)

        # Folder selection
        folder_frame = tk.Frame(self, bg="#cceeff", padx=10, pady=10)
        folder_frame.pack(pady=10, fill="x", padx=20)
        tk.Button(folder_frame, text="Select Folder", font=("Arial", 12), width=20, bg="#99ddff",
                  command=self.select_folder).pack(pady=5)

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

        # Export button
        tk.Button(result_frame, text="Export CSV", bg="#99ddff", font=("Arial", 12), command=self.export_csv).pack(pady=10)

# Run
if __name__ == "__main__":
    app = WakaAmaApp()
    app.mainloop()
