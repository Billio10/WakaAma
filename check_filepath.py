def folder_reader(self, folder_path, year):
    final_files_dict = {}
    ranking_dict = {}
    try:
        # Look for year folder inside selected folder
        year_folder = None
        for entry in os.listdir(folder_path):
            if str(year) in entry and os.path.isdir(os.path.join(folder_path, entry)):
                year_folder = os.path.join(folder_path, entry)
                break
        if not year_folder:
            self.ranker_desc.config(text=f"No folder found for year {year},")
            return

        files = os.listdir(year_folder)
        for file in files:
            if "final" in file.lower() and file.lower().endswith(".lif"):
                final_files_dict[file] = os.path.join(year_folder, file)
                self.ranker_desc.config(text=f"Below is a preview of the rankings. To download the file as a .csv file, "
                                             f"click 'Export to csv'. Number of items in folder: {len(files)}. Number "
                                             f"of final files: {len(final_files_dict)}")

        self.results.grid(row=2, column=0, sticky="nswe", padx=50,  pady=50)
        self.results.insert(0, "Loading, please wait...")
        self.scrollbar.config(command=self.results.yview)
        self.frate.update()
        for key, value in final_files_dict.items():
            self.file_reader(key, value, ranking_dict)
        self.ranking_results()
        self.label.config(text="")
        self.csv_button.config(state=NORMAL)
    except Exception as e:
        self.label.config(text=f"Failed to read folder: {e}", fg="red")
