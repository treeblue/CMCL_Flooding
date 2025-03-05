#this uses Environment Agency flood and river level data from the real-time data API (Beta)

import requests as R
import pandas as pd
import io

# root = "https://environment.data.gov.uk/flood-monitoring"
# ending = ".csv"
other = "https://environment.data.gov.uk/flood-monitoring/id/floodAreas/122WAC953"

# stations = f"{root}/id/stations{ending}"


def reader(specifier:str) -> pd.DataFrame:
    root = "https://environment.data.gov.uk/flood-monitoring"
    ending = ".csv"

    try:
        req = R.get(f"{root}{specifier}{ending}").content
    except:
        raise Exception("invalid url")
    
    return pd.read_csv(io.StringIO(req.decode("utf-8")))

df = reader("/id/stations/1029TH/readings")
print(df.columns)
print(df["dateTime"].iloc[0])