import os
import csv
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from collections import defaultdict

# Helper functions
def read_lif_file(filepath):
    try:
        with open(filepath, 'r', encoding="latin-1") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return []
    return [line.strip() for line in lines if line.strip()]

def assign_points_from_lif(lif_lines):
    club_scores = defaultdict(int)
    prev_place = None
    prev_points = 0

    def get_points(place):
        try:
            n = int(place)
            return 9 - n if 1 <= n <= 8 else 1
        except:
            return 0

    if not lif_lines or "Final" not in lif_lines[0]:
        return club_scores

    for line in lif_lines[1:]:
        parts = line.split(",")
        if len(parts) < 6:
            continue

        place = parts[0].strip()
        assoc = parts[5].strip()
        if not assoc or place.upper() in ("DQ", "DNS") or place == "":
            continue

        points = get_points(place)
        if place == prev_place:
            points = prev_points
        else:
            prev_place = place
            prev_points = points

        assocs = [a.strip() for a in assoc.split("&")]
        for a in assocs:
            club_scores[a] += points

    return club_scores

class WakaAmaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Waka Ama Games")
        self.geometry("550x300")
        self.configure(bg="#e6f7ff")
        self.total_scores = defaultdict(int)
        self.parent_folder = ""
        self.show_interface()

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    def select_parent_folder(self):
        folder = filedialog.askdirectory(title="Choose Folder")
        if folder:
            self.parent_folder = folder
            messagebox.showinfo("Folder Selected", f"Chosen folder:\n{folder}")

    def process_year(self, event=None):
        year = self.year_entry.get().strip()
        if not year.isdigit() or int(year) < 2017:
            messagebox.showwarning("Invalid Year", "Please enter a valid year (≥ 2017).")
            return
        if not self.parent_folder:
            messagebox.showwarning("No Folder Selected", "Please select a folder first.")
            return

        folder = os.path.join(self.parent_folder, f"WakaNats{year}")
        if not os.path.exists(folder):
            messagebox.showerror("Folder Not Found", f"Folder '{folder}' was not found")
            return

        files = [f for f in os.listdir(folder) if f.lower().endswith(".lif")]
        if not files:
            messagebox.showinfo("No Files Found", f"No .lif files found in {folder}.")
            return

        self.total_scores = defaultdict(int)
        final_count = 0
        total_files = len(files)

        # Progress window
        progress_win = tk.Toplevel(self)
        progress_win.title(f"Processing {year}")
        progress_win.geometry("500x400")
        progress_win.configure(bg="#f0f9ff")

        tk.Label(
            progress_win,
            text=f"Year being processed: {year}",
            font=("Arial", 14, "bold"),
            bg="#f0f9ff"
        ).pack(pady=10)

        file_label = tk.Label(
            progress_win,
            text="",
            font=("Arial", 11),
            bg="#f0f9ff",
            justify="left"
        )
        file_label.pack(pady=10)

        summary_label = tk.Label(
            progress_win,
            text=f"Total files: {total_files}\nFinal files: {final_count}",
            font=("Arial", 12, "bold"),
            bg="#f0f9ff"
        )
        summary_label.pack(pady=10)

        # Process each file
        for i, f in enumerate(files, 1):
            filepath = os.path.join(folder, f)
            lif_lines = read_lif_file(filepath)

            if lif_lines and "Final" in lif_lines[0]:
                final_count += 1
                file_scores = assign_points_from_lif(lif_lines)
                for club, points in file_scores.items():
                    self.total_scores[club] += points

            # Update popup text
            file_label.config(text=f"Processing file {i}/{total_files}: {f}")
            summary_label.config(text=f"Total files: {total_files}\nFinal files: {final_count}")
            progress_win.update_idletasks()

        # Keep popup visible for 2 seconds after processing
        progress_win.after(2000, lambda: [progress_win.destroy(), self.show_scoreboard(year)])

    def show_scoreboard(self, year):
        popup = tk.Toplevel(self)
        popup.title(f"Ranking Calculator - {year}")
        popup.geometry("650x550")
        popup.configure(bg="#f9f9f9")

        tk.Label(
            popup,
            text=f"🏆 Scoreboard – {year} 🏆",
            font=("Arial", 16, "bold"),
            bg="#f9f9f9",
            fg="#004080"
        ).pack(pady=15)

        columns = ("Rank", "Association", "Points")
        tree = ttk.Treeview(popup, columns=columns, show="headings", height=15)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=180 if col != "Rank" else 70)
        tree.pack(fill="both", expand=True, padx=15, pady=15)

        sorted_scores = sorted(self.total_scores.items(), key=lambda x: x[1], reverse=True)
        for rank, (club, points) in enumerate(sorted_scores, 1):
            tree.insert("", "end", values=(rank, club, points))

        btn_frame = tk.Frame(popup, bg="#f9f9f9")
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame, text="Export to CSV", font=("Arial", 12),
            bg="#99ddff", command=self.export_csv
        ).pack(side="left", padx=10)

        tk.Button(
            btn_frame, text="Return", font=("Arial", 12),
            bg="#ffcccc", command=popup.destroy
        ).pack(side="left", padx=10)

    def export_csv(self):
        if not self.total_scores:
            messagebox.showwarning("Export Error", "No data to export. Process a year first.")
            return

        file_path = filedialog.asksaveasfilename(
            title="Save CSV",
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")]
        )
        if not file_path:
            return

        try:
            with open(file_path, 'w', newline='', encoding="utf-8") as csvfile:
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
        tk.Label(
            self, text="Waka Ama Games",
            font=("Arial", 20, "bold"), bg="#e6f7ff", fg="#004080"
        ).pack(pady=10)

        tk.Label(
            self,
            text="Select the parent folder and enter a year (≥ 2017)\n"
                 "Press Enter to generate the scoreboard.",
            font=("Arial", 12),
            bg="#e6f7ff"
        ).pack(pady=5)

        folder_frame = tk.Frame(self, bg="#cceeff", padx=10, pady=10)
        folder_frame.pack(pady=5, fill="x", padx=20)
        tk.Button(folder_frame, text="Choose Folder", font=("Arial", 12), width=20, bg="#99ddff",
                  command=self.select_parent_folder).pack(side="left", padx=(0, 10))

        tk.Label(folder_frame, text="Enter Year:", font=("Arial", 12), bg="#cceeff").pack(side="left")
        self.year_entry = tk.Entry(folder_frame, font=("Arial", 12), width=10)
        self.year_entry.pack(side="left", padx=(5, 0))
        self.year_entry.bind("<Return>", self.process_year)

if __name__ == "__main__":
    app = WakaAmaApp()
    app.mainloop()
