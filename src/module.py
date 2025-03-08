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
    def __init__(self,station_ID:str,time:float=24.): #time is in hours
        self.station = station_ID
        #find possible measures for station
        df = self.data_getter(f"/id/stations/{station_ID}/measures")
        measures = []
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
        

    def data_getter(self,item:str,time:float=None,m:dict=None) -> pd.DataFrame: #returns None if no data found
        #gets readings from the Flooding API, possible option to filter for both time (in hrs) and by measure type
        root = "https://environment.data.gov.uk/flood-monitoring/"
        filter = ""
        if time != None:
            oldest = datetime.now() - timedelta(hours=time//1,minutes=time%1*60)
            filter += f"?since={datetime_to_str(oldest)}"

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
        print(self.master)

        fig, axs = plt.subplots(nrows=len(axes),sharex=True)
        if len(axes) == 1:
            axs = [axs]
        
        for ax,param in zip(axs,axes):
            for m in self.master:
                if m["parameter"] == param:
                    ax.plot(m["df"]["dateTime"].apply(str_to_datetime),m["df"]["value"],label=f'{m["qualifier"]} {m["value"]} ({m["unit"]})')
                    ax.set_ylabel(m["name"])
            ax.legend()


        # axes = []
        # for m in self.master:
        #     if m["name"] not in axes:
        #         if len(axes) > 1:
        #             axes.append(ax.twin())
        #             axes_names[m["name"]] = i
                    
        #         else:
        #             axes.append(ax)
        #     i+=1
        # print(axes)
        
        # # axes[m["name"]].get_yaxis().set_tick_params(direction='out')
        # # axes[m["name"]].spines["right"].set_position(("axes",displace))     
        # # axes[m["name"]].set_ylabel(f'{m["name"]} - {m["qualifier"]} ({m["unit"]})')      
        # fig.subplots_adjust(right=0.75)
        
        
        # # for name in axes:
            
        
        # last = axes[list(axes.keys())[0]]
        # last.set_frame_on(True)
        # last.patch.set_visible(False)
        

        # #plot on each axis
        # for m in self.master:
        #     times = []
        #     values = []
        #     for i in range(len(m["df"]["value"])):
        #         times.append(str_to_datetime(m["df"]["dateTime"].iloc[i]))
        #         values.append(m["df"]["value"].iloc[i])
        #     axes[m["name"]].plot(times,values,label=f'{m["name"]} - {m["qualifier"]} ({m["value"]})')
            

        #other plot setting
        ticks = plt_ticker.LinearLocator(6)
        axs[-1].xaxis.set_major_locator(ticks)
        format = plt_dates.DateFormatter("%m/%d %H:%M")
        axs[-1].xaxis.set_major_formatter(format)
        plt.xticks(rotation=30)
        
        axs[-1].set_xlabel("Date & Time")
        # fig.legend()
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
    # a = flooding("720763")
    # a = flooding("1029TH")
    # a = flooding("733548") #has no readings in the last 24 hours as of 08/03/2025
    a = flooding("50181")
    # a = flooding("3680")
    a.plot()
    # a.table(open=True)