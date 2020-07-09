# GPX heatmaps
## Heatmap plotter `gpx_map.py`
Plotting of GPX routes (running, biking, etc.) in a heatmap with elevation.

Script is run via the command line (`python gpx_map.py`) and can handle single/multiple GPX files. It looks more interesting with multiple files. The files are sorted by name, so if elevation is turned on, it is recommended to having a naming convention which gives the proper chronological order (since the elevation plot is cumulative).

It has been tested with GPX files from Strava. It may work for other formats.

_To use:_
1. Edit the `files` list if you want a single GPX track or multiple. It's currently configured for multiple files (sorted by date for elevation purposes). It currently runs in the same directory as the files
2. Edit the `evelation_on` if you want to turn off the elevation plotting (in case the file doesn't have elevation or you simply don't want to see it)
3. Edit the `auto_bound` if you want to manually set the figure bounds: `bottom_left` and `upper_right`

With lots of files, it starts to look like this:

![normal](https://github.com/michlkallen/gpx_mapping/blob/master/images/heatmap_simple.png)

With only a few, it looks more like this:

![simple](https://github.com/michlkallen/gpx_mapping/blob/master/images/heatmap_simple.png)

And turning off the elevation would look like this:

![simple_no_elev](https://github.com/michlkallen/gpx_mapping/blob/master/images/heatmap_no_elev.png)

# Miscellaneous Tools
## Unzipping Strava bulk export `gpx_extract.py`
Quick script to take the zipped export file from Strava and pull out all the FIT and GPX files

## Fixing a route with incorrect times `gpx_correct.py`
Script to correct timestamps on GPX files.

Use if creating a GPX file manually through www.gpxgenerator.com (for example) and the speed used is incorrect. (Or if you want to modify an existing route.)

_To use:_
1. Edit the `file_in` name and the `file_out` name if desired.
2. Edit the average speed (and variability) if desired. Currently set up for 4:25/km

After navigating to the directory in question, run:

`python gpx_correct.py`

Returns elapsed time and a new GPX file to the directory.

The script is currently set up to only function when there are also "elev" tags in the
GPX file. It could be modified in the future to work without.

## Converting Garmin FIT to GPX
To convert FIT files to GPX files using GPS Babel (Windows .bat file):
```
FOR %%i IN (*.fit) DO "C:\Program Files (x86)\GPSBabel\gpsbabel" -i garmin_fit -f %%i -o gpx,gpxver=1.1 -F %%~Ni_fit.gpx
```
