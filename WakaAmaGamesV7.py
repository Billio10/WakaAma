import os
import tkinter as tk
from tkinter import filedialog, messagebox

class Sprint3Input:
    def __init__(self):
        self.parent_folder = ""
        self.year = None
        self.root = tk.Tk()
        self.root.title("Waka Ama Year Selection")
        self.root.geometry("400x150")
        self.root.configure(bg="#e6f7ff")
        self.create_interface()
        self.root.mainloop()

    def create_interface(self):
        tk.Label(
            self.root, text="Select the parent folder and enter a year (≥ 2017):",
            font=("Arial", 12), bg="#e6f7ff"
        ).pack(pady=10)

        folder_frame = tk.Frame(self.root, bg="#cceeff", padx=10, pady=10)
        folder_frame.pack(pady=5, fill="x", padx=20)

        tk.Button(
            folder_frame, text="Choose Folder", font=("Arial", 12),
            bg="#99ddff", width=15, command=self.select_parent_folder
        ).pack(side="left", padx=(0,10))

        tk.Label(folder_frame, text="Enter Year:", font=("Arial", 12), bg="#cceeff").pack(side="left")
        self.year_entry = tk.Entry(folder_frame, font=("Arial", 12), width=8)
        self.year_entry.pack(side="left", padx=(5,0))
        self.year_entry.bind("<Return>", self.process_inputs)

    def select_parent_folder(self):
        folder = filedialog.askdirectory(title="Select Parent Folder")
        if folder:
            self.parent_folder = folder
            messagebox.showinfo("Folder Selected", f"Chosen folder:\n{folder}")

    def validate_year(self):
        """Check that year is ≥ 2017 and folder exists."""
        year_text = self.year_entry.get().strip()
        if not year_text.isdigit() or int(year_text) < 2017:
            messagebox.showwarning("Invalid Year", "Please enter a valid year (≥ 2017).")
            return False
        if not self.parent_folder:
            messagebox.showwarning("No Folder Selected", "Please select a folder first.")
            return False
        self.year = int(year_text)
        return True

    def process_inputs(self, event=None):
        if self.validate_year():
            messagebox.showinfo("Inputs Validated", f"Year: {self.year}\nFolder: {self.parent_folder}")


# Run 
if __name__ == "__main__":
    Sprint3Input()
