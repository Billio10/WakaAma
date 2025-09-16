import os
import csv
from tkinter import Tk, StringVar, messagebox, filedialog
from tkinter import ttk
from collections import defaultdict
from PIL import Image, ImageTk
import tkinter as tk


# === Data Processing Functions ===

def read_lif_file(filepath):
    """Read a .lif file and group its races by 'Final' markers."""
    try:
        with open(filepath, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        return []

    races, current_race = [], []
    for line in lines:
        line = line.strip()
        if "Final" in line:
            if current_race:
                races.append(current_race)
            current_race = [line]
        elif current_race:
            current_race.append(line)
    if current_race:
        races.append(current_race)
    return races


def assign_points(races, club_scores):
    """Assign points to clubs based on race results."""
    place_points = {1: 8, 2: 7, 3: 6, 4: 5, 5: 4, 6: 3, 7: 2, 8: 1}
    for race in races:
        results = []
        for line in race[1:]:
            parts = line.split(",")
            if len(parts) > 5:
                placing, club_name = parts[0].strip(), parts[5].strip()
                if placing.upper() not in ("DQ", "DNS") and club_name:
                    try:
                        results.append((int(placing), club_name))
                    except ValueError:
                        continue
        results.sort()

        i = 0
        while i < len(results):
            place = results[i][0]
            tied_clubs = [results[i][1]]
            j = i + 1
            while j < len(results) and results[j][0] == place:
                tied_clubs.append(results[j][1])
                j += 1

            points = place_points.get(place, 1)
            for club in tied_clubs:
                club_scores[club] += points
            i = j


def save_results_to_csv(scores, output_file):
    """Save results to CSV, sorted by points descending."""
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Rank', 'Club Name', 'Points'])
        for rank, (club, points) in enumerate(sorted_scores, 1):
            writer.writerow([rank, club, points])


def should_include_folder(folder_name, year_filter):
    """Check if folder matches selected year (if given)."""
    if not year_filter:
        return True
    try:
        folder_year = int(''.join(filter(str.isdigit, folder_name)))
        return folder_year == int(year_filter)
    except ValueError:
        return False
