# Waka Ama Games Score Calculator  
A Python GUI tool that calculates Waka Ama club standings from `.lif` race files, displays rankings, and exports results to CSV.  
## Features  
* Reads `.lif` files and processes only Finals results.  
* Assigns points based on placement (handles ties and multiple associations).  
* Displays an interactive scoreboard by year (≥2017).  
* Exports standings to CSV.  
## Requirements  
* Python 3.x  
* `tkinter` (GUI), `csv`, `os`, `collections`  
## Usage  
1. Run the script:  
2. Click **Choose Folder** to select the parent folder containing `WakaNatsYYYY` folders.  
3. Enter a **Year (≥2017)** and press **Enter**.  
4. View the scoreboard popup and export results if desired.  
## Points System  
* 1st → 8 points, 2nd → 7 points … 8th → 1 point  
* Ties share points; multiple associations separated by `&` each get full points.  


