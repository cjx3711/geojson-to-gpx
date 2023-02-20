import json
import sys
from argparse import ArgumentParser
from datetime import datetime

# This file is in python3
# This processes the Google Takeout Location History JSON file
# and converts it to GPX format
# The file format is correct as of 2023-02-01

def main(argv):
  arg_parser = ArgumentParser()
  arg_parser.add_argument("input", help="Input File (JSON)")
  arg_parser.add_argument("output", help="Output File (will be overwritten!)")
  arg_parser.add_argument("-s", "--start", default=None, help="Start date inclusive (YYYY-MM-DD)")
  arg_parser.add_argument("-e", "--end", default=None, help="End date inclusive (YYYY-MM-DD)")

  args = arg_parser.parse_args()
  if args.input == args.output:
    arg_parser.error("Input and output have to be different files")
    return

  print("Opening file %s" % args.input)
  try:
    json_data = open(args.input).read()
  except:
    print("Error opening input file")
    return

  print("Decoding json")
  try:
    data = json.loads(json_data)
  except:
    print("Error decoding json")
    return

  # Open the output file for writing
  try:
    f_out = open(args.output, "w")
  except:
    print("Error creating output file for writing")
    return
  
  f_out.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
  f_out.write("<gpx xmlns=\"http://www.topografix.com/GPX/1/1\" version=\"1.1\" creator=\"Google Latitude JSON Converter\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd\">\n")
  f_out.write("  <metadata>\n")
  f_out.write("    <name>Location History</name>\n")
  f_out.write("  </metadata>\n")
  f_out.write("  <trk>\n")
  f_out.write("    <trkseg>\n")

  # Check if the data has locations
  if "locations" in data and len(data["locations"]) > 0:
    items = data["locations"]
    count = 0
    added = 0
    for item in items:
      count += 1
      if (count % 10000 == 0):
        print("Processed %s items" % count)
      if ("latitudeE7" not in item or "longitudeE7" not in item):
        print("Skipping item %s" % count)
        print(item)
        continue
      latitude = int(item["latitudeE7"]) / 10000000.0
      longitude = int(item["longitudeE7"]) / 10000000.0
      timestamp = item["timestamp"]

      if args.start is not None:
        # Get date part of timestamp
        date = timestamp.split("T")[0]
        if date < args.start:
          continue
      if args.end is not None:
        # Get date part of timestamp
        date = timestamp.split("T")[0]
        if date > args.end:
          continue

      added += 1
      altitude = item["altitude"] if "altitude" in item else None
      accuracy = item["accuracy"] if "accuracy" in item else None
      speed = item["speed"] if "speed" in item else None
      f_out.write("      <trkpt lat=\"%s\" lon=\"%s\">\n" % (latitude, longitude))
      if "altitude" in item:
          f_out.write("        <ele>%d</ele>\n" % altitude)
      f_out.write("        <time>%s</time>\n" % timestamp)
      if "accuracy" in item or "speed" in item:
          f_out.write("        <desc>\n")
          if "accuracy" in item:
              f_out.write("          Accuracy: %d\n" % accuracy)
          if "speed" in item:
              f_out.write("          Speed:%d\n" % speed)
          f_out.write("        </desc>\n")
      f_out.write("      </trkpt>\n")
    f_out.write("    </trkseg>\n")
    f_out.write("  </trk>\n")
    f_out.write("</gpx>\n")
  f_out.close()

  print("Done! Processed %d lines, added %d lines." % (count, added))

if __name__ == "__main__":
  main(sys.argv)
