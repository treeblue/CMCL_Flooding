import requests as R
import pandas as pd
import io
import matplotlib.pyplot as plt
import matplotlib.ticker as plt_ticker
import matplotlib.dates as plt_dates
from datetime import datetime, timedelta

def str_to_datetime(API_dt:str) -> datetime:
    #converts the API's time format to a datetime object
    return datetime.strptime(API_dt,"%Y-%m-%dT%H:%M:%SZ")

def datetime_to_str(dt:datetime) -> str:
    #converts a datetime object to the API's time fromat
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

def readings_getter(station_ID:str, time:float=24.) -> pd.DataFrame:
    #gets the latest {time}hrs worth of readings from the api
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
    
    #determine which measures the station has
    possible_measures = {
        "Water Level":"level",
        "Flow":"flow",
        "Wind Direction":"wind-direction",
        "Wind Speed":"wind-speed",
        "Temperature":"temperature"}
    measures = {}
    for m in df["measure"]:
        for pm in possible_measures:
            if possible_measures[pm] in m:
                if pm in measures:
                    if m[60:] not in measures[pm]:
                        measures[pm].append(m[60:])
                else:
                    measures[pm] = [m[60:]]

    #create axes for each measure
    fig, ax = plt.subplots()
    axes = [ax] + [ax.twinx() for _ in range(len(measures)-1)]
    # print(axes)
                
    #plot on each axis
    for ms,axis in zip(measures,axes):
        for m in measures[ms]:
            times = []
            values = []
            for i in range(len(df["value"])):
                if m in df["measure"].iloc[i]:
                    times.append(str_to_datetime(df["dateTime"].iloc[i]))
                    values.append(df["value"].iloc[i])
            axis.plot(times,values,label=m)

    ticks = plt_ticker.LinearLocator(6)
    axes[0].xaxis.set_major_locator(ticks)
    format = plt_dates.DateFormatter("%m/%d %H:%M")
    axes[0].xaxis.set_major_formatter(format)
    plt.xticks(rotation=30)
    
    axes[0].set_xlabel("Date & Time")
    for label,axis in zip(measures.keys(),axes):
        axis.set_ylabel(label)
    fig.legend()
    plt.show()

