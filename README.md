## Overview
This project provides a framework to access recent data from the real time flood monitoring API (https://environment.data.gov.uk/flood-monitoring/doc/reference) and provides a basic gui and sample script in which how to use the framework.

## Python libraries used:
- requests
- pandas
- io
- matplotlib
- datetime
- tkinter

## Usage
Importing the tools:
```bash
from module import selector, flooding
```
### GUI
The GUI uses tkinter, it produces an ordered list.
It is ordered by station status and then alphabetically by station name.
Some stations might not work with the script due to data returned by the API. For any stations with a non-active status this is typically due to a lack of recent data.

Running the GUI:
```bash
s = selector()
```
The GUI returns the selected station as a string, called by:
```bash
s.station
```

### Backend
The backend is a stand alone python class that takes 2 arguments: a station identifier and a time (default is 24 hours). The station identifier can either be a station name or a station ID. The time is the desired duration of the collected data in hours before the current time.
There are two function intended for the user, plot() and table(). plot() takes no arguments and purely plots the selected station data using matplotlib. table() returns a pandas DataFrame object as well as saving it to a csv, it has a boolian argument that when set to True opens the file at runtime.

### Example full stack use
As seen in main.py:
```bash
s = selector()
a = flooding(s.station)
a.table(open=True)
a.plot()
```

## Files
- main.py - contains a full stack script, just run this if you want all data from a station in the last 24 hours
- module.py - contains both the selector and flooding classes, as well as some test cases which I got manually from the API

## Additional Notes:
- Colours used in the graphs are chosen with colourblind readability in mind.
- Some stations use multiple different units for similar measurements, these are plotted on the same axis and is the reason most units are in the graph labels instead of on the y-axis