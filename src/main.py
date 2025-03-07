#this uses Environment Agency flood and river level data from the real-time data API (Beta)


from module import *


other = "https://environment.data.gov.uk/flood-monitoring/id/floodAreas/122WAC953"
trial = "https://environment.data.gov.uk/flood-monitoring/id/stations/1029TH/readings?latest.csv"



if __name__ == "__main__":
    df = readings_getter("1029TH",time=24.)
    # df = readings_getter("720763")


    plotter(df)
