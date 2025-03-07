#this uses Environment Agency flood and river level data from the real-time data API (Beta)

import requests as R
import pandas as pd
import io
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


other = "https://environment.data.gov.uk/flood-monitoring/id/floodAreas/122WAC953"
trial = "https://environment.data.gov.uk/flood-monitoring/id/stations/1029TH/readings?latest.csv"

def str_to_datetime(API_dt:str) -> datetime:
    #converts the API's time format to a datetime object
    return datetime.strptime(API_dt,"%Y-%m-%dT%H:%M:%SZ")

def datetime_to_str(dt:datetime) -> str:
    #converts a datetime object to the API's time fromat
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

def data_reader(station_ID:str, time:float=24.) -> pd.DataFrame: #gets the latest {time}hrs worth of readings from the api
    root = "https://environment.data.gov.uk/flood-monitoring/id/stations/"
    ending = "/readings.csv"
    oldest = datetime.now() - timedelta(hours=time//1,minutes=time%1*60)
    time_filter = f"?since={datetime_to_str(oldest)}"

    try:
        req = R.get(f"{root}{station_ID}{ending}{time_filter}").content
    except:
        raise Exception("Error grabbing data from the API")
    
    return pd.read_csv(io.StringIO(req.decode("utf-8")))

def plotter(df:pd.DataFrame) -> None:
    
    measures = []
    for m in df["measure"]:
        if m not in measures:
            measures.append(m)
    print(measures[0][40:])
    print("\n\n\n")

    for m in measures:
        times = []
        values = []
        for i in range(len(df["value"])):
            if df["measure"].iloc[i] == m:
                times.append(str_to_datetime(df["dateTime"].iloc[i]))
                values.append(df["value"].iloc[i])
        plt.plot(times,values,label=m[:])

    # plt.plot(times,df["value"])
    # plt.show()


df = data_reader("1029TH")
# print(df.columns)
# print(df["dateTime"])

plotter(df)

# dt = df["dateTime"].iloc[0]
# print(dt)
# print(str_to_datetime(dt))
# print(datetime_to_str(str_to_datetime(dt)))
