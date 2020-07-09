"""
Script to generate a heatmap PNG image of a single or multiple GPX files.

It includes option for setting the boundary for the figure (in case you have GPX files
from a wide variety of locations) as well as the ability to plot elevation.

It has been tested with GPX files from Strava. It may work for other formats.

To use:
-------
1. Edit the `files` list if you want a single GPX track or multiple. It's currently
   configured for multiple files (sorted by date for elevation purposes)
   It currently runs in the same directory as the files
2. Edit the `evelation_on` if you want to turn off the elevation plotting
   (in case the file doesn't have elevation or you simply don't want to see it)
3. Edit the `auto_bound` if you want to manually set the figure bounds:
   `bottom_left` and `upper_right`

Navigate to the directory via the terminal and run:

`python gpx_map.py`
"""
import glob
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import haversine

# Uncomment to set a prettier font
# mpl.rcParams["font.sans-serif"] = "Clear Sans"

# Generate a list of the files (and order by date (name))
files = sorted(glob.glob("*.gpx"))

# Whether to include elevation
elevation_on = True

# Figure boundary settings
auto_bound = True
bottom_left = [-71.88404399631361, 42.21004834738177]  # lat long - get from OSM/equiv
upper_right = [-71.73123784139484, 42.34119566293228]  # lat long - get from OSM/equiv

# namespace for GPX files
ns = {"gpx": "http://www.topografix.com/GPX/1/1"}

# Configure the figure
fig = plt.figure(figsize=(10, 10), tight_layout=True)

if elevation_on:
    gs = mpl.gridspec.GridSpec(nrows=2, ncols=1, height_ratios=[14, 1])

    ax_top = fig.add_subplot(gs[0, 0])
    ax_bot = fig.add_subplot(gs[1, 0])

    ax_bot.axis("off")
else:
    ax_top = fig.add_subplot()

if auto_bound is False:
    ax_top.set_xlim(left=bottom_left[0], right=upper_right[0])
    ax_top.set_ylim(bottom=bottom_left[1], top=upper_right[1])

# Clean up the figure a bit
ax_top.axis("off")
ax_top.set_aspect("equal")

# initialize lists for distance, elevation gain, elevation
distance = [0]

if elevation_on:
    elev_gain = [0]
    elev = [0]

for file in files:
    # Extract the longitude, latitude, elevation, timestamp from the gpx
    tree = ET.parse(file)
    latitude = [
        float(x.attrib["lat"])
        for x in tree.findall("./gpx:trk/gpx:trkseg/gpx:trkpt", ns)
    ]
    longitude = [
        float(y.attrib["lon"])
        for y in tree.findall("./gpx:trk/gpx:trkseg/gpx:trkpt", ns)
    ]
    timestamp = [
        t.text for t in tree.findall("./gpx:trk/gpx:trkseg/gpx:trkpt/gpx:time", ns)
    ]
    if elevation_on:
        elevation = [
            float(e.text)
            for e in tree.findall("./gpx:trk/gpx:trkseg/gpx:trkpt/gpx:ele", ns)
        ]

    # Calculate the distance and elevation traveled
    for i in range(len(latitude)):
        if i == 0:
            pass
        else:
            p1_lat, p1_lon = latitude[i - 1], longitude[i - 1]
            p2_lat, p2_lon = latitude[i], longitude[i]

            delta = haversine.haversine((p1_lat, p1_lon), (p2_lat, p2_lon))

            if elevation_on:
                elev_delta = elevation[i] - elevation[i - 1]
                delta_3d = np.sqrt(delta ** 2 + (elev_delta / 1000) ** 2)
                distance.append(delta_3d)
                elev.append(elev_delta)

                # Elevation gained only uses > 0
                if elev_delta > 0:
                    elev_gain.append(elev_delta)
                else:
                    elev_gain.append(0)

            else:
                distance.append(delta)

    # Throw the stuff onto a plot
    ax_top.plot(
        longitude,
        latitude,
        c="k",
        ls="-",
        lw=1,
        alpha=0.3,
        solid_capstyle="round",
        solid_joinstyle="round",
    )

if elevation_on:
    ax_bot.fill_between(range(len(elev)), np.cumsum(elev), facecolor="g", alpha=0.6)

    # Add some stats for the title
    plt.suptitle(
        f"Total Distance: {np.round(np.sum(distance),1)} km, \
    Elevation Gain: {np.round(np.sum(elev_gain),0):.0f} m"
    )
else:
    plt.suptitle(f"Total Distance: {np.round(np.sum(distance),1)} km")

# plt.show()
plt.savefig("heatmap.png", dpi=300, bbox_inches="tight")
