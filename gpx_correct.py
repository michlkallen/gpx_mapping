"""
Script to correct timestamps on GPX files.

Use if creating a GPX file manually through www.gpxgenerator.com
and the speed used is incorrect. (Or if you want to modify an existing route.)

To use:
-------
1. Edit the `file_in` name and the `file_out` name if desired.
2. Edit the average speed (and variability) if desired. Currently set up for 4:25/km

After navigating to the directory in question, run:

`python gpx_correct.py`

Returns elapsed time and a new GPX file to the directory.

The script is currently set up to only function when there are also "elev" tags in the
GPX file. It could be modified in the future to work without.
"""
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import haversine

# File to modify
file_in = "0331.gpx"
file_out = file_in[:-4] + "-analog.gpx"

# Average speed (avg_rate) [seconds/km] and variability (var) [seconds]
avg_rate = 265
var = 10

# namespace for GPX files
ns = {"gpx": "http://www.topografix.com/GPX/1/1"}

# initialize lists for distance, elevation gain, elevation
elev_gain = [0]
distance = [0]
elev = [0]


# Extract the longitude, latitude, elevation, timestamp from the gpx
tree = ET.parse(file_in)
latitude = [
    float(x.attrib["lat"])
    for x in tree.findall("./gpx:trk/gpx:trkseg/gpx:trkpt", ns)
]
longitude = [
    float(y.attrib["lon"])
    for y in tree.findall("./gpx:trk/gpx:trkseg/gpx:trkpt", ns)
]
elevation = [
    float(e.text)
    for e in tree.findall("./gpx:trk/gpx:trkseg/gpx:trkpt/gpx:ele", ns)
]
timestamp = [
    t.text for t in tree.findall("./gpx:trk/gpx:trkseg/gpx:trkpt/gpx:time", ns)
]

# Calculate the distance and elevation traveled
for i in range(len(latitude)):
    if i == 0:
        pass
    else:
        p1_lat, p1_lon = latitude[i - 1], longitude[i - 1]
        p2_lat, p2_lon = latitude[i], longitude[i]

        delta = haversine.haversine((p1_lat, p1_lon), (p2_lat, p2_lon))
        elev_delta = elevation[i] - elevation[i - 1]
        delta_3d = np.sqrt(delta**2 + (elev_delta/1000)**2)

        distance.append(delta_3d)
        elev.append(elev_delta)

# Update the timestamps!
rate = avg_rate + np.random.default_rng().integers(-var, var,
                                                   size=len(distance),
                                                   endpoint=True)

# Calculate the seconds between data points
time_delta = np.array(distance)*rate

# Calculate the cumulative sum (easier for writing the next step)
time_delta_cum = np.cumsum(time_delta)
new_stamps = [
    (pd.to_datetime(timestamp[0])
     + pd.Timedelta(time_delta_cum[i], "s")).strftime("%Y-%m-%dT%H:%M:%SZ")
    for i in range(len(timestamp))
    ]

for i, time in enumerate(tree.iterfind("./gpx:trk/gpx:trkseg/gpx:trkpt/gpx:time", ns)):
    time.text = new_stamps[i]

tree.write(file_out, encoding="UTF-8")

print(f"{time_delta_cum[-1]/60:.1f} minutes")
