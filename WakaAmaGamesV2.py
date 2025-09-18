import os
import tkinter as tk
from tkinter import scrolledtext

# Base folder where your WakaNats folders are stored
BASE_PATH = r"C:\Users\qle78\OneDrive - Papatoetoe High School\Documents\DTP3\Waka Ama\3.7B resource files\3.7B resource files"

class WakaAmaApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Main window setup
        self.title("Waka Ama Games")
        self.geometry("450x350")
        self.configure(bg="#e6f7ff")  # Light blue background
        self.selected_year = None

        # Show main interface
        self.show_interface()

    # Clear all widgets
    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    # Analyze the selected year
    def analyze_year(self, year):
        self.selected_year = year
        folder = os.path.join(BASE_PATH, f"WakaNats{year}")

        self.result_text.delete(1.0, tk.END)  # Clear previous results

        if os.path.exists(folder):
            files = os.listdir(folder)
            lif_files = [file for file in files if file.lower().endswith('.lif')]
            self.result_text.insert(tk.END, f"Found {len(lif_files)} .lif files in {folder}\n")
            for f in lif_files:
                self.result_text.insert(tk.END, f"{f}\n")
        else:
            self.result_text.insert(tk.END, f"Folder '{folder}' was not found\n")

    # Show interface
    def show_interface(self):
        self.clear_screen()

        # Title
        tk.Label(self, text="Waka Ama Games", font=("Arial", 18, "bold"), bg="#e6f7ff").pack(pady=15)

        # Year selection frame
        year_frame = tk.Frame(self, bg="#cceeff", padx=10, pady=10)
        year_frame.pack(pady=10, fill="x", padx=20)

        tk.Label(year_frame, text="Select a year to analyze:", font=("Arial", 14), bg="#cceeff").pack(pady=5)

        tk.Button(year_frame, text="2017", font=("Arial", 12), width=20, bg="#99ddff",
                  command=lambda: self.analyze_year("2017")).pack(pady=5)
        tk.Button(year_frame, text="2018", font=("Arial", 12), width=20, bg="#99ddff",
                  command=lambda: self.analyze_year("2018")).pack(pady=5)

        # Result area
        result_frame = tk.Frame(self, bg="#f0f8ff", padx=10, pady=10)
        result_frame.pack(pady=10, fill="both", expand=True, padx=20)

        tk.Label(result_frame, text="Results:", font=("Arial", 14), bg="#f0f8ff").pack(anchor="w")

        self.result_text = scrolledtext.ScrolledText(result_frame, width=50, height=10, font=("Arial", 10))
        self.result_text.pack(fill="both", expand=True)

# Start the program
if __name__ == "__main__":
    app = WakaAmaApp()
    app.mainloop()
