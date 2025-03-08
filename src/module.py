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

class flooding:
    def __init__(self,station,time:float=24.): #time is in hours
    
        if type(station)==int or any(i.isdigit() for i in str(station)):
            station_IDs = [str(station)]
        elif type(station) == str:
            DF = self.data_getter("/id/stations",filter=f"?label={station}")
            station_IDs = list(DF["stationReference"].iloc[:])
        else:
            raise Exception("Please use either a station ID (int/str) or station name (str) as an input")

        self.station = str(station)

        #find possible measures for station (across all station IDs)
        measures = []
        for station_ID in station_IDs:
            df = self.data_getter(f"/id/stations/{station_ID}/measures")
            for row in df.iloc:
                m = {"name":row["parameterName"],
                    "parameter":row["parameter"],
                    "qualifier":row["qualifier"],
                    "unit":row["unitName"],
                    "value":row["valueType"],
                    "id":row["@id"][60:]}
                measures.append(m)

        #create a master list including dataframes for each available measure
        self.master = []
        for m in measures:
            minidf = self.data_getter(f'/id/measures/{m["id"]}/readings',time)
            if type(minidf) == pd.DataFrame:
                m["df"] = minidf
                self.master.append(m)
        
        if len(self.master) == 0:
            raise Exception(f"There are no readings from this station in the last {time//1} hours")
        
    def data_getter(self,item:str,time:float=None,m:dict=None,filter:str="") -> pd.DataFrame: #returns None if no data found
        #gets readings from the Flooding API, possible option to filter for both time (in hrs) and by measure type
        root = "https://environment.data.gov.uk/flood-monitoring"
        if time != None:
            oldest = datetime.now() - timedelta(hours=time//1,minutes=time%1*60)
            filter += f"?since={datetime_to_str(oldest)}"

        # print(f"{root}{item}{filter}") #printing link for debugging
        try:
            req = R.get(f"{root}{item}.csv{filter}").content
        except:
            raise Exception(f"Error getting data from the API at {root}{item}.csv{filter}")
        
        try:
            return pd.read_csv(io.StringIO(req.decode("utf-8")))
        except:
            return None
    
    def plot(self) -> None:
        #create axes for each parameter
        axes = []
        units = []
        for m in self.master:
            if m["parameter"] not in axes:
                axes.append(m["parameter"])

        fig, axs = plt.subplots(nrows=len(axes),sharex=True)
        if len(axes) == 1:
            axs = [axs]
        
        for ax,param in zip(axs,axes):
            for m in self.master:
                if m["parameter"] == param:
                    m["df"].sort_values(by=["dateTime"],inplace=True)
                    ax.plot(m["df"]["dateTime"].apply(str_to_datetime),m["df"]["value"],label=f'{m["qualifier"]} {m["value"]} ({m["unit"]})')
                    ax.set_ylabel(m["name"])
            ax.legend()

        #other plot setting
        ticks = plt_ticker.LinearLocator(6)
        axs[-1].xaxis.set_major_locator(ticks)
        format = plt_dates.DateFormatter("%m/%d %H:%M")
        axs[-1].xaxis.set_major_formatter(format)
        plt.xticks(rotation=30)
        
        axs[-1].set_xlabel("Date & Time")
        plt.show()

    def table(self,open:bool=False) -> pd.DataFrame:
        #make a list of all dataframes as well as labels for the dataframe columns
        all_dfs = []
        value_labels = []
        for m in self.master:
            value_labels.append(f'{m["name"]}-{m["qualifier"]}-{m["value"]} ({m["unit"]})')
            all_dfs.append(m["df"].copy())
        
        #rename "value" comlumns
        for df,label in zip(all_dfs,value_labels):
            del df["measure"]
            df.rename(columns={"dateTime":"DateTime","value":label},inplace=True)
            df.set_index("DateTime")

        #join all of the dataframes
        master_df = all_dfs[0].copy()
        for df in all_dfs[1:]:
            master_df = master_df.join(df,rsuffix="_copy")
            del master_df["DateTime_copy"]

        #change DateTime column to be DateTime objects instead of strings
        master_df["DateTime"] = master_df["DateTime"].apply(lambda x: str_to_datetime(x))
        master_df.to_csv(f"{self.station}_Flooding_Data.csv")
        if open:
            import os
            os.startfile(f"{self.station}_Flooding_Data.csv")

        return master_df


if __name__ == "__main__":
    a = flooding("COOMBE CELLARS")
    # a = flooding("720763")
    # a = flooding("1029TH")
    # a = flooding(733548) #has no readings in the last 24 hours as of 08/03/2025
    # a = flooding(50181) #has wind speed in both (Knot) and (Knots)
    # a = flooding("3680")
    a.plot()
    # a.table(open=True)