# GeoJSON to GPX Converter

aka: Google Takeout Location History GeoJSON to GPX converter

This is a script that is part of my photo geotagging workflow (which you can read about here) but it can be used to convert the Google Takeout format into a gpx format for use anywhere else. This conversion is lossy and you will only get the location, timestamp, accuracy and speed data for each point. All other Metadata will be lost.

## Requirements
- Python > 3.7
- A bit of command line knowledge

## Usage
```
usage: geojson2gpx.py [-h] [-s START] [-e END] input output

positional arguments:
  input                     Input File (JSON)
  output                    Output File (will be overwritten!)

options:
  -h, --help                 show this help message and exit
  -s START, --start START    Start date inclusive (YYYY-MM-DD)
  -e END, --end END          End date inclusive (YYYY-MM-DD)
```

## Example:
Assuming the GeoJSON file is `Records-002.json`, and the output file you want is `location-history.gpx`.

Put the file `geojson2gpx.py` in the same folder as `Records-002.json`
```
> python3 geojson2gpx.py Records-002.json location-history.gpx
```

## “Advanced” Usage
Sometimes having 10 years of history in one file might lag the program you’re trying to import it into, so you can use the optional flags -s and -e to specify a start and end date. 

You can also run this once for each year and export the different tracks to different years. I could have built this functionality into the script, but I was way too lazy and it was much easier to just run the script multiple times and wait.

This is the bash code I came up with for getting it to split the files into different years.

```
python3 self.py Records-002.json output-2013.gpx -s 2013-01-01 -e 2013-12-31 && \
python3 self.py Records-002.json output-2014.gpx -s 2014-01-01 -e 2014-12-31 && \
python3 self.py Records-002.json output-2015.gpx -s 2015-01-01 -e 2015-12-31 && \
python3 self.py Records-002.json output-2016.gpx -s 2016-01-01 -e 2016-12-31 && \
python3 self.py Records-002.json output-2017.gpx -s 2017-01-01 -e 2017-12-31 && \
python3 self.py Records-002.json output-2018.gpx -s 2018-01-01 -e 2018-12-31 && \
python3 self.py Records-002.json output-2019.gpx -s 2019-01-01 -e 2019-12-31 && \
python3 self.py Records-002.json output-2020.gpx -s 2020-01-01 -e 2020-12-31 && \
python3 self.py Records-002.json output-2021.gpx -s 2021-01-01 -e 2021-12-31 && \
python3 self.py Records-002.json output-2021.gpx -s 2021-01-01 -e 2021-12-31 && \
python3 self.py Records-002.json output-2023.gpx -s 2023-01-01 -e 2023-12-31
```

As you can see, this is some extremely advanced stuff, so proceed with caution.
Alternatively, you could also write a for loop in bash but I was too lazy to stackoverflow the syntax.

## Using the GPX file
Once you have the gpx files and want to use it to geotag your photos, you can refer to the main tutorial (which is not yet available)


