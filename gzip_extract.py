"""
Use to unzip files from Strava bulk export
Handles .fit.gz and .gpx.gz automatically

Last update: 2020-05-11
"""
import glob
import gzip
import shutil

files = glob.glob('*.fit.gz')

for i, file in enumerate(files):
    out_file = str(i) + '.fit'
    with gzip.open(file, 'rb') as f_in:
        with open(out_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

files = glob.glob('*.gpx.gz')

for i, file in enumerate(files):
    out_file = str(i) + '.gpx'
    with gzip.open(file, 'rb') as f_in:
        with open(out_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
