#this uses Environment Agency flood and river level data from the real-time data API (Beta)
from module import flooding,selector


if __name__ == "__main__":
    s = selector()
    a = flooding(s.station)
    a.table(open=False)
    a.plot()
