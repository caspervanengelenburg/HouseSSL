import numpy as np
from matplotlib.cm import get_cmap
import matplotlib.colors as mcolors

# some nice colors
delft_color = "#00A6D6" # TU Delft light blue color
google_colors = ["#4285F4", # blue
                 "#DB4437", # red
                 "#F4B400", # yellow
                 "#0F9D58"  # green
                 ]


# Custom coloring schemes
COLORS_RPLAN = ['#e6550d',  # living room
                '#1f77b4',  # master room
                '#fd8d3c',  # kitchen
                '#6b6ecf',  # bathroom
                '#fdae6b',  # dining room
                '#d3d3d3',  # child room
                '#d3d3d3',  # study room
                '#1f77b4',  # second room
                '#1f77b4',  # guest room
                '#2ca02c',  # balcony
                '#fdd0a2',  # entrance
                '#5254a3',  # storage
                '#5254a3',  # walk-in
                '#000000',  # external area
                '#ffffff',  # exterior wall
                '#ffa500',  # front door
                '#ffffff',  # interior wall
                '#ff0000']  # interior door

COLORS_LIFULL = ['#e6550d',  # living room
                 '#fd8d3c',  # kitchen
                 '#1f77b4',  # bedroom
                 '#6b6ecf',  # bathroom
                 '#808080',  # missing (todo: better color)
                 '#5254a3',  # closet
                 '#2ca02c',  # balcony
                 '#fdd0a2',  # corridor
                 '#fdae6b',  # dining room
                 '#d3d3d3']  # laundry room (todo: better color)

COLORS_MSD = ['#1f77b4',  # bedroom
              '#e6550d',  # living room
              '#fd8d3c',  # kitchen
              '#fdae6b',  # dining
              '#fdd0a2',  # corridor
              '#72246c',  # stairs
              '#5254a3',  # storeroom
              '#6b6ecf',  # bathroom
              '#2ca02c',  # balcony
              '#000000',  # structure
              '#ffc000',  # door
              '#98df8a',  # entrance door
              '#d62728']  # window

# color maps
CMAP_RPLAN = get_cmap(mcolors.ListedColormap(COLORS_RPLAN))
CMAP_LIFULL = get_cmap(mcolors.ListedColormap(COLORS_LIFULL))
CMAP_MSD = get_cmap(mcolors.ListedColormap(COLORS_MSD))

ROOM_ARRAY_TOGETHER = [[0],
                       [1, 5, 7, 8], # bedroom
                       [2],
                       [3],
                       [4],
                       [6],
                       [9],
                       [10],
                       [11],
                       [12],
                       [13],
                       [14],
                       [15],
                       [16],
                       [17]]

COLORS_RPLAN_REDUC = ['#1f77b4',  # living room
                         '#e6550d',  # bedroom
                         '#fd8d3c',  # kitchen
                         '#fdae6b',  # bathroom
                         '#fdd0a2',  # dining room
                         '#5254a3',  # study room
                         '#37c837',  # balcony
                         '#1f77b4',  # entrance
                         '#98df8a',  # storage
                         '#d62728',  # walk-in
                         '#e6e6e6',  # external area
                         '#000000',  # exterior wall
                         '#000000',  # front door
                         '#000000',  # interior wall
                         '#ffffff']  # interior door

# Color maps
CMAP_RPLAN = get_cmap(mcolors.ListedColormap(COLORS_RPLAN))
CMAP_RPLAN_REDUC = get_cmap(mcolors.ListedColormap(COLORS_RPLAN_REDUC))


# Entity categories and associated classes
CATEGORIES = ["living room",
              "master room",
              "kitchen",
              "bathroom",
              "dining room",
              "child room",
              "study room",
              "second room",
              "guest room",
              "balcony",
              "entrance",
              "storage",
              "walk-in",
              "external area",
              "exterior wall",
              "front door",
              "interior wall",
              "interior door"]

# Entity categories and associated classes
CAT_RPLAN =  ["livingroom",
              "bedroom",
              "kitchen",
              "bathroom",
              "dining room",
              "child room",
              "study room",
              "second room",
              "guest room",
              "balcony",
              "corridor",
              "storage",
              "walk-in",
              "external area",
              "exterior wall",
              "front door",
              "interior wall",
              "interior door"]

CAT_MSD = ['bedroom',  # modified swiss dwellings: 5.4k V2 version
           'livingroom',
           'kitchen',
           'dining',
           'corridor',
           'stairs',
           'storeroom',
           'bathroom',
           'balcony',
           'structure',
           'door',
           'entrance Door',
           'window']

CLASSES = np.arange(0, len(CAT_RPLAN))


# Roots
DATA_PATH = r'C:\Users\caspervanengel\OneDrive\Documents\PHD\1_data\rplan\0-full'