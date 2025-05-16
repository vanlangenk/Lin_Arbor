import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import Toplevel, Label, Button
import webbrowser
import cv2

# === CONFIGURATION ===
image_path = r"C:\Users\kenne\Lin_Arbor\data\ndvi_map.png"
csv_path = r"C:\Users\kenne\Lin_Arbor\data\linwood_species_inventory.csv"
output_path = r"C:\Users\kenne\Lin_Arbor\docs\plant_overlay.png"
show_grid = False
font_size = 6
grid_interval = 500

# === LOAD IMAGE AND DATA ===
img = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
df = pd.read_csv(csv_path)

# === POPUP WINDOW ===
def show_popup(row):
    win = Toplevel()
    win.title(f"{row['Common Name']} ({row['Scientific Name']})")

    Label(win, text=f"Common Name: {row['Common Name']}", anchor='w').pack(fill='x')
    Label(win, text=f"Scientific Name: {row['Scientific Name']}", anchor='w', fg='blue', cursor='hand2').bind(
        "<Button-1>", lambda e: open_plantnet(row['Scientific Name'])
    ).pack(fill='x')
    Label(win, text=f"Zone: {row['Zone']}", anchor='w').pack(fill='x')
    Label(win, text=f"Light Preference: {row['Light Preference']}", anchor='w').pack(fill='x')
    Label(win, text=f"Appearance: {row['Appearance']}", anchor='w').pack(fill='x')

    Button(win, text="Search PlantNet", command=lambda: open_plantnet(row['Scientific Name'])).pack(pady=5)

# === PLANTNET SEARCH ===
def open_plantnet(scientific_name):
    sci_name = scientific_name.strip().replace(' ', '+')
    url = f"https://identify.plantnet.org/search?query={sci_name}"
    webbrowser.open_new(url)

# === TOGGLE GRID ===
def toggle_grid(event):
    global show_grid
    if event.key == 'control':
        show_grid = not show_grid
        render()

# === CLICK EVENT ===
def on_click(event):
    if event.xdata is None or event.ydata is None:
        return
    for _, row in df.iterrows():
        try:
            x, y = int(row['x']), int(row['y'])
            dist = np.hypot(event.xdata - x, event.ydata - y)
            if dist < 20:
                show_popup(row)
                break
        except:
            continue

# === RENDER FUNCTION ===
def render():
    plt.close('all')
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.imshow(img)

    if show_grid:
        ax.set_xticks(np.arange(0, img.shape[1], grid_interval))
        ax.set_yticks(np.arange(0, img.shape[0], grid_interval))
        ax.grid(True, color='gray', linestyle='--', linewidth=0.5)
        for x in np.arange(0, img.shape[1], grid_interval):
            for y in np.arange(0, img.shape[0], grid_interval):
                ax.text(x, y, f"({x},{y})", fontsize=5, color='black')

    for _, row in df.iterrows():
        try:
            x, y = int(row['x']), int(row['y'])
            common = row['Common Name'].strip()
            scientific = row['Scientific Name'].strip()
            label = f"{common}\n({scientific})"
            ax.text(x, y, label, fontsize=font_size, color='red',
                    bbox=dict(facecolor='yellow', alpha=0.5, boxstyle='round,pad=0.3'))
        except:
            continue

    ax.set_title("Lin Arbor Plant Overlay")
    ax.set_xlabel("X coordinate (pixels)")
    ax.set_ylabel("Y coordinate (pixels)")
    fig.canvas.mpl_connect('button_press_event', on_click)
    fig.canvas.mpl_connect('key_press_event', toggle_grid)
    plt.savefig(output_path)
    plt.show()

render()
